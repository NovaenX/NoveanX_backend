from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens import FoodAddScreen, FoodListScreen, FoodEditScreen, SettingsScreen

Window.size = (360, 540)


class FoodApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.settings_data = {
            "protein_target": 0,
            "calories_target": 0
        }

        sm = ScreenManager()

        sm.add_widget(FoodListScreen(name='list'))
        sm.add_widget(FoodEditScreen(name='edit'))
        sm.add_widget(FoodAddScreen(name='add'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm


if __name__ == "__main__":
    FoodApp().run()
