from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import requests

FOOD_API_URL = "http://127.0.0.1:8000/foods/"
SETTINGS_API_URL = "http://127.0.0.1:8000/settings/"


class FoodCard(BoxLayout):
    def __init__(self, food, on_press_callback, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None,
                         height=dp(160), padding=dp(10), spacing=dp(5), **kwargs)

        with self.canvas.before:
            self.bg_color = Color(0.12, 0.12, 0.12, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        light_text = (0.95, 0.95, 0.95, 1)
        subtle_text = (0.6, 0.6, 0.6, 1)

        self.add_widget(Label(text=f"[b]{food['name']}[/b]", markup=True, font_size=18,
                              color=light_text, size_hint_y=None, height=dp(30)))
        self.add_widget(
            Label(text=f"Quantity: {food['quantity']}", font_size=14, color=light_text))
        self.add_widget(
            Label(text=f"Protein: {food['protein']} g", font_size=14, color=light_text))
        self.add_widget(
            Label(text=f"Calories: {food['calories']} kcal", font_size=14, color=light_text))
        self.add_widget(Label(text=f"Added: {food['created_date'].split('T')[0]}",
                              font_size=12, color=subtle_text))

        # Touch behavior: bind tap/click to callback passing food id
        self.bind(on_touch_down=self._on_touch_down)
        self.on_press_callback = on_press_callback
        self.food_name = food["name"]

    def _update_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _on_touch_down(self, instance, touch):
        if self.collide_point(*touch.pos):
            # Call the callback with this food id
            self.on_press_callback(self.food_name)
            return True
        return False


class FoodList(GridLayout):
    def __init__(self, on_food_select, **kwargs):
        super().__init__(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10), **kwargs)
        self.bind(minimum_height=self.setter("height"))
        self.on_food_select = on_food_select
        self.load_foods()

    def load_foods(self):
        self.clear_widgets()
        try:
            response = requests.get(FOOD_API_URL)
            response.raise_for_status()
            foods = response.json()
            foods.sort(key=lambda f: f['created_date'], reverse=True)
            if not foods:
                self.add_widget(
                    Label(text="No food items available.", color=(1, 1, 1, 1)))
            for food in foods:
                self.add_widget(FoodCard(food, self.on_food_select))
        except requests.RequestException as e:
            self.add_widget(
                Label(text=f"Error fetching food data:\n{e}", color=(1, 0.3, 0.3, 1)))
