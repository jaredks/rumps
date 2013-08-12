import rumps
import time


def timez():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


@rumps.timer(1)
def a(sender):
    print sender, timez()


@rumps.clicked('Change timer')
def changeit(_):
    response = rumps.Window('Enter new interval').run()
    if response.clicked:
        global_namespace_timer.interval = int(response.text)


@rumps.clicked('All timers')
def activetimers(_):
    print rumps.timers()


@rumps.clicked('Start timer')
def start_timer(_):
    global_namespace_timer.start()


@rumps.clicked('Stop timer')
def stop_timer(_):
    global_namespace_timer.stop()


if __name__ == "__main__":
    global_namespace_timer = rumps.Timer(a, 4)
    rumps.App('fuuu', menu=('Change timer', 'All timers', 'Start timer', 'Stop timer')).run()
