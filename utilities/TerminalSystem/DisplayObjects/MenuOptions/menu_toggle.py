from base_menu_option import BaseMenuOption


class MenuToggle(BaseMenuOption):

    def __init__(self, name: str, text: str, color_scheme: dict[str, list[str]] | None = None,
                 function: callable | None = None, *args, **kwargs) -> None:
        """Initialize the MenuOption object.

        Args:
            name (str):
                The name of the menu option.
            text (str):
                The text of the menu option.
            color_scheme (dict[str, list[str]], optional):
                The color scheme of the menu option.
                Defaults to None.
            function (callable, optional):
                The function called under certain circumstances.
                Defaults to None.
            *args:
                The arguments to hand to the function if and when it's called.
            **kwargs:
                The keyword arguments to hand to the function if and when it's called.
        """
        super().__init__(name, text, color_scheme, function, *args, **kwargs)

    def execute(self):
        self.toggle.value = not self.toggle.value
        if self.toggle.value:
            self.name = self.toggle_on
        else:
            self.name = self.toggle_off

    def __str__(self):
        return self.name