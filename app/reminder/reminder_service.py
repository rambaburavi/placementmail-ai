from datetime import timedelta


class ReminderService:

    OFFSETS = [
        ("24", timedelta(hours=24)),
        ("12", timedelta(hours=12)),
        ("6", timedelta(hours=6)),
        ("1", timedelta(hours=1)),
        ("15", timedelta(minutes=15)),
    ]

    def get_reminder_times(self, deadline):

        reminders = []

        for label, delta in self.OFFSETS:

            reminders.append(
                (
                    label,
                    deadline - delta,
                )
            )

        return reminders