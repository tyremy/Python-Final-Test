from identified_object import IdentifiedObject


class Competition(IdentifiedObject):

    def __init__(self, oid, teams, location, date_time=None):
        super().__init__(oid)
        self._teams_competing = teams
        self.location = location
        self.date_time = date_time

    @property
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        emails = []
        for team in self._teams_competing:
            members = team.members
            for member in members:
                if member.email not in emails:
                    emails.append(member.email)
        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        if self.date_time is None:
            return f"Competition at {self.location} with {len(self._teams_competing)} teams"
        else:
            s1 = f"Competition at {self.location} on {self.date_time.strftime('%m/%d/%Y %H:%M')}"
            s2 = f" with {len(self._teams_competing)} teams"
            return s1 + s2
