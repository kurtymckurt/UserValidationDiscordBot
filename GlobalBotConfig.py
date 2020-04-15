class GlobalBotConfig:
    def __init__(self):
        self.dict_of_user_to_code = {}
        self.dict_of_guild_to_config = {}
        self.dict_of_guild_to_server_name = {}

    def add_server_name(self, guild_id, name):
        self.dict_of_guild_to_server_name[guild_id] = name

    def get_server_name(self, guild_id):
        return self.dict_of_guild_to_server_name[guild_id]

    def exists_server_name(self, guild_id):
        return guild_id in self.dict_of_guild_to_server_name

    def add_guild_config(self, guild_id, server_channel_role_config):
        self.dict_of_guild_to_config[guild_id] = server_channel_role_config

    def get_guild_config(self, guild_id):
        return self.dict_of_guild_to_config[guild_id]

    def exists_guild_config(self, guild_id):
        return guild_id in self.dict_of_guild_to_config

    def add_user_code(self, user_id, code):
        self.dict_of_user_to_code[user_id] = code

    def get_user_code(self, user_id):
        return self.dict_of_user_to_code[user_id]

    def exists_user_code(self, user_id):
        return user_id in self.dict_of_user_to_code

    def delete_user_code(self, user_id):
        del self.dict_of_user_to_code[user_id]
