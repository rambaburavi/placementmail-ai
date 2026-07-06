import json


class PromptBuilder:

    def build(self, email):

        return f"""
You are an AI email analyzer for PlacementMail AI.

Analyze the email carefully.

Return ONLY valid JSON.

Do not write markdown.

Do not explain anything.

Categories:

Placement
Internship
Interview
Coding Assessment
Hackathon
Offer Letter
Rejection
Resume Request
College
Newsletter
Finance
Security
Personal
Spam
Other

Priority:

Critical
High
Medium
Low
Ignore

Notification Rules

notify_telegram:
- Always true for every legitimate email.
- Only false for obvious spam or malformed emails.

notify_whatsapp:
True ONLY if the email requires immediate user attention.

Examples:
- Interview Invitation
- Online Assessment
- Coding Assessment
- Resume Shortlisted
- Offer Letter
- Joining Instructions
- Registration Deadline
- Assessment Deadline
- Document Verification
- Placement Process Update with action required
- Deadline within 48 hours

False for:
- Newsletters
- Promotions
- LinkedIn recommendations
- GitHub notifications
- Google security alerts
- Finance updates
- General announcements
- Marketing emails

notification_reason:
Give a short reason.

Examples:
Interview Invitation
Online Assessment
Deadline Tomorrow
Offer Letter
Joining Instructions
Not Important

Return EXACTLY this JSON:

{{
    "category": "",
    "priority": "",
    "placement_related": false,
    "notify_telegram": true,
    "notify_whatsapp": false,
    "notification_reason": "",
    "company": "",
    "role": "",
    "deadline": "",
    "summary": "",
    "action_required": "",
    "confidence": 0.0
}}

EMAIL

{json.dumps(email, indent=2)}
"""