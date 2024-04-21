from duplicate_oid import DuplicateOID
from identified_object import IdentifiedObject


class League(IdentifiedObject):

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        if any(existing_team.oid == team.oid for existing_team in self.teams):
            raise DuplicateOID("OID Already Exists", team.oid)
        elif team.name in [team.name for team in self._teams]:
            pass
        else:
            self._teams.append(team)

    def remove_team(self, team):
        if self.competitions_for_team(team):
            raise ValueError()
        elif team in self.teams:
            self._teams.remove(team)

    def team_named(self, team_name):
        for team in self._teams:
            if team.name == team_name:
                return team
        else:
            return None

    def add_competition(self, competition):
        if any(existing_comp.oid == competition.oid for existing_comp in self.competitions):
            raise DuplicateOID("OID Already Exists", competition.oid)
        elif (competition.teams_competing != [] and
              (competition.teams_competing[0] not in self.teams or competition.teams_competing[1] not in self.teams)):
            raise ValueError()
        else:
            self._competitions.append(competition)

    def teams_for_member(self, member):
        return [team for team in self._teams if member in team.members]

    def competitions_for_team(self, team):
        return [competition for competition in self._competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        member_competitions = []
        for competition in self._competitions:
            for team in competition.teams_competing:
                if member in team.members and competition not in member_competitions:
                    member_competitions.append(competition)

        return member_competitions

    def __str__(self):
        return f"{self.name}: {len(self._teams)} teams, {len(self._competitions)} competitions"
