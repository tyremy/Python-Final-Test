import csv
import os
import pickle
from league import League
from team import Team
from team_member import TeamMember


class LeagueDatabase:
    _sole_instance = None

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as f:
                return pickle.load(f)
        except IOError:
            print("Error Encountered Opening and Reading File - Loading Backup")
            backup_name = file_name + ".backup"
            try:
                with open(backup_name, mode="rb") as f:
                    return pickle.load(f)
            except IOError:
                print("Unable to Read Backup")

    @property
    def leagues(self):
        return self._leagues

    def add_league(self, league):
        self.leagues.append(league)

    def remove_league(self, league):
        self.leagues.remove(league)

    def league_named(self, name):
        existing_leagues = [league for league in self.leagues if league.name == name]
        if existing_leagues:
            return existing_leagues[0]
        else:
            return None

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        if os.path.isfile(file_name):
            # Create Backup
            backup_name = file_name + '.backup'
            os.replace(file_name, backup_name)

        # Create File
        with open(file_name, mode="wb") as f:
            pickle.dump(self, f)

    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, mode='r', encoding="utf-8") as f:
                reader = csv.reader(f)
                # Skip Headers
                next(reader, None)

                # List of teams names to avoid duplicates
                teams_names = []
                for row in reader:

                    # Create Teams and Add to League
                    if row[0] not in teams_names:
                        teams_names.append(row[0])
                        team_to_create = Team(self.next_oid(), row[0])
                        league.add_team(team_to_create)

                    # Create and add team members
                    new_member = TeamMember(self.next_oid(), row[1], row[2])
                    team_for_member = league.team_named(row[0])
                    team_for_member.add_member(new_member)

        except FileNotFoundError:
            print("Error: File not found")

    def export_league_teams(self, league, file_name):
        try:
            with open(file_name, mode='w', encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Team Name", "Member Name", "Member Email"])
                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])

        except IOError:
            print("Error Writing to CSV")


if __name__ == "__main__":
    ldb = LeagueDatabase.instance()
    l1 = League(LeagueDatabase.next_oid(ldb), "EASTERN")
    l2 = League(LeagueDatabase.next_oid(ldb), "WESTERN")

    ldb.add_league(l1)
    ldb.add_league(l2)
    ldb.import_league_teams(l1, '../Saved Leagues/Manual2.csv')
    ldb.export_league_teams(l1, '../Saved Leagues/Manual3.csv')
