class HeaderParser:
    
    HEADER_MAP = {
        "From": "sender",
        "Subject": "subject",
        "Date": "timestamp",
        "To": "recipient",
        "Cc": "cc",
        "Bcc": "bcc",
        "Reply-To": "reply_to",
        "Message-ID": "message_header_id",
    }

    def parse(self, headers):

        result = {
            "sender": "",
            "recipient": "",
            "subject": "",
            "timestamp": "",
            "cc": "",
            "bcc": "",
            "reply_to": "",
            "message_header_id": "",
        }

        for header in headers:

            key = self.HEADER_MAP.get(header["name"])

            if key:
                result[key] = header["value"]

        return result