import os
import base64
import pyperclip
import flet as ft
import webbrowser

def main(page: ft.Page):
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "B64_icon.ico")
    page.window_icon = icon_path
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Base64 Toolbox"
    page.bgcolor = ft.Colors.SURFACE
    page.window_width = 600
    page.window_height = 500

    def show_toast(message: str, color: str = ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    txt_input = ft.TextField(
        label="Input Text",
        multiline=True,
        border_radius=8,
        border_color=ft.Colors.CYAN_500,
        text_style=ft.TextStyle(color=ft.Colors.ON_SURFACE),
        expand=True,
    )

    txt_output_container = ft.Container(
        content=ft.Text(
            value="Output will appear here...",
            selectable=True,
            color=ft.Colors.ON_SURFACE,
            size=16,
            weight=ft.FontWeight.NORMAL,
        ),
        padding=ft.Padding(10, 10, 10, 10),
        border=ft.border.all(1, ft.Colors.CYAN_500),
        border_radius=8,
        width=page.window_width * 0.8,
        height=100,
        alignment=ft.alignment.center,
    )

    method_selection = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="base64", label="Base64", fill_color=ft.Colors.CYAN_500),
                ft.Radio(value="ascii", label="ASCII", fill_color=ft.Colors.CYAN_500),
                ft.Radio(value="utf-8", label="UTF-8", fill_color=ft.Colors.CYAN_500),
                ft.Radio(value="caesar", label="Caesar", fill_color=ft.Colors.CYAN_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        value="base64",
    )
    
    method_selection.value = "base64"
    
    shift_input = ft.TextField(
        label="Caesar Shift (Default: 3)",
        value="3",
        width=100,
        border_radius=8,
        border_color=ft.Colors.CYAN_500,
        text_style=ft.TextStyle(color=ft.Colors.ON_SURFACE),
    )

    def process_text(input_text: str, method: str, is_encrypt: bool) -> str:
        try:
            if method == "ascii":
                return " ".join(str(ord(char)) for char in input_text) if is_encrypt else "".join(chr(int(num)) for num in input_text.split())
            elif method == "base64":
                return base64.b64encode(input_text.encode("utf-8")).decode("ascii") if is_encrypt else base64.b64decode(input_text).decode("utf-8")
            elif method == "utf-8":
                return " ".join(str(byte) for byte in input_text.encode("utf-8")) if is_encrypt else bytes(map(int, input_text.split())).decode("utf-8")
            elif method == "caesar":
                shift = int(shift_input.value) if shift_input.value.isdigit() else 3
                return "".join(
                    chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else chr((ord(char) - 97 + shift) % 26 + 97) if char.islower() else char
                    for char in input_text
                ) if is_encrypt else "".join(
                    chr((ord(char) - 65 - shift) % 26 + 65) if char.isupper() else chr((ord(char) - 97 - shift) % 26 + 97) if char.islower() else char
                    for char in input_text
                )
        except Exception as ex:
            return f"Error: {ex}"

    def encrypt_click(e):
        txt_output_container.content.value = process_text(txt_input.value, method_selection.value, True)
        page.update()

    def decrypt_click(e):
        txt_output_container.content.value = process_text(txt_input.value, method_selection.value, False)
        page.update()

    def copy_click(e):
        pyperclip.copy(txt_output_container.content.value)
        show_toast("Output copied to clipboard!")

    def open_update_link(e):
        webbrowser.open("https://github.com/TheDoctor200/Base64Tools/releases/latest")

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Icon(name="ROCKET_LAUNCH_SHARP", size=32, color=ft.Colors.WHITE),
                        ft.Text("Base64 Toolbox", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(color=ft.Colors.WHITE),
                    method_selection,
                    shift_input,
                    txt_input,
                    ft.Row([
                        ft.ElevatedButton("Encrypt", on_click=encrypt_click, color=ft.Colors.LIGHT_GREEN_500),
                        ft.ElevatedButton("Decrypt", on_click=decrypt_click, color=ft.Colors.RED_500),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    txt_output_container,
                    ft.ElevatedButton("Copy to Clipboard", on_click=copy_click, color=ft.Colors.CYAN_400),
                    ft.Row([
                        ft.Container(
                            content=ft.ElevatedButton("Update App", on_click=open_update_link, color=ft.Colors.AMBER_500),
                            alignment=ft.alignment.bottom_right,
                            padding=ft.Padding(10, 10, 10, 10),
                        ),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Container(
                        content=ft.Text(
                            value="Made by TheDoctor",
                            color=ft.Colors.WHITE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.alignment.bottom_right,
                        padding=ft.Padding(10, 10, 10, 10),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=ft.Colors.SURFACE,
            border_radius=10,
            expand=True,
        )
    )

ft.app(target=main, view=ft.FLET_APP, assets_dir="assets")