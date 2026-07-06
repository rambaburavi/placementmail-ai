import json
import re


class ResponseParser:

    DEFAULT = {
    "category": "Other",
    "priority": "Low",
    "placement_related": False,
    "notify_telegram": True,
    "notify_whatsapp": False,
    "notification_reason": "",
    "company": "",
    "role": "",
    "deadline": "",
    "summary": "",
    "action_required": "",
    "confidence": 0.0,
}

    def parse(self, text: str):

        # Remove markdown code fences
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

        # Extract the first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            return self.DEFAULT

        try:
            data = json.loads(match.group())

            return {
                **self.DEFAULT,
                **data,
            }

        except Exception:
            return self.DEFAULT