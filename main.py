from tornado import ioloop
import hangups
from hangups.notify import Notifier

class chat(object):

    def __init__(self):
        try:
            cookies = hangups.get_auth_stdin('c.txt')
        except hangups.GoogleAuthError as e:
            print('Login failer ({})'.format(e))
            sys.exit(1)
        
        self._client = hangups.Client(cookies)
        self._client.on_connect.add_observer(self._on_connect)
        self._client.on_disconnect.add_observer(self._on_disconnect)
        self._client.on_message.add_observer(self._on_message)

        ioloop.IOLoop.instance().run_sync(self._client.connect)
        iploop.IOLoop.instance().start()

    def _on_connect(self):
        self._conv_list = hangups.ConversationList(self._client)
        self._user_list = hangups.UserList(self._client)
        self._notifier = Notifier(self._client, self._conv_list)

    def _on_message(self, chat_message):
        conv = hangups.ConversationList.get(self._conv_list, chat_message.conv_id)
        if chat_message.user_id != self._client.self_user_id:
            """conv.send_message(text=chat_message.text)"""
            print(chat_message)

    def _on_disconnect(self):
        print('Disconnected')

def main():
    try:
        chat()
    except KeyboardInterrupt:
        pass
    except:
        print('')
        raise

if __name__ == '__main__':
    main()
