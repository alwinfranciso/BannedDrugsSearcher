from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivy.core.window import Window

Window.size = (360, 640)  # Set the window size for desktop testing

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDTextField:
            id: file_path
            hint_text: "File Path"
            readonly: True

        MDRaisedButton:
            text: "Browse"
            on_release: app.file_manager_open()

        MDTextField:
            id: word
            hint_text: "Word to Search"

        MDRaisedButton:
            text: "Search"
            on_release: app.search_word()

        ScrollView:
            MDList:
                id: results_list
'''

class MainScreen(Screen):
    pass

class WordSearchApp(MDApp):
    def build(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show('/')  # Show the root directory

    def select_path(self, path):
        self.root.get_screen('main').ids.file_path.text = path
        self.file_manager.close()

    def exit_manager(self, *args):
        self.file_manager.close()

    def search_word(self):
        file_path = self.root.get_screen('main').ids.file_path.text
        word = self.root.get_screen('main').ids.word.text
        if file_path and word:
            results = self.search_word_in_file(file_path, word)
            self.display_results(results)
        else:
            self.show_dialog("Input Error", "Please provide both file path and word to search.")

    def search_word_in_file(self, file_path, word):
        results = []
        try:
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    if word in line:
                        results.append(f'Word "{word}" found in line {line_number}: {line.strip()}')
        except FileNotFoundError:
            results.append(f'The file {file_path} does not exist.')
        return results

    def display_results(self, results):
        results_list = self.root.get_screen('main').ids.results_list
        results_list.clear_widgets()
        for result in results:
            results_list.add_widget(OneLineListItem(text=result))

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

if __name__ == '__main__':
    WordSearchApp().run()
