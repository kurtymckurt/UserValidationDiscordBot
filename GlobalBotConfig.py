from tinydb import TinyDB, Query
from datetime import datetime


def is_user_old(created_at):
    dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
    now = int(dt_obj.timestamp())
    return now - created_at > 86400


class GlobalBotConfig:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = GlobalBotConfig()
        return cls.__instance

    def __init__(self):
        self.db = TinyDB('db.json')
        self.config_table = self.db.table("config")
        self.user_table = self.db.table("user")

    def delete_guild(self, guild_id):
        server_config = Query()
        self.config_table.remove(server_config.guild_id == guild_id)

    def delete_expired_users(self):
        user = Query()
        users = self.user_table.all()
        for u in users:
            if is_user_old(u['created_at']):
                self.user_table.remove((user.guild_id == u['guild_id']) & (user.user_id == u['user_id']))

    def exists_guild_config(self, guild_id):
        server_config = Query()
        return len(self.config_table.search(server_config.guild_id == guild_id)) > 0

    def create_guild_config(self, guild_id):
        if not self.exists_guild_config(guild_id):
            self.config_table.insert({'server_name': 'My Discord', 'guild_id': guild_id,
                                      'role': 'new_user', 'channel': 'guest', 'server_rules': 'No Rules have been set'})

    def add_server_name(self, guild_id, name):
        server_config = Query()
        self.config_table.update({'server_name': name}, server_config.guild_id == guild_id)

    def add_role(self, guild_id, role):
        server_config = Query()
        self.config_table.update({'role': role}, server_config.guild_id == guild_id)

    def add_channel(self, guild_id, channel):
        server_config = Query()
        self.config_table.update({'channel': channel}, server_config.guild_id == guild_id)

    def add_rules(self, guild_id, rules):
        server_config = Query()
        self.config_table.update({'server_rules': rules}, server_config.guild_id == guild_id)

    def get_server_name(self, guild_id):
        server_config = Query()
        return self.config_table.search(server_config.guild_id == guild_id)[0]['server_name']

    def get_guild_config(self, guild_id):
        server_config = Query()
        return self.config_table.search(server_config.guild_id == guild_id)[0]

    def add_user_code(self, guild_id, user_id, code):
        user = Query()
        dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
        created_at = int(dt_obj.timestamp())
        if len(self.user_table.search((user.guild_id == guild_id) & (user.user_id == user_id))) == 0:
            self.user_table.insert({'guild_id': guild_id, 'user_id': user_id, 'code': code, 'created_at': created_at})
        else:
            self.user_table.update({'code': code, 'created_at': created_at},(user.guild_id == guild_id) & (user.user_id == user_id))

    def get_user_code(self, guild_id, user_id):
        user = Query()
        return self.user_table.search((user.guild_id == guild_id) & (user.user_id == user_id))[0]['code']

    def exists_user_code(self, guild_id, user_id):
        user = Query()
        return len(self.user_table.search((user.guild_id == guild_id) & (user.user_id == user_id))) > 0

    def delete_user_code(self, guild_id, user_id):
        user = Query()
        return self.user_table.remove((user.guild_id == guild_id) & (user.user_id == user_id))
