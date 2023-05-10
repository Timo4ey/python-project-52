from django.utils.translation import gettext_lazy as _
import json
import os
from pathlib import Path


class DataTrans:
    def __init__(self):
        self.wrong_login_message = None
        self.logout_message = None
        self.login_message = None
        self.password_text = None
        self.username_text = None
        self.get_text_from_json()

    def get_text_from_json(self):
        with open(os.path.join(Path(__file__).resolve().parent,
                               'trans_conf.json'), 'r') as f:
            data = json.load(f)
            self.username_text = _(data.get('username_text', ''))
            self.password_text = _(data.get('password_text', ''))
            self.login_message = _(data.get('login_message', ''))
            self.logout_message = _(data.get('logout_message', ''))
            self.wrong_login_message = _(data.get('wrong_login_message', ''))
