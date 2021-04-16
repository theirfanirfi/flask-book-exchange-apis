from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from sqlalchemy import and_, or_


class ParticipantBL(BusinessLogic):
    def get_my_chat_participants(self, user):

        query = "SELECT chat_participants.*, " \
                "JSON_OBJECT('user_one_id', user_one.user_id, 'user_one_fullname', " \
                "user_one.fullname, 'user_one_profile_image', user_one.profile_image) as user_one, " \
                "JSON_OBJECT('user_two_id', user_two.user_id, 'user_two_fullname', user_two.fullname, " \
                "'user_two_profile_image', user_one.profile_image) as user_two, " \
                "IF(user_one.user_id="+str(user.user_id)+",true,false) as amIUserOne FROM chat_participants " \
                "LEFT JOIN users as user_one on user_one.user_id = chat_participants.user_one_id " \
                "LEFT JOIN users as user_two on user_two.user_id = chat_participants.user_two_id " \
                "WHERE user_one_id = "+str(user.user_id)+" OR user_two_id = "+str(user.user_id)
        return super().get_by_custom_query(schemaName="participants",query=query, isMany=True, isDump=True)

    def get_participant(self, user_one_id, user_two_id):
        model = MF.getModel("participants")[1]
        participants = model.query.filter(or_(and_(model.user_one_id==user_one_id, model.user_two_id==user_two_id),
                                              and_(model.user_two_id==user_one_id, model.user_one_id==user_two_id)))
        if not participants.count() > 0:
            return self.create_participants(user_one_id, user_two_id)
        return participants.first()

    def get_participant_by_id(self, p_id, user_id):
        model = MF.getModel("participants")[1]
        participants = model.query.filter(and_((model.p_id==p_id), or_(model.user_one_id==user_id, model.user_two_id==user_id)))
        if not participants.count() > 0:
            return False
        return participants.first()

    def create_participants(self, user_one_id, user_two_id):
        model = MF.getModel("participants")[0]
        model.user_one_id = user_one_id
        model.user_two_id = user_two_id

        try:
            db.session.add(model)
            db.session.commit()
            return model
        except Exception as e:
            print(e)
            return False


