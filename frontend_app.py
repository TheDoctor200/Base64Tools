## Imports

import flet as ft
import os
import subprocess
import platform
import base64
import pyperclip
import requests

def main(page: ft.Page):
    # Setting window icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "B64_icon.ico")
    page.window_icon = icon_path

    # Enforce dark theme
    page.theme_mode = ft.ThemeMode.DARK
    
    page.title = "Base64 Toolbox"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.spacing = 20
    page.bgcolor = ft.colors.BLUE_GREY_900

    txt_input = ft.TextField(
        label="Input", 
        width=400, 
        multiline=True, 
        border_color=ft.colors.BLUE_ACCENT,
        text_style=ft.TextStyle(color=ft.colors.WHITE)  # Adjust text color
    )
    
    txt_output = ft.TextField(
        label="Output", 
        width=400, 
        disabled=True, 
        expand=True, 
        multiline=True, 
        border_color=ft.colors.GREEN_ACCENT,
        text_style=ft.TextStyle(color=ft.colors.WHITE)  # Adjust text color
    )
    
    encoding_type = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="utf-8", label="UTF-8", fill_color=ft.colors.BLUE_ACCENT),
                ft.Radio(value="ascii", label="ASCII", fill_color=ft.colors.BLUE_ACCENT),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

## Definitions of the properties 

    def process_text(input_text: str, encoding: str, is_encrypt: bool) -> str:
        try:
            if is_encrypt:
                encoded_text = input_text.encode(encoding)
                encrypted_text = base64.b64encode(encoded_text).decode("ascii")
                return encrypted_text
            else:
                decoded_text = base64.b64decode(input_text).decode(encoding)
                return decoded_text
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
        txt_output.value = "Copied to clipboard!"
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
                        ft.Text("No Internet Connection", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ],
                    spacing=8,
                ),
                content=ft.Text("Please check your internet connection and try again.", color=ft.colors.WHITE),
                actions=[
                    ft.ElevatedButton("OK", on_click=close_dialog),
                ],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

## New Page add Buttons to decrypt, and so on.. 

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(name=icon_path, size=32, color=ft.colors.WHITE),
                            ft.Text("Base64 Toolbox", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=ft.colors.WHITE),
                    ft.Row(
                        [
                            ft.Text("Encoding:", color=ft.colors.WHITE),
                            encoding_type,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row([txt_input]),
                    ft.Row([ft.ElevatedButton("Encrypt", on_click=encrypt_click, color=ft.colors.GREEN)]),
                    ft.Row([txt_output]),
                    ft.Row([ft.ElevatedButton("Decrypt", on_click=decrypt_click, color=ft.colors.RED)]),
                    ft.Row([ft.ElevatedButton("Copy", on_click=copy_click, color=ft.colors.BLUE)]),
                    ft.Row(
                        [
                            ft.Text("Created by TheDoctor", size=12, color=ft.colors.WHITE),
                            ft.Icon(name=ft.icons.ROCKET_LAUNCH_OUTLINED, color=ft.colors.CYAN_200),
                            ft.ElevatedButton("Check for App Update", on_click=update_click, color=ft.colors.ORANGE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=10,
        )
    )

## End Code 
ft.app(target=main)



