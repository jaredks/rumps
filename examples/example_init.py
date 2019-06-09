import rumps


@rumps.clicked('Switch next')
def switch_next(_):
    switch_previous.menuitem.state = not switch_previous.menuitem.state


@rumps.clicked('Switch previous')
def switch_previous(_):
    switch_next.menuitem.state = not switch_next.menuitem.state


def init_app():
    switch_next.menuitem.state = True


if __name__ == "__main__":
    rumps.App('First item should be checked', on_before_event_loop=init_app).run()
