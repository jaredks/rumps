import rumps

rumps.debug_mode(True)

@rumps.clicked('Icon', 'On')
def a(_):
    app.icon = 'test.png'

@rumps.clicked('Icon', 'Off')
def b(_):
    app.icon = None

@rumps.clicked('Title', 'On')
def c(_):
    app.title = 'Buzz'

@rumps.clicked('Title', 'Off')
def d(_):
    app.title = None

app = rumps.App('Buzz Application', quit_button=rumps.MenuItem('Quit Buzz', key='q'))
app.menu = [
    ('Icon', ('On', 'Off')),
    ('Title', ('On', 'Off'))
]
app.run()
