from flask_classful import FlaskView, route
from flask import render_template, flash, redirect, url_for, request, jsonify
from application.Team.TeamForm import TeamForm, SendTeamMessageForm
from application.Team.Team import Team
from flask_login import login_user, logout_user, login_required, current_user
from application.API.Factory.BLFactory import BF


class TeamView(FlaskView):
	title = 'Team Chat'
	exclude_methods=['redirect_with_form']
	bl = Team()

	def redirect_with_form(self, form, tform):
		return render_template("cpanel/team_account.html",title=self.title, form=form, tform=tform)

	def index(self):
		form = TeamForm()
		team = self.bl.get_team_account()
		form.fullname.data = team.fullname
		form.welcome_message.data = team.welcome_message

		team_message_form = SendTeamMessageForm()
		return self.redirect_with_form(form, team_message_form)

	def get(self, id):
		#currently, not implemented
		pass

	def chats(self):
		team = self.bl.get_team_account()
		isFound, participants = BF.getBL("participants").get_participants(team)
		participant_list = list()
		for p in participants:
			participant_dict = dict()
			participant_dict.update({
				"participant": p,
				"un_read_messages": BF.getBL("messages").get_unread_messages_count_for_participant(p.p_id)
			})
			participant_list.append(participant_dict)

		return render_template("cpanel/team_chat_board.html", participants=participant_list, is_chats=False)

	@route('/chat/<string:participant_id>')
	def chat(self, participant_id):
		team = self.bl.get_team_account()
		isFound, participants = BF.getBL("participants").get_participants(team)

		participant = BF.getBL("participants").get_participant_by_id(participant_id, team.user_id)

		if not team or not participants:
			return redirect(url_for("TeamView:chats"))

		isFound, chats = BF.getBL("messages").get_chat_messages_for_team(participant, team)

		participant_list = list()
		for p in participants:
			participant_dict = dict()
			participant_dict.update({
				"participant": p,
				"un_read_messages": BF.getBL("messages").get_unread_messages_count_for_participant(p.p_id)
			})
			participant_list.append(participant_dict)

		BF.getBL("messages").make_messages_read_for_user(team.user_id)

		return render_template("cpanel/team_chat_board.html",
							   participants=participant_list,
							   is_chats=True,
							   chats=chats,
							   participant=participant)

	@route('/get_messages/<string:p_id>')
	def get_messages(self, p_id):
		if not p_id:
			return jsonify({"isError": True, "isFound": False})

		team = self.bl.get_team_account()
		participant = BF.getBL("participants").get_participant_by_id(p_id, team.user_id)
		if not participant or not team:
			return jsonify({"isError": True, "isFound": False})

		isFound, chats = BF.getBL("messages").get_chat_messages_for_team(participant, team, isDump=True)
		messages = ""
		for c in chats:
			if c['amISender'] == 1:
				print('sender')
				messages += '<div class="media w-50 mb-3">'
				messages += '<div class="media-body ml-3">'
				messages += '<div class="bg-light rounded py-2 px-3 mb-2">'
				messages += '<p class="text-small mb-0 text-muted">'+ c['message_text']+'</p>'
				messages += '</div>'
				messages += '<p class="small text-muted">'+c['created_at']+'</p>'
				messages += '</div>'
				messages += '</div>'
			else:
				print('receiver')
				messages += '<div class="media w-50 ml-auto mb-3">'
				messages += '<div class="media-body">'
				messages += '<div class="bg-primary rounded py-2 px-3 mb-2">'
				messages += '<p class="text-small mb-0 text-white">'+ c['message_text']+'</p>'
				messages += '</div>'
				messages += '<p class="small text-muted">'+c['created_at']+'</p>'
				messages += '</div>'
				messages += '</div>'

		return jsonify({"isError": False, "isFound": isFound, "chats": messages})

	@route('/send_message/<string:p_id>')
	def send_message(self, p_id):
		if not p_id:
			return jsonify({"isError": True, "isFound": False, "isSent": False,})

		team = self.bl.get_team_account()
		participant = BF.getBL("participants").get_participant_by_id(p_id, team.user_id)
		if not participant or not team:
			return jsonify({"isError": True, "isFound": False, "isSent": False})

		message = request.args.get('msg')
		sender_id = team.user_id
		receiver_id = participant.user_one_id if not participant.user_one_id == team.user_id else participant.user_two_id

		msg = BF.getBL("message").create_chat_message(sender_id, receiver_id, message, p_id)
		messages = ""
		if msg:
			messages += '<div class="media w-50 mb-3">'
			messages += '<div class="media-body ml-3">'
			messages += '<div class="bg-light rounded py-2 px-3 mb-2">'
			messages += '<p class="text-small mb-0 text-muted">' + msg.message_text + '</p>'
			messages += '</div>'
			messages += '<p class="small text-muted">' + msg.created_at+ '</p>'
			messages += '</div>'
			messages += '</div>'
			return jsonify({"isError": False, "isSent": True, "chats": messages})
		else:
			return jsonify({"isError": False, "isSent": False, "chats": messages})

	@route("/send_team_message", methods=['POST'])
	@login_required
	def send_team_message(self):
		tform = SendTeamMessageForm()
		team = self.bl.get_team_account()
		if tform.validate_on_submit():
			participants = BF.getBL("participant").get_all_participants_for_user(team.user_id)
			if not participants:
				pass

			error_counter = 0
			for p in participants:
				receiver_id = p.user_one_id if not p.user_one_id == team.user_id else p.user_two_id
				sent_message = BF.getBL("messages").create_chat_message(team.user_id, receiver_id, tform.send_message.data, p.p_id)
				if sent_message:
					error_counter += 1

			if error_counter == 0:
				flash("Error occurred while sending messages. Please try again", "error")
				return redirect(request.referrer)

			flash(str(error_counter)+ " message(s) sent.","success")
			return redirect(request.referrer)

		else:
			form = TeamForm()
			form.fullname.data = team.fullname
			form.welcome_message.data = team.welcome_message
			return self.redirect_with_form(form, tform)

	@route('/get_unread_message_count')
	def get_unread_message_count(self):
		team = self.bl.get_team_account()
		count =  BF.getBL("message").get_unread_messages_count_for_user(team.user_id)
		return str(count)

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

