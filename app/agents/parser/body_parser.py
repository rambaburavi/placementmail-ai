import base64
from bs4 import BeautifulSoup


class BodyParser:

    def __init__(self):
        self.plain_text = ""
        self.html = ""

    def parse(self, payload):

        self.plain_text = ""
        self.html = ""

        self._walk(payload)

        # If only HTML exists, generate plain text
        if not self.plain_text and self.html:
            self.plain_text = BeautifulSoup(
                self.html,
                "html.parser"
            ).get_text(
                separator=" ",
                strip=True
            )

        return {
            "plain_text": self.plain_text,
            "html": self.html
        }

    def _walk(self, part):

        mime = part.get("mimeType", "")

        # Recursive traversal
        if "parts" in part:
            for child in part["parts"]:
                self._walk(child)

        body = part.get("body", {})
        data = body.get("data")

        if not data:
            return

        try:
            decoded = base64.urlsafe_b64decode(data).decode(
                "utf-8",
                errors="ignore"
            )
        except Exception:
            return

        if mime == "text/plain":
            self.plain_text += decoded

        elif mime == "text/html":
            self.html += decoded