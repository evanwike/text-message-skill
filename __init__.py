from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.parse import match_one
from twilio.rest import Client

LOGGER = getLogger(__name__)

account_sid = ''
auth_token = ''
# client = Client(account_sid, auth_token)
phone_num = ''

class TextMessage(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.numbers = {
            'evan': '',
            'cam': '',
            'dui': '',
            'max': '',
            'tondi': ''
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
