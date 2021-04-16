from application import db
from application.API.Factory.SchemaFactory import SF
from application.API.Factory.ModelFactory import MF
from application.API.BusinessLogic.BusinessLogic import BusinessLogic
from sqlalchemy import and_, or_


class ParticipantBL(BusinessLogic):
    def get_participant(self, user_one_id, user_two_id):
        model = MF.getModel("participants")[1]
        participants = model.query.filter(or_(and_(model.user_one_id==user_one_id, model.user_two_id==user_two_id),
                                              and_(model.user_two_id==user_one_id, model.user_one_id==user_two_id)))
        if not participants.count() > 0:
            return self.create_participants(user_one_id, user_two_id)
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


