#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating TextFieldMenuItem - editable text fields in menu bar dropdowns.

This example shows:
1. Creating a TextFieldMenuItem directly with custom styling
2. Using the @text_field decorator
3. Accessing and updating text field values
4. Using callbacks when text changes
5. Customizing margins and dimensions
"""

import rumps


class TextFieldApp(rumps.App):
    def __init__(self):
        super(TextFieldApp, self).__init__("Text Field Demo")
        
        # Create a TextFieldMenuItem directly with custom styling
        self.search_field = rumps.TextFieldMenuItem(
            value='',
            placeholder='Search...',
            callback=self.on_search_changed,
            dimensions=(200, 24),  # Custom size
            margins=(15, 5, 15, 5)  # Custom margins for better spacing
        )
        
        # Create a compact text field with tighter margins
        self.quick_note = rumps.TextFieldMenuItem(
            value='',
            placeholder='Quick note...',
            callback=self.on_note_changed,
            dimensions=(180, 20),
            margins=(8, 3, 8, 3)
        )
        
        # Add it to the menu
        self.menu = [
            'Status',
            rumps.separator,
            'Search',
            self.search_field,
            rumps.separator,
            'Quick Note',
            self.quick_note,
            rumps.separator,
            'Settings',
        ]
    
    def on_search_changed(self, sender):
        """Called when the search field text changes."""
        search_text = sender.value
        print(f"Search text changed: {search_text}")
        # Update the status item
        self.menu['Status'].title = f"Last search: {search_text if search_text else '(empty)'}"
    
    def on_note_changed(self, sender):
        """Called when the quick note field changes."""
        note = sender.value
        print(f"Quick note: {note}")
    
    @rumps.text_field('Settings', 'Username', value='admin', placeholder='Enter username', dimensions=(160, 22))
    def on_username_changed(self, sender):
        """Called when the username field changes."""
        username = sender.value
        print(f"Username changed: {username}")
    
    @rumps.text_field('Settings', 'API Key', placeholder='Enter your API key', dimensions=(200, 22), margins=(12, 4, 12, 4))
    def on_api_key_changed(self, sender):
        """Called when the API key field changes."""
        api_key = sender.value
        print(f"API key changed: {api_key}")


if __name__ == '__main__':
    TextFieldApp().run()
