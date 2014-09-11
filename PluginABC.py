import abc

class GoglebotPlugin(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def pluginName(self):
        """return the plugin's name as a string"""
        return

    @abc.abstractmethod
    def onMessageReceived(self, inputString):
        """Process the input string and return a string"""
        return
