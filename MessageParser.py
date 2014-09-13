import re
import random
import wikipedia
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

    def cAtFaCtS(self):
        """Thanks for signing up for Cat Facts! ..
        """
        returnString = ""
        
        facts = open("catfacts.txt", "r")
        catlines = facts.read()        

        catlinesSplit = catlines.split(";")

        returnString = random.choice(catlinesSplit)

        facts.close() 

        return returnString

    def chuck(self):
        """Chuck Norris Facts ..
        """
        returnString = ""
        
        facts = open("chucknorris.txt", "r")
        chucklines = facts.read()        

        chucklinesSplit = chucklines.split(";")

        returnString = random.choice(chucklinesSplit)

        facts.close() 

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
            elif command == "catfacts":
                returnString = self.cAtFaCtS()
            elif command == "chucknorris":
                returnString = self.chuck()
            else:
                returnString = "I don't know how to {}.".format(command)

        return returnString
