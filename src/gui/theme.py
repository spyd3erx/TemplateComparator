"""Theme and color constants for the Flet GUI."""

import flet as ft

# ── Color Palette ──
PRIMARY = "#0D6EFD"  # Blue - primary actions
PRIMARY_DARK = "#0A58CA"  # Darker blue - hover states
SURFACE = "#FFFFFF"  # White - cards and surfaces
BACKGROUND = "#F0F2F5"  # Light gray - app background
TEXT_PRIMARY = "#1A1D23"  # Near-black - main text
TEXT_SECONDARY = "#6B7280"  # Gray - secondary text
BORDER = "#E2E5EA"  # Light border
SUCCESS = "#10B981"  # Green - success states
ERROR = "#EF4444"  # Red - error states
WARNING = "#F59E0B"  # Amber - warnings

# ── Typography ──
FONT_FAMILY = "Segoe UI"
HEADING_SIZE = 26
SUBHEADING_SIZE = 16
BODY_SIZE = 14
CAPTION_SIZE = 12

# ── Spacing & Radius ──
CARD_RADIUS = 12
BUTTON_RADIUS = 8
PADDING_LG = 32
PADDING_MD = 20
PADDING_SM = 12
PADDING_XS = 8


def get_light_theme() -> ft.Theme:
    """Returns the light theme for the application."""
    return ft.Theme(
        color_scheme_seed=PRIMARY,
        font_family=FONT_FAMILY,
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            on_primary=SURFACE,
            surface=SURFACE,
        ),
    )
