from datetime import datetime


class NewUser:
    def __init__(self, user_id):
        self.user_id = user_id
        dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
        self.created_at = int(dt_obj.timestamp())

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def is_old(self):
        # 86400 is one day in seconds
        return self.created_at > 86400
