import os
import subprocess
import platform
import base64
import pyperclip
import requests
import flet as ft


def main(page: ft.Page):
    # Setting window icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "B64_icon.ico")
    page.window_icon = icon_path

    # Enforce dark theme with a modern look
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Base64 Toolbox"
    page.bgcolor = ft.Colors.SURFACE  # Corrected to a valid color

    # Helper function for status notifications
    def show_toast(message: str, color: str = ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    # Text Input
    txt_input = ft.TextField(
        label="Input Text",
        multiline=True,
        border_radius=8,
        border_color=ft.Colors.CYAN_500,
        text_style=ft.TextStyle(color=ft.Colors.ON_SURFACE),
        expand=True,
    )

    # Output display with increased size
    txt_output = ft.Text(
        value="Output will appear here...",
        selectable=True,
        color=ft.Colors.ON_SURFACE,
        size=16,
        weight=ft.FontWeight.NORMAL,
    )

    # Encoding method selection (Base64, ASCII, Caesar)
    method_selection = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="base64", label="Base64", fill_color=ft.Colors.CYAN_500),
                ft.Radio(value="ascii", label="ASCII", fill_color=ft.Colors.CYAN_500),
                ft.Radio(value="caesar", label="Caesar", fill_color=ft.Colors.CYAN_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        value="base64",
    )

    # Caesar cipher shift input
    shift_input = ft.TextField(
        label="Caesar Shift (Default: 3)",
        value="3",
        width=100,
        border_radius=8,
        border_color=ft.Colors.CYAN_500,
        text_style=ft.TextStyle(color=ft.Colors.ON_SURFACE),
    )

    # Function to process Base64, ASCII, and Caesar
    def process_text(input_text: str, method: str, is_encrypt: bool) -> str:
        try:
            if method == "ascii":
                if is_encrypt:
                    return " ".join(str(ord(char)) for char in input_text)
                else:
                    return "".join(chr(int(num)) for num in input_text.split())
            elif method == "base64":
                if is_encrypt:
                    encoded_text = input_text.encode("utf-8")
                    return base64.b64encode(encoded_text).decode("ascii")
                else:
                    decoded_bytes = base64.b64decode(input_text)
                    return decoded_bytes.decode("utf-8")
            elif method == "caesar":
                shift = int(shift_input.value) if shift_input.value.isdigit() else 3
                if is_encrypt:
                    return caesar_cipher(input_text, shift)
                else:
                    return caesar_cipher(input_text, -shift)
        except Exception as ex:
            return f"Error: {ex}"

    # Caesar cipher logic
    def caesar_cipher(text: str, shift: int) -> str:
        result = []
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
            else:
                result.append(char)
        return "".join(result)

    # Encryption function
    def encrypt_click(e):
        input_text = txt_input.value.strip()
        if not input_text:
            show_toast("Please enter input text", color=ft.Colors.RED)
            return
        method = method_selection.value
        result = process_text(input_text, method, True)
        update_output(result)
        show_toast("Text encrypted successfully!")

    # Decryption function
    def decrypt_click(e):
        input_text = txt_input.value.strip()
        if not input_text:
            show_toast("Please enter input text", color=ft.Colors.RED)
            return
        method = method_selection.value
        result = process_text(input_text, method, False)
        update_output(result)
        show_toast("Text decrypted successfully!")

    # Function to update the output display
    def update_output(result: str):
        txt_output.value = result if result else "Output will appear here..."
        page.update()

    # Copy function
    def copy_click(e):
        pyperclip.copy(txt_output.value)
        show_toast("Output copied to clipboard!")

    # Add components to the page
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(name="info", size=32, color=ft.Colors.WHITE),
                            ft.Text("Base64 Toolbox", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=ft.Colors.WHITE),
                    ft.Row(
                        [
                            ft.Text("Method:", color=ft.Colors.WHITE),
                            method_selection,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Text("Caesar Shift:", color=ft.Colors.WHITE),
                            shift_input,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        txt_input,
                        width=page.window.width * 0.8,
                        margin=ft.Margin(0, 10, 0, 10),
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.ElevatedButton("Encrypt", on_click=encrypt_click, color=ft.Colors.LIGHT_GREEN_500),
                                border_radius=8,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton("Decrypt", on_click=decrypt_click, color=ft.Colors.RED_500),
                                border_radius=8,
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column([txt_output]),
                        width=page.window.width * 0.8,
                        height=150,
                        padding=ft.Padding(10, 10, 10, 10),
                        bgcolor=ft.Colors.ON_SURFACE_VARIANT,  # Adjusted to use a valid color
                        border_radius=8,
                        alignment=ft.alignment.center_left,
                    ),
                    ft.Container(
                        content=ft.ElevatedButton("Copy to Clipboard", on_click=copy_click, color=ft.Colors.CYAN_400),
                        border_radius=8,
                        expand=False,
                        width=150,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=ft.Colors.SURFACE,  # Corrected to valid color
            border_radius=10,
            expand=True,
        )
    )


# Start the app
ft.app(target=main)





