import unittest

from fake_emailer import FakeEmailer
from competition import Competition
from team import Team
from datetime import datetime
from team_member import TeamMember


class CompetitionTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

        #Teams
        self.team1 = Team(100, "Tigers")
        self.team2 = Team(101, "Wildcats")

        #Members
        self.member1 = TeamMember(500, "Tyler Remy", "tzr0043@auburn.edu")
        self.member2 = TeamMember(501, "Jimmy Smith", "jsmith@auburn.edu")
        self.member3 = TeamMember(502, "Tom Jones", "tjones@auburn.edu")
        self.member4 = TeamMember(503, "Ashe Remy", "aremy@auburn.edu")

        #Assign members to Teams
        self.team1.add_member(self.member1)
        self.team1.add_member(self.member2)
        self.team2.add_member(self.member3)
        self.team2.add_member(self.member4)

        comp_date_time = datetime.strptime("03/29/2024 12:00", "%m/%d/%Y %H:%M")

        #Set up competition
        self.competition1 = Competition(1, [self.team1, self.team2], "Auburn, AL", comp_date_time)

    def test_competition_object_created(self):
        """Test to check that competition is being created and all variables are set properly"""

        teams_competing = [self.team1, self.team2]
        competition2 = Competition(2, teams_competing, "Auburn, AL")

        self.assertEqual(1, self.competition1.oid)
        self.assertEqual([self.team1, self.team2], self.competition1._teams_competing)
        self.assertEqual("Auburn, AL", self.competition1.location)
        self.assertEqual(datetime.strptime("03/29/2024 12:00", "%m/%d/%Y %H:%M"), self.competition1.date_time)
        self.assertEqual(None, competition2.date_time)

    def test_send_email_sends_email_to_correct_members(self):
        """Test that send email sends message to each member of each team in competition
            and does not send multiple emails to members that are on more than one team"""

        fake_emailer = FakeEmailer()
        members = [self.member1, self.member2, self.member3, self.member4]
        recipient_list = [member.email for member in members]

        self.competition1.send_email(fake_emailer, "Game", "Test Message")

        self.assertEqual(recipient_list, fake_emailer.recipients)
        self.assertEqual("Game", fake_emailer.subject)
        self.assertEqual("Test Message", fake_emailer.message)

        #Duplicate a member
        self.team2.add_member(self.member1)
        self.competition1.send_email(fake_emailer, "Game", "Test Message")
        self.assertEqual(recipient_list, fake_emailer.recipients)

    def test_str_override_provides_correct_formatting(self):
        """Test that override of str method returns correct formatting of competition object
            both with and without date"""

        self.competition2 = Competition(1, [self.team1, self.team2], "Auburn, AL")

        competition_string_with_date = "Competition at Auburn, AL on 03/29/2024 12:00 with 2 teams"
        competition_string_no_date = "Competition at Auburn, AL with 2 teams"

        self.assertEqual(competition_string_with_date, str(self.competition1))
        self.assertEqual(competition_string_no_date, str(self.competition2))


if __name__ == '__main__':
    unittest.main()
