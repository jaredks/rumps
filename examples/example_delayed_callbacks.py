from rumps import *

@clicked('Testing')
def tester(sender):
    sender.state = not sender.state

class SomeApp(rumps.App):
    def __init__(self):
        super(SomeApp, self).__init__(type(self).__name__, menu=['On', 'Testing'])
        rumps.debug_mode(True)

    @clicked('On')
    def button(self, sender):
        sender.title = 'Off' if sender.title == 'On' else 'On'
        Window("I can't think of a good example app...").run()

if __name__ == "__main__":
    SomeApp().run()
