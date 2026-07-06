class NotificationFormatter:
    
    @staticmethod
    def format(email: dict) -> str:

        priority = email.get("priority", "UNKNOWN").upper()

        emoji = {
            "CRITICAL": "🚨",
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "IGNORE": "⚪",
        }.get(priority, "⚪")

        provider = email.get("ai_provider", "Unknown")
        status = email.get("analysis_status", "Unknown")

        return f"""
<b>New Email Received</b>

<b>Company:</b> {email.get("company", "Unknown")}

<b>Subject:</b>
{email.get("subject", "No Subject")}

<b>Category:</b> {email.get("category", "Other")}

{emoji} <b>Priority:</b> {priority}

<b>Deadline:</b>
{email.get("deadline", "Not Mentioned")}

<b>Summary:</b>

{email.get("summary", "No Summary")}

<b>Action Required:</b>

{email.get("action_required", "No Action Required")}

<b>AI Provider:</b> {provider}

<b>Analysis Status:</b> {status}
"""