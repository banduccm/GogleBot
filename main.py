import sys
from tornado import ioloop
import hangups


class MessageParser(object):
    """This is a basic class to do some very basic parsing of messages and
    returning strings for specific inputs.
    """

    def __init__(self):
        """Constructor:
        Initialise the user dictionary, used for keeping score
        """
        self._userDict = {}

    def findNameInMessage(self, msgString):
        """Searches for a name by finding the first (if any) @ in a string,
        then grabbing any text between the @ and the next ' ' character.
        Returns an empty string if no @ is found in the input string.
        """
        returnString = ''
        nameEnd = 0
        nameStart = -1

        if '@' in msgString:
            nameStart = msgString.find('@')

        nameStart += 1  # Increment the position by 1 to skip the @ sign

        if nameStart > 0:
            nameEnd = msgString.find(' ', nameStart)

            if (nameEnd < 0):
                # There is no space in the string after the @, assume that the
                # name goes to the end of the string
                returnString = msgString[nameStart:]
            else:
                returnString = msgString[nameStart:nameEnd]

        return returnString

    def findScoreInMessage(self, msgString):
        """Searches for a score by finding the first (if any) + or - in a
        string, then grabbing any text between the +/- and the next ' '
        character. Returns an empty string if no + or - is found in the input
        string.
        """
        returnString = ''
        scoreEnd = 0
        scoreStart = -1
        scoreSign = ''

        if '+' in msgString:
            scoreSign = '+'
            scoreStart = msgString.find('+')
        elif '-' in msgString:
            scoreSign = '-'
            scoreStart = msgString.find('-')

        scoreStart += 1

        if scoreStart > 0:
            scoreEnd = msgString.find(' ', scoreStart)

            if (scoreEnd < 0):
                # There is no space in the string after the sign, assume the
                # score goes to the end of the string
                returnString = scoreSign + msgString[scoreStart:]
            else:
                returnString = scoreSign + msgString[scoreStart:scoreEnd]

        return returnString

    def parseMessage(self, chat_message):
        """Parses the input chat message object's text and keeps the user score
        up to date if necessary
        """
        returnString = ''
        name = self.findNameInMessage(chat_message.text)
        score = self.findScoreInMessage(chat_message.text)
        if name:
            if name.lower() not in self._userDict:
                # Create the user key if it does not exist
                self._userDict[name.lower()] = 0

            if score:
                # If both a name and score were found in the message text,
                # update the dictionary and print the user's total score
                intScore = int(score)
                self._userDict[name.lower()] += intScore
                returnString = ''.join(
                    name.lower(),
                    ': ',
                    str(self._userDict[name.lower()])
                    )

        return returnString


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

        # Initialize the Hangups client using the credentials collected above
        # and the callbacks defined in this class
        self._client = hangups.Client(cookies)
        self._client.on_connect.add_observer(self._on_connect)
        self._client.on_disconnect.add_observer(self._on_disconnect)
        self._client.on_message.add_observer(self._on_message)

        # Initialise the message parser
        self._parser = MessageParser()

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


def main():
    try:
        ChatClient()
    except KeyboardInterrupt:
        pass
    except:
        print('')
        raise

if __name__ == '__main__':
    main()
