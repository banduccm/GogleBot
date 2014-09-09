"""A Horrible Project based on the Hangups library
"""

import sys
import hangups
import re
import random
import wikipedia
from tornado import ioloop
from collections import defaultdict


class MessageParser(object):
    """This is a basic class to do some very basic parsing of messages and
    returning strings for specific inputs.
    """

    def __init__(self):
        """Constructor:
        Initialise the user dictionary, used for keeping score
        """
        # Default all user scores to 0
        self._userDict = defaultdict(int)

    def findCommandInMessage(self, msgString):
        """Searches for a command by finding the first (if any) # in a string,
        then getting all of the alpha characters immediately following the #.
        Returns empty if no # is found in the input string.
        """
        returnString = ''
        m = re.search("#(?P<cmd>[a-zA-Z0-9_]+)", msgString)
        if m:
            returnString = m.group("cmd")

        return returnString

    def findNameInMessage(self, msgString):
        """Searches for a name by finding the first (if any) @ in a string,
        then getting all of the alpha characters immediately following the @.
        Returns an empty string if no @ is found in the input string.
        """
        returnString = ''
        m = re.search("@(?P<name>[a-zA-Z]+)", msgString)
        if m:
            returnString = m.group("name")

        return returnString

    def findScoreInMessage(self, msgString):
        """Searches for a score by finding the first (if any) + or - in a
        string, then getting all of the alpha characters immediately
        following the +/-. Returns an empty string if no + or - is found
        in the input string.
        """
        returnString = ''
        m = re.search("(?P<score>[\-\+][0-9]+)", msgString)
        if m:
            returnString = m.group("score")

        return returnString

    def parseDieRoll(self, msgString):
        """Parses the "roll the dice" command by finding the desired die size
        then returning a random number from 1 to the found size. Thanks to
        Doug for the idea, which was lovingly ripped off. Returns an error
        string if no valid die size is found.
        """
        errorString = "Invalid die. Try #rtd d<number>."
        returnString = ''
        m = re.search("d(?P<die>[0-9]+)", msgString)
        if m:
            try:
                dieSize = int(m.group("die"))
            except:
                returnString = errorString
            else:
                if dieSize > 0:
                    returnString = str(random.randint(1, dieSize))
                else:
                    returnString = errorString
        else:
            returnString = errorString

        return returnString

    def handleRandomCommand(self):
        """Gets a random page from Wikipedia and prints the summary paragraph.
        """
        returnString = ""

        pg = wikipedia.random(1)
        try:
            returnString = wikipedia.summary(pg)
        except wikipedia.exceptions.DisambiguationError:
            returnString = self.handleRandomCommand()

        return returnString

    def parseMessage(self, chat_message):
        """Parses the input chat message object's text and keeps the user score
        up to date if necessary
        """
        returnString = ''

        name = self.findNameInMessage(chat_message.text)
        command = self.findCommandInMessage(chat_message.text)

        if name:
            score = self.findScoreInMessage(chat_message.text)
            if score:
                # If both a name and score were found in the message text,
                # update the dictionary and print the user's total score
                intScore = 0
                try:
                    intScore = int(score)
                except:
                    returnString = "Invalid Score Format! Try <+/-><number>."
                else:
                    lname = name.lower()
                    self._userDict[lname] += intScore
                    returnString = '{}: {}'.format(
                        lname,
                        self._userDict[lname]
                        )

        elif command:
            if command == "score":
                returnString = ' | '.join(
                    '{}: {}'.format(*item) for item in self._userDict.items()
                    )
            elif command == "3257":
                returnString = "Hot Asphalt"
            elif command == "rtd":
                returnString = self.parseDieRoll(chat_message.text)
            elif command == "random":
                returnString = self.handleRandomCommand()
            else:
                returnString = "I don't know how to {}.".format(command)

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
