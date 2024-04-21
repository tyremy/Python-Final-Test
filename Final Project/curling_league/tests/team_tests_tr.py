from duplicate_email import DuplicateEmail
from duplicate_oid import DuplicateOID
from team_member import TeamMember
from fake_emailer import FakeEmailer
from team import Team
import unittest


class TeamTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.team1 = Team(123, "Tigers")
        self.team_member1 = TeamMember(222, "Tyler Remy", "tzr0043@auburn.edu")
        self.team_member2 = TeamMember(223, "Jimmy Smith", "jsmith@auburn.edu")

    def test_team_starts_as_empty_list(self):
        """Test if team starts out as an empty list"""

        self.assertEqual([], self.team1._members)

    def test_if_adding_members_adds_to_list(self):
        """Test if add member method adds member to members"""

        self.team1.add_member(self.team_member1)
        self.team1.add_member(self.team_member2)

        self.assertEqual([self.team_member1, self.team_member2], self.team1._members)

    def test_if_return_named_returns_correct_member(self):
        """Test to see if correct name is returned and that none is returned if name not found"""

        self.team1.add_member(self.team_member1)
        self.team1.add_member(self.team_member2)

        self.assertEqual(self.team_member1, self.team1.member_named("Tyler Remy"))
        self.assertEqual(None, self.team1.member_named("NoName"))

    def test_remove_member_removes_specified_member(self):
        """Test to see if correct member is removed and nothing happens if member is not in list"""
        team_member3 = TeamMember(224, "Not A Real Person", "test@yahoo.com")
        self.team1.add_member(self.team_member1)
        self.team1.add_member(self.team_member2)

        #Base -> Members contains member 1 and 2
        self.assertEqual([self.team_member1, self.team_member2], self.team1._members)

        #Removing member not in members list has no effect
        self.team1.remove_member(team_member3)
        self.assertEqual([self.team_member1, self.team_member2], self.team1._members)

        #Removing member 2 leaves only member 1
        self.team1.remove_member(self.team_member2)
        self.assertEqual([self.team_member1], self.team1._members)

        #Removing member 1 results in blank list
        self.team1.remove_member(self.team_member1)
        self.assertEqual([], self.team1._members)

        #Calling remove against blank list doesn't error out
        self.team1.remove_member(self.team_member1)
        self.assertEqual([], self.team1._members)

    def test_send_email_that_emails_are_sent(self):
        """Test to see if emails are sent to all members of team except those with None for email"""
        fake_emailer = FakeEmailer()
        team_member3 = TeamMember(225, "Tom Jones", None)
        self.team1.add_member(self.team_member1)
        self.team1.add_member(self.team_member2)
        self.team1.add_member(team_member3)

        self.team1.send_email(fake_emailer, "Game", "Test Message")

        self.assertEqual([self.team_member1.email, self.team_member2.email], fake_emailer.recipients)
        self.assertEqual("Game", fake_emailer.subject)
        self.assertEqual("Test Message", fake_emailer.message)

    def test_override_str_returns_proper_format(self):
        """Test to make sure overridden str method returns proper format"""
        self.team1.add_member(self.team_member1)
        self.team1.add_member(self.team_member2)
        team2 = Team(124, "Wildcats")

        self.assertEqual("Tigers: 2 members", str(self.team1))
        self.assertEqual("Wildcats: 0 members", str(team2))

    def test_if_member_added_email_is_unique(self):
        """Test that adding a member with duplicate email (not case-sensitive) raises exception"""
        with self.assertRaises(DuplicateEmail):
            tm1 = TeamMember(123, "Tyler", "tzr0043@aub.edu")
            tm2 = TeamMember(456, "James", "TZR0043@aub.edu")
            self.team1.add_member(tm1)
            self.team1.add_member(tm2)

    def test_if_member_added_oid_is_unique(self):
        """Test that adding a member with duplicate email raises exception"""
        with self.assertRaises(DuplicateOID):
            tm1 = TeamMember(123, "Tyler", "tzr0043@aub.edu")
            tm2 = TeamMember(123, "James", "jsmith@aub.edu")
            self.team1.add_member(tm1)
            self.team1.add_member(tm2)


if __name__ == '__main__':
    unittest.main()
