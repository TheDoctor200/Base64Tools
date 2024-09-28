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

    # Enforce dark theme with a modern look
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Base64 Toolbox"
    page.bgcolor = ft.colors.SURFACE_VARIANT

    # Helper function for status notifications
    def show_toast(message: str, color: str = ft.colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
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
        border_color=ft.colors.CYAN_500,
        text_style=ft.TextStyle(color=ft.colors.ON_SURFACE_VARIANT),
        expand=True  # Make the input expand based on available space
    )

    # Output display (using ft.Text instead of ft.TextField)
    txt_output = ft.Text(
        value="Output will appear here...",
        selectable=True,  # Allows text to be copied
        width=page.window_width * 0.8,  # Responsive width based on window size
        color=ft.colors.ON_SURFACE_VARIANT,
        max_lines=None,  # Unlimited lines
        overflow="visible"  # Output can grow based on content
    )

    # Encoding type selection
    encoding_type = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="utf-8", label="UTF-8", fill_color=ft.colors.CYAN_500),
                ft.Radio(value="ascii", label="ASCII", fill_color=ft.colors.CYAN_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        value="utf-8",
    )

    # Function to process Base64
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

    # Encryption and decryption functions
    def encrypt_click(e):
        input_text = txt_input.value
        if not input_text:
            show_toast("Please enter input text", color=ft.colors.RED)
            return
        encoding = encoding_type.value
        txt_output.value = process_text(input_text, encoding, True)
        show_toast("Text encrypted successfully!")
        page.update()

    def decrypt_click(e):
        input_text = txt_input.value
        if not input_text:
            show_toast("Please enter input text", color=ft.colors.RED)
            return
        encoding = encoding_type.value
        txt_output.value = process_text(input_text, encoding, False)
        show_toast("Text decrypted successfully!")
        page.update()

    # Copy function
    def copy_click(e):
        pyperclip.copy(txt_output.value)
        show_toast("Output copied to clipboard!")

    # Function to check internet availability
    def is_internet_available():
        try:
            requests.head("http://www.google.com/", timeout=1)
            return True
        except requests.ConnectionError:
            return False

    # Update function
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

    # Add components to the page
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Title and logo
                    ft.Row(
                        [
                            ft.Icon(name=icon_path, size=32, color=ft.colors.WHITE),
                            ft.Text("Base64 Toolbox", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=ft.colors.WHITE),
                    # Encoding selection
                    ft.Row(
                        [
                            ft.Text("Encoding:", color=ft.colors.WHITE),
                            encoding_type,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    # Text input field (with full width expansion)
                    ft.Container(
                        txt_input,
                        width=page.window_width * 0.8,  # Responsive width based on window size
                        margin=ft.Margin(0, 10, 0, 10),  # Corrected margin to use four values
                    ),
                    # Encrypt and decrypt buttons with container for border radius
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Encrypt", 
                                    on_click=encrypt_click, 
                                    color=ft.colors.LIGHT_GREEN_500,
                                ),
                                border_radius=8,
                                expand=True,  # Button expands based on available space
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Decrypt", 
                                    on_click=decrypt_click, 
                                    color=ft.colors.RED_500,
                                ),
                                border_radius=8,
                                expand=True,  # Button expands based on available space
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    # Output display field
                    ft.Container(
                        txt_output,
                        width=page.window_width * 0.8,  # Responsive width based on window size
                        padding=ft.Padding(10, 10, 10, 10),  # Corrected padding with all sides specified
                        bgcolor=ft.colors.SURFACE_VARIANT,  # Background color for output
                        border_radius=8,
                        alignment=ft.alignment.center_left,
                    ),
                    # Copy button with container for border radius
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Copy to Clipboard", 
                            on_click=copy_click, 
                            color=ft.colors.CYAN_400,
                        ),
                        border_radius=8,
                        expand=True,  # Button expands based on available space
                    ),
                    # Footer
                    ft.Row(
                        [
                            ft.Text("Created by TheDoctor", size=12, color=ft.colors.WHITE),
                            ft.Icon(name=ft.icons.ROCKET_LAUNCH_OUTLINED, color=ft.colors.CYAN_200),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Check for App Update", 
                                    on_click=update_click, 
                                    color=ft.colors.ORANGE,
                                ),
                                border_radius=8,
                                expand=True,  # Button expands based on available space
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True  # Ensure column expands vertically
            ),
            padding=ft.Padding(20, 20, 20, 20),  # Corrected padding with four values
            bgcolor=ft.colors.SURFACE,
            border_radius=10,
            expand=True  # Ensure container expands with screen size
        )
    )

# Start the app
ft.app(target=main)














