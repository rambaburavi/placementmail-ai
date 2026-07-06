from datetime import datetime

from app.services.gmail.gmail_service import GmailService
from app.agents.parser.parser_agent import ParserAgent
from app.agents.analyzer.analyzer_agent import AnalyzerAgent

from app.repositories.email_repository import EmailRepository
from app.repositories.reminder_repository import ReminderRepository

from app.models.email import Email
from app.models.email_reminder import EmailReminder

from app.services.notifications.notification_service import NotificationService

from app.reminder.deadline_parser import DeadlineParser
from app.reminder.reminder_service import ReminderService
from app.reminder.reminder_scheduler import ReminderScheduler


class EmailWorkflow:

    def __init__(self, db):

        self.gmail = GmailService()
        self.parser = ParserAgent()
        self.ai = AnalyzerAgent()

        self.repository = EmailRepository(db)
        self.reminder_repository = ReminderRepository(db)

        self.notification = NotificationService()

        self.reminder_service = ReminderService()
        self.reminder_scheduler = ReminderScheduler()

    def process_email(self, message_id: str):

        # ----------------------------------------------------
        # Duplicate Check
        # ----------------------------------------------------

        existing = self.repository.get_by_message_id(message_id)

        if existing:
            return {
                "status": "already_processed",
                "gmail_message_id": existing.gmail_message_id,
                "thread_id": existing.thread_id,
                "sender": existing.sender,
                "subject": existing.subject,
                "category": existing.category,
                "priority": existing.priority,
                "placement_related": existing.placement_related,
                "company": existing.company,
                "deadline": existing.deadline,
                "summary": existing.summary,
                "action_required": existing.action_required,
            }

        # ----------------------------------------------------
        # Fetch Gmail Email
        # ----------------------------------------------------

        gmail_message = self.gmail.get_message(message_id)

        # ----------------------------------------------------
        # Parse Email
        # ----------------------------------------------------

        parsed = self.parser.parse(gmail_message)

        # ----------------------------------------------------
        # AI Analysis
        # ----------------------------------------------------

        analysis = self.ai.analyze(parsed)

        deadline_text = analysis.get("deadline")

        # ----------------------------------------------------
        # Create Email Model
        # ----------------------------------------------------

        email = Email(
            gmail_message_id=parsed["message_id"],
            thread_id=parsed["thread_id"],
            sender=parsed["sender"],
            subject=parsed["subject"],
            body=parsed["plain_text"],

            category=analysis["category"],
            priority=analysis["priority"],
            placement_related=analysis["placement_related"],

            company=analysis["company"],

            deadline=deadline_text,

            action_required=analysis["action_required"],
            summary=analysis["summary"],

            ai_provider=analysis["ai_provider"],
            analysis_status=analysis["analysis_status"],

            created_at=datetime.utcnow(),
        )

        # ----------------------------------------------------
        # Save Email
        # ----------------------------------------------------

        saved_email = self.repository.save(email)

        # ----------------------------------------------------
        # Parse Deadline
        # ----------------------------------------------------

        deadline_at = DeadlineParser.parse(deadline_text)

        if deadline_at:

            saved_email.deadline_at = deadline_at

            self.repository.update(saved_email)

            reminders = self.reminder_service.get_reminder_times(
                deadline_at
            )

            for label, reminder_time in reminders:

                job_id = f"{saved_email.id}_{label}"

                # Skip duplicate reminders

                if self.reminder_repository.exists(job_id):
                    continue

                offset_minutes = int(
                    (deadline_at - reminder_time).total_seconds() / 60
                )

                reminder = EmailReminder(
                    email_id=saved_email.id,
                    job_id=job_id,
                    offset_minutes=offset_minutes,
                    reminder_time=reminder_time,
                    status="PENDING",
                )

                reminder = self.reminder_repository.create_reminder(
                    reminder
                )

                scheduled = self.reminder_scheduler.schedule(
                    reminder_id=reminder.id,
                    email_id=saved_email.id,
                    label=label,
                    reminder_time=reminder_time,
                )

                if scheduled:
                    self.reminder_repository.mark_scheduled(
                        reminder.id
                    )

        # ----------------------------------------------------
        # Notifications
        # ----------------------------------------------------

        analysis["subject"] = saved_email.subject
        analysis["sender"] = saved_email.sender
        analysis["company"] = saved_email.company
        analysis["category"] = saved_email.category
        analysis["priority"] = saved_email.priority

        analysis["notify_telegram"] = True
        analysis["notify_whatsapp"] = False

        self.notification.notify(analysis)

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "status": "processed",
            "gmail_message_id": saved_email.gmail_message_id,
            "thread_id": saved_email.thread_id,
            "sender": saved_email.sender,
            "subject": saved_email.subject,
            "category": saved_email.category,
            "priority": saved_email.priority,
            "placement_related": saved_email.placement_related,
            "company": saved_email.company,
            "deadline": saved_email.deadline,
            "summary": saved_email.summary,
            "action_required": saved_email.action_required,
            "ai_provider": saved_email.ai_provider,
            "analysis_status": saved_email.analysis_status,
        }