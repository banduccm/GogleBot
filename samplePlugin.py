import PluginABC

class samplePlugin(PluginABC.GoglebotPlugin):
    def pluginName(self):
        return "Sample Plugin"

    def onMessageReceived(self, inputString):
        return "Sample!"
