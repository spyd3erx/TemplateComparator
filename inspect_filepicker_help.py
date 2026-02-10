import flet as ft
import importlib.metadata
import sys

try:
    print(f"Flet version: {importlib.metadata.version('flet')}")
except Exception as e:
    print(f"Error getting version: {e}")

print("\nFilePicker help:")
try:
    help(ft.FilePicker)
except Exception as e:
    print(f"Error getting help: {e}")
