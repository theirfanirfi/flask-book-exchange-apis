from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for, request
from application.Team.TeamForm import TeamForm
from application.Team.Team import Team
from flask_login import login_user, logout_user, login_required, current_user
from application.API.Factory.BLFactory import BF


class TeamView(FlaskView):
	title = 'Team Chat'
	exclude_methods=['redirect_with_form']
	bl = Team()

	def redirect_with_form(self, form):
		return render_template("cpanel/team_account.html",title=self.title, form=form)

	def index(self):
		form = TeamForm()
		team = self.bl.get_team_account()
		form.fullname.data = team.fullname
		form.welcome_message.data = team.welcome_message
		return self.redirect_with_form(form)

	def get(self, id):
		#currently, not implemented
		pass

	def chats(self):
		team = self.bl.get_team_account()
		isFound, participants = BF.getBL("participants").get_participants(team)
		return render_template("cpanel/team_chat_board.html", participants=participants, is_chats=False)

	@route('/chat/<string:participant_id>')
	def chat(self, participant_id):
		team = self.bl.get_team_account()
		participants = BF.getBL("participants").get_participant_by_id(participant_id, team.user_id)

		if not team or not participants:
			return redirect(url_for("TeamView:chats"))

		chats = BF.getBL("messages").get_chat_messages_for_team(participants, team)
		return render_template("cpanel/team_chat_board.html",
							   participants=participants,
							   is_chats=True,
							   chats=chats)


	@route("/update", methods=['POST'])
	@login_required
	def update(self):
		user = current_user
		self.title = user.fullname
		form = TeamForm()
		if form.validate_on_submit():
			updatedTeamAccount = self.bl.update_team_account(form)
			if not updatedTeamAccount:
				flash("Error occurred while updating team account. Please try again", "error")
			else:
				flash("Team account updated successfully.", "success")
			return redirect(request.referrer)
		else:
			return render_template("cpanel/team_account.html", title=self.title, form=form)

