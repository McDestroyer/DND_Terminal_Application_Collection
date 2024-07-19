import dependency_installer
dependency_installer.install_dependency("pynput")

from pynput import mouse


class Suppressor:
    def __init__(self, window_rect):
        self.window_rect = window_rect

        self.is_clicked = False

        self.mc = mouse.Controller()

        self.listener = mouse.Listener(win32_event_filter=self.win32_event_filter)
        self.listener.start()

    def win32_event_filter(self, msg, _) -> bool:
        # Suppress Left click
        if (msg == 513 or msg == 514) and self.window_rect and (
                self.window_rect["left"] < self.mc.position[0] < self.window_rect["right"] and
                self.window_rect["top"] < self.mc.position[1] < self.window_rect["bottom"]
        ):
            # print("Suppressed left click")
            # print(f"Left click {'pressed' if self.is_clicked else 'released'}")
            self.is_clicked = True if msg == 513 else False
            self.listener.suppress_event()
        return True
