import rumps

rumps.debug_mode(True)

@rumps.clicked('Print Something')
def print_something(_):
    rumps.alert(message='something', ok='YES!', cancel='NO!')


@rumps.clicked('On/Off Test')
def on_off_test(_):
    print_button = app.menu['Print Something']
    if print_button.callback is None:
        print_button.set_callback(print_something)
    else:
        print_button.set_callback(None)


@rumps.clicked('Clean Quit')
def clean_up_before_quit(_):
    print 'execute clean up code'
    rumps.quit_application()


app = rumps.App('Hallo Thar', menu=['Print Something', 'On/Off Test', 'Clean Quit'], quit_button=None)
app.run()
