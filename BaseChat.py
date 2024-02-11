import flet as ft
import time

def main_style():
    return {
        "width": 420,
        "height": 500,
        "bgcolor": "#141518",
        "border_radius": 10,
        "padding": 15,
    }

def prompt_style():
    return {
        "width": 420,
        "height": 40,
        "bgcolor": "black",
        "content_padding": 10,
        "cursor_color": "white",
    }

class Prompt(ft.TextField):
    def __init__(self, chat: ft.ListView):
        super().__init__(**prompt_style(), on_submit=self.run_prompt)
        self.chat = chat

    def animate_text_output(self, name: str, response: str):
        word_list: list = []
        msg = CreateMessage(name, "")
        self.chat.controls.append(msg)

        for word in list(response):
            word_list.append(word)
            msg.text.value = "".join(map(str, word_list))
            self.chat.update()
            time.sleep(0.008)

    def user_output(self, prompt):
        self.animate_text_output(name="Me", response=prompt)

    def assistant_output(self, prompt):
        response_text = "Resposta do assistente simulada."  # Substitua pela lógica desejada

        self.animate_text_output(name="Tintomax", response=response_text)

    def run_prompt(self, event):
        text = event.control.value
        self.user_output(prompt=text)
        self.assistant_output(prompt=text)

        self.value = ""
        self.update()

class MainContentArea(ft.Container):
    def __init__(self):
        super().__init__(**main_style())
        self.chat = ft.ListView(
            expand=True,
            height=200,
            spacing=15,
            auto_scroll=True
        )
        self.content = self.chat

class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        self.text = ft.Text(self.message)
        super().__init__(spacing=4)
        self.controls = [ft.Text(self.name, opacity=0.6), self.text]

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"

    main_content_area = MainContentArea()
    prompt = Prompt(chat=main_content_area.chat)

    page.add(
        ft.Text("Chat Simulado", size=28, weight="w800"),
        main_content_area,
        ft.Divider(height=6, color="transparent"),
        prompt,
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
