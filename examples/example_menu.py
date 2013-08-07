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
        sender['ppp'] = MenuItem('ppp')
    else:
        del sender['$']
        del sender['%']
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
    None
]
app.run()
