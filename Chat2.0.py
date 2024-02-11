import TelaInicial
from TelaInicial import main
import flet as ft
if __name__ == "__main__":
    # Chame as funções diretamente

    TelaInicial.ft.app(target=main, view=ft.FLET_APP_WEB, assets_dir="assets")