import re


class LinkExtractor:

    URL_PATTERN = re.compile(
        r"https?://[^\s<>\"']+"
    )

    def extract(self, text):

        return list(
            set(
                self.URL_PATTERN.findall(text)
            )
        )