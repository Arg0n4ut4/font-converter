from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class Dirs:
    root: Path
    font_lib: Path
    fonts_ttf: Path
    fonts_used: Path


def build_paths(root: Path | None = None) -> Dirs:
    if root:
        base = Path(root).resolve()
    elif getattr(sys, "frozen", False):
        # Executable (cx_Freeze): use the executable folder as base.
        base = Path(sys.executable).resolve().parent
    else:
        base = Path(__file__).resolve().parent.parent
    return Dirs(
        root=base,
        font_lib=base / "font_lib",
        fonts_ttf=base / "fonts_ttf",
        fonts_used=base / "fonts_used",
    )


def ensure_directories(dirs: Dirs) -> None:
    # Ensure base folders exist before any operation.
    for folder in (dirs.font_lib, dirs.fonts_ttf, dirs.fonts_used):
        folder.mkdir(parents=True, exist_ok=True)


def list_ttf_files(dirs: Dirs) -> list[Path]:
    # List only TTF files directly under fonts_ttf.
    return sorted(dirs.fonts_ttf.glob("*.ttf"))
