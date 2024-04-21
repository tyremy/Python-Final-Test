import sys
from PyQt5 import uic, QtWidgets
from team_member import TeamMember
from utility_methods import UtilityMethods

Ui_MainWindow, QtBaseClass = uic.loadUiType('./User Interfaces/team_editor.ui')


class TeamEditor(QtBaseClass, Ui_MainWindow):
    def __init__(self, team=None, league=None, database=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # if league is not none, set title, and set up temp teams array and fill with league team
        self.temp_members = []
        if team is not None:
            self.team = team
            self.list_title.setText(f"Members on Team: {team.name}")
            for member in team.members:
                self.temp_members.append(member)
        if league is not None:
            self.league = league
        if database is not None:
            self.database = database
        UtilityMethods.update_ui(self.member_list, self.temp_members)
        self.add_member_button.clicked.connect(self.add_new_member)
        self.delete_member_button.clicked.connect(self.delete_member)
        self.update_member_button.clicked.connect(self.update_member)

    def add_new_member(self):
        """Creates new member and adds member to temp list instead of team so that if user cancels dialogue,
            the team will remain unedited"""
        # get member name and email from input and check is empty or member already exists
        member_name = self.add_member_name_line_edit.text()
        member_email = self.add_member_email_line_edit.text()
        if (member_name == ''
                or member_name in [member.name for member in self.temp_members]):
            return UtilityMethods.warn("Invalid Member Name", "Member name cannot be blank and cannot be duplicate")
        elif member_email in [member.email for member in self.temp_members]:
            return UtilityMethods.warn("Invalid Member Email", "Member Email cannot be duplicate")

        # create member object
        member_oid = self.database.next_oid()
        member_to_add = TeamMember(member_oid, member_name, member_email)

        # add member to temp list, clear line edit, and update ui
        self.temp_members.append(member_to_add)
        self.add_member_name_line_edit.clear()
        self.add_member_email_line_edit.clear()
        UtilityMethods.update_ui(self.member_list, self.temp_members)

    def delete_member(self):
        """Deletes member from temp list"""
        # Get member index
        member_row = UtilityMethods.get_selected_item(self.member_list, self.temp_members)
        if member_row == -1:
            return UtilityMethods.warn("Select Member", "You must select a member from the list")

        # Remove selected member from team
        member_to_remove = self.temp_members[member_row]
        member_name = member_to_remove.name
        UtilityMethods.confirm_deletion(self, member_to_remove, member_name, self.temp_members, self.member_list)

    def update_member(self):
        # Get member index
        member_row = UtilityMethods.get_selected_item(self.member_list, self.temp_members)
        if member_row == -1:
            return UtilityMethods.warn("Select Member", "You must select a member from the list")

        # Pop selected member from list
        member_to_update = self.temp_members.pop(member_row)

        # Get new member information and check for errors - re-insert member and clear fields if error
        new_name = self.update_member_name_line_edit.text()
        new_email = self.update_member_email_line_edit.text()
        if (new_name == ''
                or new_name in [member.name for member in self.temp_members]):
            self.temp_members.insert(member_row, member_to_update)
            return UtilityMethods.warn("Invalid Member Name", "Member name cannot be blank and cannot be duplicate")
        elif new_email in [member.email for member in self.temp_members]:
            self.temp_members.insert(member_row, member_to_update)
            return UtilityMethods.warn("Invalid Member Email", "Member Email cannot be duplicate")

        # Modify member object, insert back into array and update ui
        member_to_update.name = new_name
        member_to_update.email = new_email
        self.temp_members.insert(member_row, member_to_update)
        self.update_member_name_line_edit.clear()
        self.update_member_email_line_edit.clear()
        UtilityMethods.update_ui(self.member_list, self.temp_members)

    def update_roster(self, team):
        """Updates the teams members from temp list -- Only called if user clicks save button"""
        # Add member to team if in temp array and not on team
        for member in self.temp_members:
            if member not in team.members:
                team.add_member(member)

        # Make array of deleted members and remove from team
        to_remove = [member for member in team.members if member not in self.temp_members]

        # Delete each team in to_remove from League
        for member in to_remove:
            team.remove_member(member)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec_())
