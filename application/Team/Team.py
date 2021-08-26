from application.Models.models import User
from application import db
from application.Team.Utils import commit_changes_to_db, save_to_db

class Team:

    def get_team_account(self):
        team = User.query.filter_by(is_team=1, is_admin=1)
        if not team.count() > 0:
            team = User.query.filter_by(is_admin=1)
            if not team.count() > 0:
                return False
            team = team.first()
            team.is_team = 1
            return save_to_db(team)
        else:
            return team.first() if team.count() > 0 else False

    @commit_changes_to_db
    def update_team_account(self, form):
        team = self.get_team_account()
        if not team or form is None:
            return False

        team.fullname = form.fullname.data
        team.welcome_message = form.welcome_message.data
        return team










