import dependency_installer
dependency_installer.install_dependency("pyperclip")

import pyperclip


class Clipboard:
    def paste(self) -> str:
        """Get the text from the clipboard."""
        return pyperclip.paste()

    def copy(self, text: str) -> None:
        """Copy text to the clipboard."""
        pyperclip.copy(text)


if __name__ == "__main__":
    clipboard = Clipboard()
    original_text = clipboard.paste()
    print(clipboard.paste())
    clipboard.copy("Hello, World!")
    print(clipboard.paste())
    clipboard.copy("Goodbye, World!")
    print(clipboard.paste())
    clipboard.copy(original_text)
    print(clipboard.paste())
