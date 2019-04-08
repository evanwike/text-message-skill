import os
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.parse import match_one
from twilio.rest import Client

LOGGER = getLogger(__name__)

account_sid = os.environ['TEXT_MESSAGE_SKILL_SID']
auth_token = os.environ['TEXT_MESSAGE_SKILL_AUTH']
client = Client(account_sid, auth_token)
phone_num = os.environ['TEXT_MESSAGE_SKILL_PHONE_NUM']

class TextMessage(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.numbers = {
            'evan': '+18163059565',
            'cam': '+18165166540',
            'dui': '+17145489619',
            'max': '+16263846895',
            'tondi': '+17857645832'
        }

    @intent_file_handler('send_message.intent')
    def handle_message_text(self, message):
        name = message.data.get('name')

        match, confidence = match_one(name, self.numbers)

        if confidence > 0.5:
            body = self.get_response('get_response')
        else:
            self.speak_dialog('send_error')
            return

        if body:
            msg = client.messages.create(body=body, from_=phone_num, to=self.numbers[match])
            self.speak_dialog('send_success', data={'name': match})
        else:
            self.speak_dialog('send_error', data={'name': match})

def create_skill():
    return TextMessage()
