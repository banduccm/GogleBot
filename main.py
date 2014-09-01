from tornado import ioloop
import hangups
from hangups.notify import Notifier

class MessageParser(object):
    def findNameInMessage(msgString):
        returnString = ''
        nameEnd = 0
        nameStart = -1

        if '@' in msgString:
            nameStart = msgString.find('@')
            
        nameStart += 1

        if nameStart > 0:
            nameEnd = msgString.find(' ', nameStart)
            
            if (nameEnd < 0):
                returnString =  msgString[nameStart:]
            else:
                returnString =  msgString[nameStart:nameEnd]

        return returnString

    def findScoreInMessage(msgString):
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
                returnString = scoreSign + msgString[scoreStart:]
            else:
                returnString = scoreSign + msgString[scoreStart:scoreEnd]

        return returnString
        
        
    def parseMessage(chat_message):
        returnString = ''
        name = MessageParser.findNameInMessage(chat_message.text)
        score = MessageParser.findScoreInMessage(chat_message.text)
        if name:
            if score:
                returnString = name + ' : ' + score
            
        return returnString
    
class ChatClient(object):
    def __init__(self):
        try:
            cookies = hangups.get_auth_stdin('c.txt')
        except hangups.GoogleAuthError as e:
            print('Login failed ({})'.format(e))
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

    def _on_message(self, chat_message):
        conv = hangups.ConversationList.get(self._conv_list, chat_message.conv_id)
        if chat_message.user_id != self._client.self_user_id:
            #Message Handling Code
            msgstr= MessageParser.parseMessage(chat_message)
            if msgstr:
                conv.send_message(text=msgstr)
            print("message received")

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
