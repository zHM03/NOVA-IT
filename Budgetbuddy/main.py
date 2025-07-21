from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from core import BudgetManager

Window.clearcolor = (0, 0, 0, 1)

class BudgetAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.manager = BudgetManager()

        self.title = Label(text="BudgetBuddy", markup=True, font_size=28, size_hint=(1, 0.15), halign="center")
        self.add_widget(self.title)

        self.income_input = TextInput(hint_text="Gelir miktarı", input_filter="float", multiline=False, size_hint_y=None, height=40)
        self.income_button = Button(text="Gelir Ekle", size_hint_y=None, height=45, background_color=(0.2, 0.7, 0.2, 1))

        self.expense_input = TextInput(hint_text="Gider miktarı", input_filter="float", multiline=False, size_hint_y=None, height=40)
        self.category_input = TextInput(hint_text="Kategori (ör. Yiyecek, Ulaşım...)", multiline=False, size_hint_y=None, height=40)
        self.expense_button = Button(text="Gider Ekle", size_hint_y=None, height=45, background_color=(0.8, 0.3, 0.3, 1))

        self.delete_income_button = Button(text="Gelirleri Listele ve Sil", size_hint_y=None, height=45, background_color=(0.3, 0.5, 0.8, 1))
        self.delete_expense_button = Button(text="Giderleri Listele ve Sil", size_hint_y=None, height=45, background_color=(0.3, 0.5, 0.8, 1))

        self.summary_label = Label(text="", font_size=16, markup=True, size_hint_y=None, height=60)

        self.income_button.bind(on_press=self.add_income)
        self.expense_button.bind(on_press=self.add_expense)
        self.delete_income_button.bind(on_press=self.show_incomes)
        self.delete_expense_button.bind(on_press=self.show_expenses)

        for widget in [
            self.income_input, self.income_button,
            self.expense_input, self.category_input, self.expense_button,
            self.delete_income_button, self.delete_expense_button,
            self.summary_label
        ]:
            self.add_widget(widget)

        self.update_summary()

    def update_summary(self):
        income, expense, balance = self.manager.get_summary()
        self.summary_label.text = (
            f"[b]Toplam Gelir:[/b] ₺{income:.2f}   \n"
            f"[b]Toplam Gider:[/b] ₺{expense:.2f}   \n"
            f"[b]Kalan:[/b] ₺{balance:.2f}"
        )

    def add_income(self, instance):
        try:
            amount = float(self.income_input.text)
            self.manager.add_income(amount)
            self.income_input.text = ""
            self.update_summary()
        except ValueError:
            self.summary_label.text = "[color=ff0000]Geçerli bir gelir miktarı girin[/color]"

    def add_expense(self, instance):
        try:
            amount = float(self.expense_input.text)
            category = self.category_input.text.strip()
            if not category:
                self.summary_label.text = "[color=ff0000]Kategori girin[/color]"
                return
            self.manager.add_expense(amount, category)
            self.expense_input.text = ""
            self.category_input.text = ""
            self.update_summary()
        except ValueError:
            self.summary_label.text = "[color=ff0000]Geçerli bir gider miktarı girin[/color]"

    def show_incomes(self, instance):
        self.clear_widgets()
        self.add_widget(Label(text="[b]Gelir Listesi[/b]", markup=True, font_size=20))
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for idx, income in enumerate(self.manager.get_all_income()):
            btn = Button(text=f"{idx+1}) ₺{income['amount']}", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, i=idx: self.delete_income(i))
            box.add_widget(btn)

        scroll.add_widget(box)
        self.add_widget(scroll)
        self.add_widget(Label(text="Silmek istediğinizin üstüne tıklayın", size_hint_y=None, height=30, halign="center", valign="middle"))
        self.add_back_button()


    def show_expenses(self, instance):
        self.clear_widgets()
        self.add_widget(Label(text="[b]Gider Listesi[/b]", markup=True, font_size=20))

        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for idx, expense in enumerate(self.manager.get_all_expense()):
            cat = expense.get("category", "")
            btn = Button(text=f"{idx+1}) ₺{expense['amount']} - {cat}", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, i=idx: self.delete_expense(i))
            box.add_widget(btn)

        scroll.add_widget(box)
        self.add_widget(scroll)
        self.add_widget(Label(text="Silmek istediğinizin üstüne tıklayın", size_hint_y=None, height=30, halign="center", valign="middle"))

        self.add_back_button()

    def delete_income(self, index):
        self.manager.delete_income(index)
        self.show_incomes(None)

    def delete_expense(self, index):
        self.manager.delete_expense(index)
        self.show_expenses(None)

    def add_back_button(self):
        btn = Button(text="Ana Ekrana Dön", size_hint_y=None, height=50, background_color=(0.6, 0.6, 0.6, 1))
        btn.bind(on_press=lambda x: self.reset_ui())
        self.add_widget(btn)

    def reset_ui(self):
        self.clear_widgets()
        self.__init__()


class BudgetBuddyApp(App):
    def build(self):
        return BudgetAppLayout()


if __name__ == '__main__':
    BudgetBuddyApp().run()
