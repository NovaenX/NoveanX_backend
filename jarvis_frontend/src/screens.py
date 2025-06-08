from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.metrics import dp
import requests

from layouts import FoodList

FOOD_API_URL = "http://127.0.0.1:8000/foods/"
SETTINGS_API_URL = "http://127.0.0.1:8000/settings/"
DAILY_API_URL = "http://127.0.0.1:8000/daily/"


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

        btn_settings = Button(text="⚙", size_hint_x=0.1, font_size=22,
                              background_normal='', background_color=(0.3, 0.3, 0.3, 1))
        btn_settings.bind(on_release=self.open_settings)
        btn_add.bind(on_release=self.open_add)

        self.food_list_scroll = ScrollView()
        self.food_list = FoodList(on_food_select=self.open_edit)
        self.food_list_scroll.add_widget(self.food_list)

        self.summary_label = Label(
            text="0/0 cal | 0/0 g protein", color=(0.9, 0.9, 0.9, 1))

        top_bar.add_widget(title)
        top_bar.add_widget(btn_add)
        top_bar.add_widget(btn_settings)

        layout.add_widget(self.summary_label)
        layout.add_widget(top_bar)
        layout.add_widget(self.food_list_scroll)

        self.add_widget(layout)

    def open_settings(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'settings'

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
        try:
            response = requests.get(DAILY_API_URL)
            if response.status_code == 200:
                data = response.json()
                settings_resp = requests.get(DAILY_API_URL).json()
                target_cal = settings_resp.get("target_calories", 0)
                target_pro = settings_resp.get("target_protein", 0)

                actual_cal = data.get("calories_intake", 0)
                actual_pro = data.get("protein_intake", 0)

                self.summary_label.text = f"{actual_cal}/{target_cal} cal | {actual_pro}/{target_pro} g protein"
            else:
                self.summary_label.text = "0/0 cal | 0/0 g protein"
        except Exception as e:
            print(f"Failed to fetch summary: {e}")
            self.summary_label.text = "0/0 cal | 0/0 g protein"


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
        self.created_value = TextInput(
            multiline=False, size_hint_y=None, height=dp(30),
            foreground_color=(0.95, 0.95, 0.95, 1),
            background_color=(0.2, 0.2, 0.2, 1),
            hint_text="YYYY-MM-DD"
        )

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
            response = requests.get(f"{FOOD_API_URL}{food_name}")
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
            "created_date": self.created_value.text + "T00:00:00"

        }
        try:
            response = requests.put(
                f"{FOOD_API_URL}{food_name}", json=updated_data)
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
            response = requests.delete(f"{FOOD_API_URL}{food_name}")
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
            response = requests.post(FOOD_API_URL, json=new_food)
            response.raise_for_status()

            self.manager.get_screen('list').refresh()
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'list'
        except requests.RequestException as e:
            print("Error adding food:", e)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'list'


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical',
                                padding=dp(15), spacing=dp(10))

        self.label_title = Label(
            text="Settings", font_size=22, color=(0.95, 0.95, 0.95, 1))
        self.protein_label = Label(
            text="Daily Protein Target (g):", color=(0.95, 0.95, 0.95, 1))
        self.protein_input = TextInput(multiline=False, input_filter='float')

        self.calories_label = Label(
            text="Daily Calorie Target:", color=(0.95, 0.95, 0.95, 1))
        self.calories_input = TextInput(multiline=False, input_filter='float')

        self.btn_save = Button(text="Save", size_hint_y=None, height=dp(
            40), background_color=(0.2, 0.6, 0.2, 1))
        self.btn_back = Button(text="Back", size_hint_y=None, height=dp(40))

        self.btn_save.bind(on_release=self.save_settings)
        self.btn_back.bind(on_release=self.go_back)

        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.protein_label)
        self.layout.add_widget(self.protein_input)
        self.layout.add_widget(self.calories_label)
        self.layout.add_widget(self.calories_input)
        self.layout.add_widget(self.btn_save)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        try:
            response = requests.get(SETTINGS_API_URL)
            if response.status_code == 200:
                data = response.json()
                self.protein_input.text = str(data.get("target_protein", ""))
                self.calories_input.text = str(data.get("target_calories", ""))
            else:
                print("Settings not found, using defaults.")
                self.protein_input.text = ""
                self.calories_input.text = ""
        except Exception as e:
            print(f"Error fetching settings: {e}")

    def save_settings(self, instance):
        try:
            protein = float(
                self.protein_input.text) if self.protein_input.text else 0
            calories = float(
                self.calories_input.text) if self.calories_input.text else 0

            response = requests.put(
                SETTINGS_API_URL,
                params={"target_protein": protein, "target_calories": calories}
            )

            if response.status_code == 200:
                print("Settings saved successfully.")
            else:
                print(f"Failed to save settings: {response.status_code}")

        except Exception as e:
            print(f"Error saving settings: {e}")

        self.go_back(instance)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'list'
