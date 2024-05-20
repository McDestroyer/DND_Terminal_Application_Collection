class Screen:
    def __init__(self, screen_name: str, display_object) -> None:
        self.screen_name = screen_name
        self.screen_objects = []
        self.display_object = display_object

    def add_object(self, screen_object):
        self.screen_objects.append(screen_object)
        self.screen_objects.sort(key=lambda x: x.get_z_index())

    def remove_object(self, screen_object):
        self.screen_objects.remove(screen_object)

    def get_objects(self):
        return self.screen_objects

    def get_name(self):
        return self.screen_name

    def __str__(self):
        return self.screen_name

    def __repr__(self):
        return self.screen_name

    def __eq__(self, other):
        return self.screen_objects == other.screen_objects

    def __ne__(self, other):
        return not self == other

    def refresh_display_objects(self):
        for screen_object in self.screen_objects:
            screen_object.get_contents()

