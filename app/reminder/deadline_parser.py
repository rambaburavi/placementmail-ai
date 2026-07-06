from dateutil.parser import parse


class DeadlineParser:

    @staticmethod
    def parse(deadline: str):

        if not deadline:
            return None

        try:
            return parse(deadline)
        except Exception:
            return None