import yagmail
import keyring


class Emailer:

    sender_address = "tzr0043pyth@gmail.com"
    _pass = keyring.get_password("fakegmail2", sender_address)
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):

        yag = yagmail.SMTP(self.sender_address, self._pass)
        yag.send(to=recipients, subject=subject, contents=message)

        for recipient in recipients:
            print(f"Sending mail to: {recipient}")


if __name__ == "__main__":
    rec = ["tyremy53@gmail.com"]
    emailer = Emailer.instance()
    emailer.send_plain_email(rec, "Hello There", "General Kenobi")
