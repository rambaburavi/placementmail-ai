from .header_parser import HeaderParser
from .body_parser import BodyParser
from .attachment_parser import AttachmentParser
from .link_extractor import LinkExtractor


class ParserAgent:

    def __init__(self):

        self.header_parser = HeaderParser()
        self.body_parser = BodyParser()
        self.attachment_parser = AttachmentParser()
        self.link_extractor = LinkExtractor()

    def parse(self, message):

        payload = message["payload"]

        headers = self.header_parser.parse(
            payload["headers"]
        )

        body = self.body_parser.parse(
            payload
        )

        attachments = self.attachment_parser.parse(
            payload
        )

        links = self.link_extractor.extract(
    body["plain_text"] or body["html"]
)

        return {

            "message_id": message["id"],

            "thread_id": message["threadId"],

            **headers,

            **body,

            "attachments": attachments,

            "links": links
        }