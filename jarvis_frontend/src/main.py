from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import requests

API_URL = "http://127.0.0.1:8000/foods/"

Window.size = (360, 540)


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
            response = requests.get(API_URL)
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


class FoodListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Top bar with title and add button
        top_bar = BoxLayout(size_hint_y=None, height=dp(50),
                            padding=dp(10), spacing=dp(10))

        title = Label(text="Food List", font_size=22,
                      size_hint_x=0.9, color=(0.95, 0.95, 0.95, 1))
        btn_add = Button(text="+", font_size=28, size_hint_x=0.1,
                         background_normal='', background_color=(0.2, 0.6, 0.8, 1))
        btn_add.bind(on_release=self.open_add)

        top_bar.add_widget(title)
        top_bar.add_widget(btn_add)

        self.food_list_scroll = ScrollView()
        self.food_list = FoodList(on_food_select=self.open_edit)
        self.food_list_scroll.add_widget(self.food_list)

        layout.add_widget(top_bar)
        layout.add_widget(self.food_list_scroll)
        self.add_widget(layout)

    def open_edit(self, food_id):
        self.manager.get_screen('edit').load_food(food_id)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'edit'

    def open_add(self, instance):
        self.manager.get_screen('add').reset_form()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'add'

    def refresh(self):
        self.food_list.load_foods()


class FoodEditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.food_data = None
        self.layout = BoxLayout(orientation='vertical',
                                padding=dp(15), spacing=dp(10))

        self.name_label = Label(text="Name:", size_hint_y=None, height=dp(
            30), color=(0.95, 0.95, 0.95, 1))
        self.name_value = Label(size_hint_y=None, height=dp(
            30), color=(0.95, 0.95, 0.95, 1))

        self.quantity_label = Label(
            text="Quantity:", color=(0.95, 0.95, 0.95, 1))
        self.quantity_input = TextInput(multiline=False, input_filter='int')

        self.protein_label = Label(
            text="Protein (g):", color=(0.95, 0.95, 0.95, 1))
        self.protein_input = TextInput(multiline=False, input_filter='float')

        self.calories_label = Label(
            text="Calories:", color=(0.95, 0.95, 0.95, 1))
        self.calories_input = TextInput(multiline=False, input_filter='float')

        self.created_label = Label(
            text="Created Date:", size_hint_y=None, height=dp(30), color=(0.6, 0.6, 0.6, 1))
        self.created_value = Label(
            size_hint_y=None, height=dp(30), color=(0.6, 0.6, 0.6, 1))

        self.btn_save = Button(text="Save", size_hint_y=None, height=dp(
            40), background_color=(0.2, 0.6, 0.2, 1))
        self.btn_delete = Button(text="Delete", size_hint_y=None, height=dp(
            40), background_color=(0.8, 0.1, 0.1, 1))
        self.btn_back = Button(text="Back", size_hint_y=None, height=dp(40))

        self.btn_save.bind(on_release=self.save_food)
        self.btn_delete.bind(on_release=self.delete_food)
        self.btn_back.bind(on_release=self.go_back)

        # Build layout
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_value)

        self.layout.add_widget(self.quantity_label)
        self.layout.add_widget(self.quantity_input)

        self.layout.add_widget(self.protein_label)
        self.layout.add_widget(self.protein_input)

        self.layout.add_widget(self.calories_label)
        self.layout.add_widget(self.calories_input)

        self.layout.add_widget(self.created_label)
        self.layout.add_widget(self.created_value)

        self.layout.add_widget(self.btn_save)
        self.layout.add_widget(self.btn_delete)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def load_food(self, food_name):
        try:
            response = requests.get(f"{API_URL}{food_name}")
            response.raise_for_status()
            self.food_data = response.json()
            self.name_value.text = self.food_data['name']
            self.quantity_input.text = str(self.food_data['quantity'])
            self.protein_input.text = str(self.food_data['protein'])
            self.calories_input.text = str(self.food_data['calories'])
            self.created_value.text = self.food_data['created_date'].split('T')[
                0]
        except requests.RequestException as e:
            self.name_value.text = "Error loading food"
            self.quantity_input.text = ""
            self.protein_input.text = ""
            self.calories_input.text = ""
            self.created_value.text = ""

            print("Error loading food:", e)

    def save_food(self, instance):
        if not self.food_data:
            return
        food_name = self.food_data["name"]
        updated_data = {
            "id": self.food_data['id'],
            "name": food_name,
            "quantity": int(self.quantity_input.text),
            "protein": float(self.protein_input.text),
            "calories": float(self.calories_input.text),
            # keep original or update if you want
            "created_date": self.food_data['created_date']
        }
        try:
            response = requests.put(f"{API_URL}{food_name}", json=updated_data)
            response.raise_for_status()
            self.manager.get_screen('list').refresh()
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'list'
        except requests.RequestException as e:
            print("Error saving food:", e)

    def delete_food(self, instance):
        if not self.food_data:
            return
        food_name = self.food_data["name"]
        try:
            response = requests.delete(f"{API_URL}{food_name}")
            response.raise_for_status()
            self.manager.get_screen('list').refresh()
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'list'
        except requests.RequestException as e:
            print("Error deleting food:", e)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'list'


class FoodAddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical',
                                padding=dp(15), spacing=dp(10))

        self.name_label = Label(text="Name:", size_hint_y=None, height=dp(
            30), color=(0.95, 0.95, 0.95, 1))
        self.name_input = TextInput(multiline=False)

        self.quantity_label = Label(
            text="Quantity:", color=(0.95, 0.95, 0.95, 1))
        self.quantity_input = TextInput(multiline=False, input_filter='int')

        self.protein_label = Label(
            text="Protein (g):", color=(0.95, 0.95, 0.95, 1))
        self.protein_input = TextInput(multiline=False, input_filter='float')

        self.calories_label = Label(
            text="Calories:", color=(0.95, 0.95, 0.95, 1))
        self.calories_input = TextInput(multiline=False, input_filter='float')

        self.btn_save = Button(text="Add Food", size_hint_y=None, height=dp(
            40), background_color=(0.2, 0.6, 0.2, 1))
        self.btn_cancel = Button(
            text="Cancel", size_hint_y=None, height=dp(40))

        self.btn_save.bind(on_release=self.add_food)
        self.btn_cancel.bind(on_release=self.go_back)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.quantity_label)
        self.layout.add_widget(self.quantity_input)
        self.layout.add_widget(self.protein_label)
        self.layout.add_widget(self.protein_input)
        self.layout.add_widget(self.calories_label)
        self.layout.add_widget(self.calories_input)
        self.layout.add_widget(self.btn_save)
        self.layout.add_widget(self.btn_cancel)

        self.add_widget(self.layout)

    def reset_form(self):
        self.name_input.text = ""
        self.quantity_input.text = ""
        self.protein_input.text = ""
        self.calories_input.text = ""

    def add_food(self, instance):
        new_food = {
            "name": self.name_input.text.strip(),
            "quantity": int(self.quantity_input.text) if self.quantity_input.text else 0,
            "protein": float(self.protein_input.text) if self.protein_input.text else 0.0,
            "calories": float(self.calories_input.text) if self.calories_input.text else 0.0,
            # 'created_date' is auto-set by backend, no need to send
        }
        if not new_food["name"]:
            print("Name is required")
            return
        try:
            response = requests.post(API_URL, json=new_food)
            response.raise_for_status()
            self.manager.get_screen('list').refresh()
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'list'
        except requests.RequestException as e:
            print("Error adding food:", e)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'list'


class FoodApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        sm = ScreenManager()

        sm.add_widget(FoodListScreen(name='list'))
        sm.add_widget(FoodEditScreen(name='edit'))
        sm.add_widget(FoodAddScreen(name='add'))

        return sm


if __name__ == "__main__":
    FoodApp().run()
