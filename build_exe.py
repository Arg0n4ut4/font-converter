from __future__ import annotations

from cx_Freeze import Executable, setup

APP_NAME = "font-converter"
VERSION = "1.0.0"
DESCRIPTION = "CLI to convert TTF to WOFF2 (subset U+000-5FF)."

build_options = {
    "includes": ["fontTools.subset", "brotli"],
    # include_files accepts a list of paths or (src, dest) tuples
    "include_files": ["logo.ico", ("licenses", "licenses")],
    "optimize": 1,
}

executables = [
    Executable(
        "main.py",
        base="Console",
        target_name=f"{APP_NAME}.exe",
        icon="logo.ico",
    )
]

setup(
    name=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    options={"build_exe": build_options},
    executables=executables,
)
