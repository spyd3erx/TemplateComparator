"""Reusable UI widgets for the Flet GUI."""

import flet as ft
from . import theme as t


def app_card(content: ft.Control, padding: int = t.PADDING_MD) -> ft.Container:
    """Wraps content inside a styled card container."""
    return ft.Container(
        content=content,
        bgcolor=t.SURFACE,
        border_radius=t.CARD_RADIUS,
        border=ft.Border.all(1, t.BORDER),
        padding=padding,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )


def section_title(text: str) -> ft.Text:
    """Creates a styled section title."""
    return ft.Text(
        text,
        size=t.SUBHEADING_SIZE,
        weight=ft.FontWeight.W_600,
        color=t.TEXT_PRIMARY,
    )


def caption_text(text: str) -> ft.Text:
    """Creates styled caption text."""
    return ft.Text(
        text,
        size=t.CAPTION_SIZE,
        color=t.TEXT_SECONDARY,
    )


def primary_button(
    text: str,
    icon: str | None = None,
    on_click=None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.FilledButton:
    """Creates a styled primary action button."""
    return ft.FilledButton(
        content=ft.Text(text),
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        expand=expand,
        style=ft.ButtonStyle(
            color=t.SURFACE,
            bgcolor={
                ft.ControlState.DEFAULT: t.PRIMARY,
                ft.ControlState.HOVERED: t.PRIMARY_DARK,
                ft.ControlState.DISABLED: t.BORDER,
            },
            shape=ft.RoundedRectangleBorder(radius=t.BUTTON_RADIUS),
            padding=ft.Padding.symmetric(horizontal=24, vertical=14),
            text_style=ft.TextStyle(
                size=t.BODY_SIZE,
                weight=ft.FontWeight.W_600,
            ),
        ),
    )


def outlined_button(
    text: str,
    icon: str | None = None,
    on_click=None,
    expand: bool = False,
) -> ft.OutlinedButton:
    """Creates a styled outlined button."""
    return ft.OutlinedButton(
        content=ft.Text(text),
        icon=icon,
        on_click=on_click,
        expand=expand,
        style=ft.ButtonStyle(
            color=t.PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=t.BUTTON_RADIUS),
            side=ft.BorderSide(width=1.5, color=t.PRIMARY),
            padding=ft.Padding.symmetric(horizontal=24, vertical=14),
            text_style=ft.TextStyle(
                size=t.BODY_SIZE,
                weight=ft.FontWeight.W_600,
            ),
        ),
    )


def file_picker_field(
    label: str,
    value: str,
    hint: str = "Seleccionar archivo...",
    on_click=None,
) -> ft.Container:
    """Creates a styled file picker input row."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    label,
                    size=t.CAPTION_SIZE,
                    weight=ft.FontWeight.W_600,
                    color=t.TEXT_SECONDARY,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.DESCRIPTION_OUTLINED,
                                size=18,
                                color=t.TEXT_SECONDARY,
                            ),
                            ft.Text(
                                value if value else hint,
                                size=t.BODY_SIZE,
                                color=t.TEXT_PRIMARY if value else t.TEXT_SECONDARY,
                                expand=True,
                                no_wrap=True,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FOLDER_OPEN_OUTLINED,
                                icon_color=t.PRIMARY,
                                icon_size=20,
                                on_click=on_click,
                                tooltip="Explorar",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    bgcolor=t.BACKGROUND,
                    border_radius=t.BUTTON_RADIUS,
                    border=ft.Border.all(1, t.BORDER),
                    padding=ft.Padding.only(left=14, right=4, top=4, bottom=4),
                ),
            ],
            spacing=6,
        ),
    )


def status_badge(text: str, color: str, icon: str) -> ft.Container:
    """Creates a small colored badge for status display."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=14, color=color),
                ft.Text(
                    text, size=t.CAPTION_SIZE, color=color, weight=ft.FontWeight.W_600
                ),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, color),
        border_radius=20,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )
