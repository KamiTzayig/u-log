# Welcome to U-Log

## Getting Started with the Chrome Extension

To use the U-Log Chrome Extension, follow these steps:

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" by toggling the switch in the top right corner.
3. Click on the "Load unpacked" button.
4. Select the `chrome_monitore` folder from your computer. This will install the extension.

## Creating a New Executable File

To create a new executable file that bundles all the necessary scripts, use the following command in your terminal or command prompt:

```bash
pyinstaller --onefile --add-data "chrome_monitor_webserver.py;." --add-data "keyboard_logger.py;." --add-data "mouse_logger.py;." --add-data "windows_logger.py;." --add-data "controller_logger.py;." main.py
```