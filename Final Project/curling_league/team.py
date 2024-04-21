from duplicate_email import DuplicateEmail
from duplicate_oid import DuplicateOID
from identified_object import IdentifiedObject


class Team(IdentifiedObject):

    def __init__(self, oid, name):
        super().__init__(oid),
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        if any(existing_member.oid == member.oid for existing_member in self.members):
            raise DuplicateOID("OID Already Exists", member.oid)
        elif (member.email is not None and
              any(existing_member.email.lower() == member.email.lower() for existing_member in self.members)):
            raise DuplicateEmail("Email Already Exists", member.email)
        else:
            self._members.append(member)

    def member_named(self, name):
        named_member = [team_member for team_member in self._members if team_member.name == name]
        if len(named_member) == 0:
            return None
        else:
            return named_member[0]

    def remove_member(self, member):
        if member in self._members:
            self._members.remove(member)

    def send_email(self, emailer, subject, message):
        emails = [member.email for member in self._members if member.email is not None]
        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        return f"{self.name}: {len(self._members)} members"
