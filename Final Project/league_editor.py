import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
from league import League
from league_database import LeagueDatabase
from PyQt5 import uic, QtWidgets
from team import Team
from team_editor import TeamEditor
from utility_methods import UtilityMethods

Ui_MainWindow, QtBaseClass = uic.loadUiType('./User Interfaces/league_editor.ui')


class LeagueEditor(QtBaseClass, Ui_MainWindow):
    def __init__(self, league=None, database=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # if league is not none, set title, and set up temp teams array and fill with league teams
        self.temp_teams = []
        if league is not None:
            self.league = league
            self.list_title.setText(f"List of teams in league: {league.name}")
            for team in league.teams:
                self.temp_teams.append(team)
        if database is not None:
            self.database = database
        UtilityMethods.update_ui(self.teams_list, self.temp_teams)
        self.add_team_button.clicked.connect(self.add_new_team)
        self.delete_team_button.clicked.connect(self.delete_team)
        self.import_teams_button.clicked.connect(self.import_league)
        self.export_teams_button.clicked.connect(self.export_league)
        self.edit_team_button.clicked.connect(self.edit_team)

    def add_new_team(self):
        """Creates new team and adds team to temp list instead of league so that if user cancels dialogue,
            the league will remain unedited"""
        # get team name from input and check is empty or team already exists
        team_name = self.add_team_line_edit.text()
        if team_name == '' or team_name in [team.name for team in self.temp_teams]:
            return UtilityMethods.warn("Invalid Team Value", "Team name cannot be blank and cannot be duplicate")

        # create team object
        team_oid = self.database.next_oid()
        team_to_add = Team(team_oid, team_name)

        # add teams to temp list, clear line edit, and update ui
        self.temp_teams.append(team_to_add)
        self.add_team_line_edit.clear()
        UtilityMethods.update_ui(self.teams_list, self.temp_teams)

    def delete_team(self):
        # Get Team Index
        team_row = UtilityMethods.get_selected_item(self.teams_list, self.temp_teams)
        if team_row == -1:
            return UtilityMethods.warn("Select Team", "You must select a team from the list")

        team_to_remove = self.temp_teams[team_row]
        team_name = team_to_remove.name
        UtilityMethods.confirm_deletion(self, team_to_remove, team_name, self.temp_teams, self.teams_list)

    def import_league(self):
        """Loads league information from a file -- Creates temp league to avoid adding teams directly to league
        in order to give user flexibility to cancel league modification even after importing"""
        tmp_league = League(99999, "tmp")
        dialog = QFileDialog()
        dialog.setDirectory("./Saved Leagues")
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            LeagueDatabase.import_league_teams(self.database, tmp_league, file_name)

            # If imported team isn't already in temp array, add to array
            for team in tmp_league.teams:
                if team.name in [team.name for team in self.temp_teams]:
                    pass
                else:
                    self.temp_teams.append(team)
            UtilityMethods.update_ui(self.teams_list, self.temp_teams)
        else:
            pass

    def export_league(self):
        """Exports league information to a file -- Prompts user to save first in order to preserve any changes
        not yet saved to league so user does not have save and close league editor and re-open to export teams"""
        # Prompt user to "save" league
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Question)
        dialog.setWindowTitle('Save League')
        dialog.setText("Save Required to Export")
        dialog.setInformativeText("League must first be saved to export, would you like to save changes and export?")
        confirm_button = dialog.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
        dialog.exec()

        # If saved, export league
        if dialog.clickedButton() == confirm_button:
            self.update_teams(self.league)
            export_dialog = QFileDialog()
            file_name = export_dialog.getSaveFileName(self, 'Save League', './Saved Leagues')
            if file_name[0] != '':
                LeagueDatabase.export_league_teams(self.database, self.league, file_name[0])
            else:
                pass
        else:
            pass

    def edit_team(self):
        """Opens the Team Editor dialog for the selected team"""
        # Get selected Team Index
        team_row = UtilityMethods.get_selected_item(self.teams_list, self.temp_teams)
        if team_row == -1:
            return UtilityMethods.warn("Select Team", "You must select a team from the list")

        # Open Team Editor Dialogue
        team_to_edit = self.temp_teams[team_row]
        dialog = TeamEditor(team_to_edit, self.league, self.database)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.update_roster(team_to_edit)
            UtilityMethods.update_ui(self.teams_list, self.temp_teams)
        else:
            pass

    def update_teams(self, league):
        """Updates the leagues teams from temp list -- Only called if user clicks save button"""
        # Add team to league if in temp array and not in league
        for team in self.temp_teams:
            if team not in league.teams:
                league.add_team(team)

        # Make array of deleted teams and remove from League
        to_remove = [team for team in league.teams if team not in self.temp_teams]

        # Delete each team in to_remove from League
        for team in to_remove:
            league.remove_team(team)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec_())
