class AttachmentParser:
    
    def parse(self, payload):

        attachments = []

        self._walk(payload, attachments)

        return attachments

    def _walk(self, part, attachments):

        filename = part.get("filename", "")

        if filename:

            attachments.append({

                "filename": filename,

                "mime_type": part.get(
                    "mimeType",
                    ""
                )
            })

        if "parts" in part:

            for child in part["parts"]:

                self._walk(child, attachments)