import os
import sys

import flet as ft
import time
import threading
from main import create_thread_and_run, wait_on_run, get_response, assistente_id, select_assistant


def main_style():
    return dict(width=550, height=300, bgcolor="black", border_radius=10, padding=15)


def prompt_style():
    return dict(width=550, height=40, bgcolor="black", content_padding=10, cursor_color="white")


class Prompt(ft.TextField):
    def __init__(self, page: ft.Page, chat: ft.ListView, timer_text: ft.Text, menuCheck: ft.Text,
                 progress_bar: ft.ProgressBar):
        super().__init__(**prompt_style(), on_submit=self.run_prompt)
        self.chat = chat
        self.page = page
        self.last_assistant_message = ""
        self.timer_text = timer_text
        self.start_time = 0
        self.timer_thread = None
        self.menuCheck = menuCheck
        self.selected_assistant_id = assistente_id
        self.progress_bar = progress_bar

    def start_timer(self):
        self.start_time = time.time()
        self.running_timer = True  # Flag para controlar o loop da thread
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while self.running_timer:
            elapsed_time = time.time() - self.start_time
            self.timer_text.value = f"Tempo: {elapsed_time:.2f} segundos"
            self.timer_text.update()
            time.sleep(0.1)

    def stop_timer(self):
        self.running_timer = False

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
        self.animate_text_output(name="Você:", response=prompt)

    def assistant_output(self, prompt):
        self.show_progress_bar()
        thread, run = create_thread_and_run(prompt, self.selected_assistant_id)
        run = wait_on_run(run, thread)
        messages = get_response(thread)

        # Processa a resposta
        for msg in messages.data:
            if msg.role == 'assistant':
                response_text = msg.content[0].text.value
                self.animate_text_output(name="Assistente:", response=response_text)
                self.last_assistant_message = response_text

                break
        self.hide_progress_bar()
        self.stop_timer()

    def run_prompt(self, event):
        self.start_timer()
        text = event.control.value
        self.user_output(prompt=text)
        self.assistant_output(prompt=text)

        self.value = ""
        self.update()
        return text

    def dropdown_changed(self, event):
        selected_assistant = event.control.value  # Corrigido para acessar o valor correto
        self.chat.controls = []
        self.selected_assistant_id = select_assistant(selected_assistant)  # função importada de main.py
        self.menuCheck.value = f"Assistente selecionado: {selected_assistant}"
        self.menuCheck.update()

    def show_progress_bar(self):
        self.progress_bar.visible = True
        self.progress_bar.update()

    def hide_progress_bar(self):
        self.progress_bar.visible = False
        self.progress_bar.update()


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

    def clear_chat(self):
        self.chat.controls = []  # Limpa a lista de mensagens
        self.chat.update()


class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        ##self.text = ft.TextField(value=self.message, read_only=True, border=None, bgcolor="transparent", text_size=15)
        self.text = ft.Text(self.message)
        super().__init__(spacing=4)
        self.controls = [ft.Text(self.name, opacity=0.6), self.text]


def main(page: ft.Page):
    # Pagina ChatBot
    page.title = "Assistentes"
    page.favicon = "assets/favicon.ico"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    page.window_center()
    page.window_width = 600
    page.window_height = 750
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    progress_bar = ft.ProgressBar(visible=False, width=100)
    menuCheck = ft.Text()
    timer_text = ft.Text(value="Tempo: 0.00 segundos")
    main_content_area = MainContentArea()
    prompt = Prompt(page, chat=main_content_area.chat, timer_text=timer_text, menuCheck=menuCheck,
                    progress_bar=progress_bar)

    dd = ft.Dropdown(
        on_change=prompt.dropdown_changed,
        options=[
            ft.dropdown.Option("Chat"),
        ],
        text_size=12,
        width=100,  # Largura do Dropdown
        height=50,  # Altura do Dropdown (opcional)
    )

    copy_button = ft.ElevatedButton(
        text="Copiar Última Mensagem do Assistente",
        on_click=lambda _: page.set_clipboard(prompt.last_assistant_message),
        color="white",
        bgcolor="#070708"
    )

    # Botão para limpar a conversa
    clear_button = ft.ElevatedButton(text="Limpar Conversa", color="white", bgcolor="#070708",
                                     on_click=lambda _: main_content_area.clear_chat())

    button_row = ft.Row(
        controls=[clear_button, copy_button],
        alignment="Center"
    )

    Assis_Esc = ft.Text("Escolha o assistente:", size=15, width=140, height=20, color="white")

    tit_row = ft.Row(
        controls=[Assis_Esc, dd],
        alignment="Center",
    )

    def resource_path(relative_path):
        """ Retorna o caminho do recurso para o sistema de arquivos ou o executável """
        try:
            # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    icons_path = resource_path("assets/icons/icon")

    def close_window(event):
        page.window_close()

    #Botões de maximizar e minimizar(adicionar ao appBar)
    '''
    def min_win(event):
        page.window_full_screen = False
        page.update()

    def max_win(event):
        page.window_full_screen = True
        page.update()
    '''

    def page2():
        page22: ft.Page
        page.window_visible = False
        page.update()

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(icon=ft.icons.MENU, text="Sobre", on_click=page2),
        ]
    )


    close_button = ft.IconButton(ft.icons.CLOSE, on_click=close_window)
    #min_button = ft.IconButton(ft.icons.MINIMIZE, on_click=min_win)
    barWin = ft.WindowDragArea(ft.Container(bgcolor='transparent', padding=10), width=470)
    #max_button = ft.IconButton(ft.icons.MAXIMIZE, on_click=max_win)

    appbar = ft.AppBar(
        toolbar_height=35,
        leading=pb,
        bgcolor="transparent",
        actions=[barWin, close_button]
    )

    page.add(
        appbar,
        ft.Image(src=icons_path),
        ft.Text("Assistente", size=18, height=50, color="white", weight=ft.FontWeight.W_900),
        tit_row,
        main_content_area,
        ft.Divider(height=2, color="transparent"),
        progress_bar,
        ft.Divider(height=2, color="transparent"),
        prompt,
        button_row,
        timer_text,
        menuCheck,
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")
