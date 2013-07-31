import rumps
import time

rumps.debug_mode(True)  # turn on command line logging information for development - default is off


@rumps.clicked("About")
def about(sender):
    sender.title = 'NOM' if sender.title == 'About' else 'About'  # can adjust titles of menu items dynamically
    rumps.alert("This is a cool app!")


@rumps.clicked("Arbitrary", "Depth", "It's pretty easy")  # very simple to access nested menu items
def does_something(sender):
    my_data = {'poop': 88}
    rumps.notification(title='Hi', subtitle='There.', message='Friend!', sound=does_something.sound, data=my_data)
does_something.sound = True


@rumps.clicked("Preferences")
def not_actually_prefs(sender):
    if not sender.icon:
        sender.icon = 'level_4.png'
    sender.state = not sender.state
    does_something.sound = not does_something.sound


@rumps.timer(4)  # create a new thread that calls the decorated function every 4 seconds
def write_unix_time(sender):
    with app.open('times', 'a') as f:  # this opens files in your app's Application Support folder
        f.write('The unix time now: {}\n'.format(time.time()))


@rumps.clicked("Arbitrary")
def change_statusbar_title(sender):
    app.title = 'Hello World' if app.title != 'Hello World' else 'World, Hello'


@rumps.notifications
def notifications(notification):  # function that reacts to incoming notification dicts
    print notification


if __name__ == "__main__":
    app = rumps.App("My Toolbar App", title='World, Hello')
    app.menu = [
        rumps.MenuItem('About', icon='pony.jpg', dimensions=(18, 18)),  # can specify an icon to be placed near text
        'Preferences',
        None,  # None functions as a separator in your menu
        {'Arbitrary':
            {"Depth": ["Menus", "It's pretty easy"],
             "And doesn't": ["Even look like Objective C", "One bit"]}},
        None
    ]
    app.run()
