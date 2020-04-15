class ServerChannelRoleConfig:
    def __init__(self, channel, role):
        self.channel = channel
        self.role = role

    def __str__(self):
        return f'[channel: {self.channel}, role: {self.role}]'
