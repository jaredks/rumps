import rumps

@rumps.segmented(segments=["10"])
def button_press(self, sender):
    print(self, sender)

app = rumps.App('Segments', quit_button=rumps.MenuItem('Quit', key='q'))
app.menu = [
    rumps.SegmentedMenuItem(["1", "2", "3"], multiselect=True, style='bordered', callback=lambda item: print("Current selection:", item.selection)),
    rumps.SegmentedMenuItem(["4", "5", "6"], style='rectangular', callback=lambda item: print("Selected", item.selection[0])),
    rumps.SegmentedMenuItem(["7", "8", "9"], momentary=True, style='separated', callback=lambda item: print("Clicked", item.selection[0])),
]
app.run()