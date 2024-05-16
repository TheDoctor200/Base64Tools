import flet as ft
import os
import subprocess
import platform
import base64
import pyperclip
import requests

def main(page: ft.Page):
    page.window_icon = ft.Icon("B64_icon.ico")
    page.title = "Base64 Toolbox"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_input = ft.TextField(label="Input", width=400)
    txt_output = ft.TextField(label="Output", width=400, disabled=True, expand=True)
    encoding_type = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="utf-8", label="UTF-8"),
                ft.Radio(value="ascii", label="ASCII"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    def process_text(input_text: str, encoding: str, is_encrypt: bool) -> str:
        try:
            if encoding == "ascii":
                if is_encrypt:
                    encoded_text = input_text.encode("ascii")
                    encrypted_text = base64.b64encode(encoded_text).decode("ascii")
                else:
                    decoded_text = base64.b64decode(input_text.encode("ascii")).decode("ascii")
                    return decoded_text
            else:
                if is_encrypt:
                    encoded_text = input_text.encode(encoding)
                    encrypted_text = base64.b64encode(encoded_text).decode("ascii")
                else:
                    decoded_text = base64.b64decode(input_text.encode(encoding)).decode(encoding)
                    return decoded_text
            return encrypted_text if is_encrypt else decoded_text
        except ValueError as e:
            return f"Error: {e}"
        except Exception as ex:
            return f"Error: {ex}"

    def encrypt_click(e):
        input_text = txt_input.value
        if not input_text:
            txt_output.value = "Please enter input text"
            page.update()
            return
        encoding = encoding_type.value
        txt_output.value = process_text(input_text, encoding, True)
        page.update()

    def decrypt_click(e):
        input_text = txt_input.value
        if not input_text:
            txt_output.value = "Please enter input text"
            page.update()
            return
        encoding = encoding_type.value
        txt_output.value = process_text(input_text, encoding, False)
        page.update()

    def copy_click(e):
        pyperclip.copy(txt_output.value)
        txt_output.value = ""
        page.update()

    def is_internet_available():
        try:
            requests.head("http://www.google.com/", timeout=1)
            return True
        except requests.ConnectionError:
            return False

    def update_click(e):
        if is_internet_available():
            try:
                if platform.system() == 'Windows':
                    os.startfile('update_app.py')
                else:
                    subprocess.call(['python3', 'update_app.py'])
            except Exception as e:
                print(f"Error opening update_app.py: {e}")
        else:
            def close_dialog(e):
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                modal=True,
               title=ft.Row(
            [
                ft.Icon(name=ft.icons.WIFI_OFF, color=ft.colors.RED_500),
                ft.Text("No Internet Connection"),
            ],
            spacing=8,
        ),
                content=ft.Text("Please check your internet connection and try again."),
                actions=[
                    ft.ElevatedButton("OK", on_click=close_dialog),
                ],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Base 64 Toolbox", size=32, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Text("Encoding:"),
                        encoding_type,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([ft.Text("Input:"), txt_input]),
                ft.Row([ft.ElevatedButton("Encrypt", on_click=encrypt_click)]),
                ft.Row([ft.Text("Output:"), txt_output]),
                ft.Row([ft.ElevatedButton("Decrypt", on_click=decrypt_click)]),
                ft.Row([ft.ElevatedButton("Copy", on_click=copy_click)]),
                ft.Row(
                    [
                        ft.Text("Created by TheDoctor", size=12, color=ft.colors.WHITE),
                        ft.Icon(name=ft.icons.ROCKET_LAUNCH_OUTLINED, color=ft.colors.BLUE_200),
                        ft.ElevatedButton("Check for App Update", on_click=update_click)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)