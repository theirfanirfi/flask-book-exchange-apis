from application import db

def commit_changes_to_db(func):
    def save_to_db(s, form):
        obj = func(s, form)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            print(e)
            return False
    return save_to_db


def save_to_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        return obj
    except Exception as e:
        print(e)
        return False
