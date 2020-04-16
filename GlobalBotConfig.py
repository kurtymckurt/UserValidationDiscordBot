from NewUser import NewUser


class GlobalBotConfig:
    def __init__(self):
        self.dict_of_guild_to_user_code_dict = {}
        self.dict_of_guild_to_config = {}
        self.dict_of_guild_to_server_name = {}

    def delete_guild(self, guild_id):
        del self.dict_of_guild_to_user_code_dict[guild_id]
        del self.dict_of_guild_to_config[guild_id]
        del self.dict_of_guild_to_server_name[guild_id]

    def delete_expired_users(self):
        for guild_id in self.dict_of_guild_to_user_code_dict:
            for new_user in self.dict_of_guild_to_user_code_dict[guild_id]:
                if new_user.is_old():
                    del self.dict_of_guild_to_user_code_dict[guild_id][new_user]

    def delete_all_users_code(self):
        for guild_id in self.dict_of_guild_to_user_code_dict:
            for new_user in self.dict_of_guild_to_user_code_dict[guild_id]:
                del self.dict_of_guild_to_user_code_dict[guild_id][new_user]

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

    def add_user_code(self, guild_id, user_id, code):
        if guild_id not in self.dict_of_guild_to_user_code_dict:
            self.dict_of_guild_to_user_code_dict[guild_id] = {}

        self.dict_of_guild_to_user_code_dict[guild_id][NewUser(user_id)] = code

    def get_user_code(self, guild_id, user_id):
        return self.dict_of_guild_to_user_code_dict[guild_id][NewUser(user_id)]

    def exists_user_code(self, guild_id, user_id):
        return NewUser(user_id) in self.dict_of_guild_to_user_code_dict[guild_id]

    def delete_user_code(self, guild_id, user_id):
        del self.dict_of_guild_to_user_code_dict[guild_id][NewUser(user_id)]
