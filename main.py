"""A Horrible Project based on the Hangups library
"""
import ChatClient

def main():
    try:
        ChatClient.ChatClient()
    except KeyboardInterrupt:
        pass
    except:
        print('')
        raise

if __name__ == '__main__':
    main()
