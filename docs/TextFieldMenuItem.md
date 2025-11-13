# TextFieldMenuItem Feature

This feature adds support for editable text fields directly within menu bar dropdowns in rumps.

## Overview

`TextFieldMenuItem` is a new menu item type that embeds an `NSTextField` control, allowing users to type text directly into the menu without opening a separate window. It follows the same pattern as the existing `SliderMenuItem`.

## Features

- **Direct text input** in menu dropdowns
- **Placeholder text** support
- **Callback function** triggered when text changes or Enter is pressed
- **Programmatic access** to current text value
- **Decorator pattern** for easy integration with menu hierarchy

## Usage

### Method 1: Direct Instantiation

```python
import rumps

class MyApp(rumps.App):
    def __init__(self):
        super(MyApp, self).__init__("My App")
        
        # Create a text field menu item
        self.search_field = rumps.TextFieldMenuItem(
            value='',
            placeholder='Search...',
            callback=self.on_search
        )
        
        self.menu = ['Search', self.search_field]
    
    def on_search(self, sender):
        search_text = sender.value
        print(f"Search: {search_text}")
```

### Method 2: Using the Decorator

```python
import rumps

class MyApp(rumps.App):
    @rumps.text_field('Settings', 'Username', value='admin', placeholder='Enter username')
    def on_username_changed(self, sender):
        username = sender.value
        print(f"Username: {username}")
```

## API Reference

### TextFieldMenuItem

**Constructor Parameters:**
- `value` (str): Initial text value (default: '')
- `placeholder` (str): Placeholder text when field is empty (default: '')
- `callback` (callable): Function called when text changes (default: None)
- `dimensions` (tuple): Width and height in pixels (default: (180, 22))
- `margins` (tuple): Left, top, right, bottom margins in pixels (default: (10, 4, 10, 4))

**Properties:**
- `value`: Get or set the current text value
- `placeholder`: Get or set the placeholder text
- `callback`: Get the current callback function

**Methods:**
- `set_callback(callback)`: Set or change the callback function

### text_field Decorator

```python
@rumps.text_field(*path, value='', placeholder='', callback=None, dimensions=(200, 24), margins=(15, 5, 15, 5))
def my_callback(self, sender):
    text = sender.value
    # Handle text change
```

**Parameters:**
- `*path`: Menu path where the text field should be placed (e.g., 'Settings', 'User Info', 'Username')
- `value`: Initial text value
- `placeholder`: Placeholder text
- `callback`: Callback function (optional, will use the decorated function)
- `dimensions`: Width and height in pixels
- `margins`: Left, top, right, bottom margins in pixels

## Examples

See `examples/example_text_field.py` for a complete working example.

## Implementation Details

- Built using native macOS `NSTextField` control
- Follows the same pattern as `SliderMenuItem`
- Uses `NSView` container for proper menu integration
- Leverages existing rumps callback mechanism via `NSApp._ns_to_py_and_callback`

## Compatibility

- Requires macOS (uses PyObjC and AppKit)
- rumps version 0.4.1+
