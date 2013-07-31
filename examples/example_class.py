import rumps

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp().run()
