import rumps

window = rumps.Window('Nothing...', 'ALERTZ')
window.title = 'WINDOWS jk'
window.message = 'Something.'
window.default_text = 'eh'

response = window.run()
print response

window.add_buttons('One', 'Two', 'Three')

print window.run()
print response
