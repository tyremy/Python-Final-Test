from fake_emailer import FakeEmailer
from team_member import TeamMember
from identified_object import IdentifiedObject

import unittest


class TeamMemberTest(unittest.TestCase):
    def test_if_team_member_is_identified_object(self):
        """Test if team member is instance of identified object"""
        tm1 = TeamMember(123, "Tyler", "tzr0043@aub.edu")

        self.assertTrue(isinstance(tm1, IdentifiedObject))

    def test_if_team_member_email_and_name_can_change(self):
        """Test is name and email can be accessed and changed"""
        tm1 = TeamMember(123, "Tyler", "tzr0043@aub.edu")
        tm1.name = "James"
        tm1.email = "test@gmail.com"

        self.assertEqual("James", tm1.name)
        self.assertEqual("test@gmail.com", tm1.email)

    def test_if_team_member_email_is_sent(self):
        """Test if send email sends email to specified team member with correct content"""
        tm1 = TeamMember(123, "Tyler", "tzr0043@aub.edu")
        fake_emailer = FakeEmailer()
        tm1.send_email(fake_emailer, "notice", "test")

        self.assertEqual("notice", fake_emailer.subject)
        self.assertEqual("test", fake_emailer.message)
        self.assertEqual(["tzr0043@aub.edu"], fake_emailer.recipients)

    def test_if_team_member_string_is_correct(self):
        """Test if override of str() returns team member in format of Name <Email>"""
        tm1 = TeamMember(123, "Name", "email")
        tm2 = TeamMember(456, "Jim Smith", "jmsith@yahoo.com")

        self.assertEqual("Name<email>", str(tm1))
        self.assertEqual("Jim Smith<jmsith@yahoo.com>", str(tm2))


if __name__ == '__main__':
    unittest.main()
