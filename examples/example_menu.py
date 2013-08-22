from rumps import *
import urllib

def sayhello(sender):
    print 'hello {}'.format(sender)

def e(_):
    print 'EEEEEEE'

def adjust_f(sender):
    if adjust_f.huh:
        sender.add('$')
        sender.add('%')
        sender['zzz'] = 'zzz'
        sender['separator'] = separator
        sender['ppp'] = MenuItem('ppp')
    else:
        del sender['$']
        del sender['%']
        del sender['separator']
        del sender['ppp']
    adjust_f.huh = not adjust_f.huh
adjust_f.huh = True

def print_f(_):
    print f

f = MenuItem('F', callback=adjust_f)

urllib.urlretrieve('http://upload.wikimedia.org/wikipedia/commons/thumb/c/'
                   'c4/Kiss_Logo.svg/200px-Kiss_Logo.svg.png', 'kiss.png')
app = App('lovegun', icon='kiss.png')
app.menu = [
    MenuItem('A', callback=print_f, key='F'),
    ('B', ['1', 2, '3', [4, [5, (6, range(7, 14))]]]),
    'C',
    [MenuItem('D', callback=sayhello), (1, 11, 111)],
    MenuItem('E', callback=e, key='e'),
    f,
    None,
    {
        'x': {'hello', 'hey'},
        'y': ['what is up']
    },
    [1, [2]],
    ('update method', ['walking', 'back', 'to', 'you']),
    'stuff',
    None
]

@clicked('update method')
def dict_update(menu):
    print menu
    print menu.setdefault('boo', MenuItem('boo',
                                          callback=lambda _: add_separator(menu)))  # lambda gets THIS menu not submenu

def add_separator(menu):
    menu.add(separator)

@clicked('C')
def change_main_menu(_):
    print app.menu
    print 'goodbye C'
    del app.menu['C']  # DELETE SELF!!!1

@clicked('stuff')
def stuff(sender):
    print sender
    if len(sender):
        sender.insert_after('lets', 'go?')
        sender['the'].insert_before('band', 'not')
        sender['the'].insert_before('band', 'a')
    else:
        sender.update(['hey', ['ho', MenuItem('HOOOO')], 'lets', 'teenage'], the=['who', 'is', 'band'])
        sender.add('waste land')

app.run()
