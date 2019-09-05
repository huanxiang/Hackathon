import time
from datetime import datetime, date, timedelta
from config import get_env


class Actions:
    def __init__(self, slackhelper, user_info=None):
        self.user_info = user_info
        self.slackhelper = slackhelper

    def help(self):
        return {
            'text': 'Available Commands: \n '
                    '\n `/hackabot help` \n This help information \n \n Hackabot Ver: 1.0'}
