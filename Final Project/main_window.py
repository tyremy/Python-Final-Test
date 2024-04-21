import sys
from PyQt5.QtWidgets import QFileDialog, QDialog
from league import League
from league_database import LeagueDatabase
from PyQt5 import uic, QtWidgets
from league_editor import LeagueEditor
from utility_methods import UtilityMethods

Ui_MainWindow, QtBaseClass = uic.loadUiType('./User Interfaces/main_window.ui')


class MainWindow(QtBaseClass, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.database = LeagueDatabase()
        self.add_league_button.clicked.connect(self.add_new_league)
        self.delete_league_button.clicked.connect(self.delete_league)
        self.edit_league_button.clicked.connect(self.edit_league)
        self.load_database_button.clicked.connect(self.load_database)
        self.save_database_button.clicked.connect(self.save_database)

    def add_new_league(self):
        """Adds a new league to the database"""
        # Get league name from user input and check if it is valid
        league_name = self.add_league_line_edit.text()
        if league_name == '' or league_name in [league.name for league in self.database.leagues]:
            return UtilityMethods.warn("Invalid League Value", "League name cannot be blank and cannot be duplicate")

        # Create new league object and add to league database
        league_oid = self.database.next_oid()
        league_to_add = League(league_oid, league_name)
        self.database.add_league(league_to_add)
        self.add_league_line_edit.clear()
        UtilityMethods.update_ui(self.league_list, self.database.leagues)

    def delete_league(self):
        """Deletes selected league from the league database"""
        # check if league is selected
        league_row = UtilityMethods.get_selected_item(self.league_list, self.database.leagues)
        if league_row == -1:
            return UtilityMethods.warn("Select League", "You must select a league from the list")

        # set league to be removed and prompt user to confirm
        league_to_remove = self.database.leagues[league_row]
        league_name = league_to_remove.name
        UtilityMethods.confirm_deletion(self, league_to_remove, league_name, self.database.leagues, self.league_list)

    def edit_league(self):
        """Opens the League Editor dialog for the selected league"""
        # check if a league is selected
        league_row = UtilityMethods.get_selected_item(self.league_list, self.database.leagues)
        if league_row == -1:
            return UtilityMethods.warn("Select League", "You must select a league from the list")

        # Open League Editor Dialogue
        league_to_edit = self.database.leagues[league_row]
        dialog = LeagueEditor(league_to_edit, self.database)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.update_teams(league_to_edit)
            UtilityMethods.update_ui(self.league_list, self.database.leagues)
        else:
            pass

    def load_database(self):
        """Loads league database from a file"""
        dialog = QFileDialog()
        dialog.setDirectory("./Saved League Databases")
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            self.database = LeagueDatabase.load(file_name)
            UtilityMethods.update_ui(self.league_list, self.database.leagues)
        else:
            pass

    def save_database(self):
        """Saves league database to a file"""
        dialog = QFileDialog()
        file_name = dialog.getSaveFileName(self, 'Save Database', './Saved League Databases')
        if file_name[0] != '':
            self.database.save(file_name[0])
        else:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
