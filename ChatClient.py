import sys
import hangups
from tornado import ioloop
import MessageParser

class ChatClient(object):
    """This class is a very basic chat client for the Hangups library. It
    implements the bare minimum to have a "working" client.
    """

    def __init__(self):
        """Constructor:
        Initialize the Hangups library, register the necessary callbacks, and
        initialise the message parser
        """
        # Attempt to get the user credentials. Request them from the python
        # terminal if they are not found
        try:
            cookies = hangups.get_auth_stdin('c.txt')
        except hangups.GoogleAuthError as e:
            print('Login failed ({})'.format(e))
            sys.exit(1)
        else:
            print('Login Successful!')

        # Initialize the Hangups client using the credentials collected above
        # and the callbacks defined in this class
        self._client = hangups.Client(cookies)
        self._client.on_connect.add_observer(self._on_connect)
        self._client.on_disconnect.add_observer(self._on_disconnect)
        self._client.on_message.add_observer(self._on_message)

        # Initialise the message parser
        self._parser = MessageParser.MessageParser()

        # Enter the IOLoop. Not 100% what's going on here, needs more research.
        # Stolen from the Hangups example code.
        ioloop.IOLoop.instance().run_sync(self._client.connect)
        ioloop.IOLoop.instance().start()

    def _on_connect(self):
        self._conv_list = hangups.ConversationList(self._client)
        self._user_list = hangups.UserList(self._client)

    def _on_message(self, chat_message):
        conv = hangups.ConversationList.get(
            self._conv_list,
            chat_message.conv_id
            )
        if chat_message.user_id != self._client.self_user_id:
            # Message Handling Code
            msgstr = self._parser.parseMessage(chat_message)
            if msgstr:
                conv.send_message(text=msgstr)

    def _on_disconnect(self):
        print('Disconnected')
