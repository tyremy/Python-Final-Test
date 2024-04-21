import unittest

from duplicate_oid import DuplicateOID
from team import Team
from team_member import TeamMember
from competition import Competition
from league import League


class LeagueTests(unittest.TestCase):
    def setUp(self):
        super().setUp()

        #Member Set Up
        self.member1 = TeamMember(500, "Tyler Remy", "tzr0043@auburn.edu")
        self.member2 = TeamMember(501, "Jimmy Smith", "jsmith@auburn.edu")
        self.member3 = TeamMember(502, "Tom Jones", "tjones@auburn.edu")
        self.member4 = TeamMember(503, "Ashe Remy", "aremy@auburn.edu")
        self.member5 = TeamMember(504, "Kevin Jones", "kevin@auburn")

        #Teams Set Up
        self.team1 = Team(200, "Tigers")
        self.team2 = Team(201, "Wildcats")
        self.team3 = Team(202, "Bulldogs")
        self.team4 = Team(203, "Cougars")
        self.team1.add_member(self.member1)
        self.team1.add_member(self.member2)
        self.team2.add_member(self.member3)
        self.team2.add_member(self.member4)
        self.team3.add_member(self.member5)

        #Competitions Set Up
        self.competition1 = Competition(100, [self.team1, self.team2], "Auburn")
        self.competition2 = Competition(101, [self.team1, self.team2], "Manhattan")
        self.competition3 = Competition(102, [self.team3, self.team4], "Dallas")

        #League Set Up
        self.league1 = League(1, "Western")

    def test_league_object_created(self):
        """Test that league object is created with an oid, name, and empty lists for
            teams and competitions"""

        self.assertEqual(1, self.league1.oid)
        self.assertEqual("Western", self.league1.name)
        self.assertEqual([], self.league1.teams)
        self.assertEqual([], self.league1.competitions)

    def test_adding_team_adds_team_to_league(self):
        """Test that team can be added to league"""

        #Add team to League
        self.league1.add_team(self.team1)

        self.assertEqual([self.team1], self.league1.teams)

    def test_removal_of_team_from_league(self):
        """Test that team is removed from league if it exists else do nothing"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)

        #Remove team 1 from league
        self.league1.remove_team(self.team1)
        #Call remove team again with team1 not in teams collection
        self.league1.remove_team(self.team1)

        self.assertEqual([self.team2], self.league1.teams)

    def test_returning_team_with_specified_name(self):
        """Test that team with specified name is returned else return none"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)

        self.assertEqual(self.team1, self.league1.team_named(self.team1.name))
        self.assertEqual(self.team2, self.league1.team_named(self.team2.name))
        self.assertEqual(None, self.league1.team_named("NotATeam"))

    def test_adding_competition_adds_competition_to_league(self):
        """Test that competition can be added to league"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)
        self.league1.add_team(self.team3)
        self.league1.add_team(self.team4)

        self.league1.add_competition(self.competition1)
        self.league1.add_competition(self.competition2)

        self.assertEqual([self.competition1, self.competition2], self.league1.competitions)

    def test_teams_for_member_returns_all_correct_teams(self):
        """Test that a list of all teams for specified member are returned"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)

        #Add Member 1 to Team 2 so member 1 is a member of both team
        self.team2.add_member(self.member1)

        self.assertEqual([self.team1, self.team2], self.league1.teams_for_member(self.member1))
        self.assertEqual([self.team1], self.league1.teams_for_member(self.member2))
        self.assertEqual([self.team2], self.league1.teams_for_member(self.member3))

    def test_competitions_for_team_returns_all_correct_competitions(self):
        """Test that a list of competitions for specified team are returned"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)
        self.league1.add_team(self.team3)
        self.league1.add_team(self.team4)
        self.league1.add_competition(self.competition1)
        self.league1.add_competition(self.competition2)
        self.league1.add_competition(self.competition3)

        self.assertEqual([self.competition1, self.competition2], self.league1.competitions_for_team(self.team1))
        self.assertEqual([self.competition3], self.league1.competitions_for_team(self.team3))

    def test_competitions_for_member_returns_all_correct_competitions(self):
        """Test that a list of competitions for specified member are returned"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)

        self.league1.add_competition(self.competition1)
        self.league1.add_competition(self.competition2)

        self.assertEqual([self.competition1, self.competition2], self.league1.competitions_for_member(self.member1))

    def test_override_string_returns_properly_formatted_string(self):
        """Test that properly formatted string is returned"""

        self.league1.add_team(self.team1)
        self.league1.add_team(self.team2)
        self.league1.add_competition(self.competition1)
        self.league1.add_competition(self.competition2)

        expected_string = "Western: 2 teams, 2 competitions"

        self.assertEqual(expected_string, str(self.league1))

    def test_that_team_added_to_league_has_unique_OID(self):
        """Test that adding a team with duplicate OID raises exception"""
        with self.assertRaises(DuplicateOID):
            team1 = Team(55, "Hurricanes")
            team2 = Team(55, "Maple Leafs")
            self.league1.add_team(team1)
            self.league1.add_team(team2)

    def test_that_competition_added_to_league_has_unique_OID(self):
        """Test that adding a team with duplicate OID raises exception"""
        with self.assertRaises(DuplicateOID):
            league2 = League(2, "Eastern")
            team1 = Team(55, "Hurricanes")
            team2 = Team(56, "Maple Leafs")
            league2.add_team(team1)
            league2.add_team(team2)
            competition4 = Competition(104, [team1, team2], "Raleigh")
            competition5 = Competition(104, [team1, team2], "Toronto")
            league2.add_competition(competition4)
            league2.add_competition(competition5)

    def test_that_exception_thrown_if_team_not_in_league(self):
        """Tests that if team is added to competition but not in league, exception is thrown"""

        with self.assertRaises(ValueError):
            league2 = League(2, "Eastern")
            team1 = Team(55, "Hurricanes")
            team2 = Team(56, "Maple Leafs")
            league2.add_team(team1)
            competition6 = Competition(105, [team1, team2], "Raleigh")
            league2.add_competition(competition6)

    def test_that_remove_team_throws_error_if_team_has_competition(self):
        """Tests that if team to be removed has a competition, exception is thrown"""

        with self.assertRaises(ValueError):
            league3 = League(3, "Northern")
            team1 = Team(57, "Senators")
            team2 = Team(58, "Rangers")
            league3.add_team(team1)
            league3.add_team(team2)
            competition7 = Competition(106, [team1, team2], "Raleigh")
            league3.add_competition(competition7)
            league3.remove_team(team2)


if __name__ == '__main__':
    unittest.main()
