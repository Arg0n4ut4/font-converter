
MENU_TEXT = """
[1] Convert and rename TTF -> WOFF2 (subset U+000-5FF)
[2] Clear fonts_used folder
[3] Help
[0] Exit
""".strip()

HELP_TEXT = """
============================
Usage
============================
- Put .ttf files in fonts_ttf.
- Run option 1 to rename and generate .woff2 into font_lib (by family subfolder), moving converted .ttf files to fonts_used.
- Use option 2 to clear fonts_used when you want to restart.
- You can keep your font library here and copy to your projects or organize in your own folders as needed.

============================
Naming
============================
- Detects Google Fonts naming pattern (as of 2026-02-16): Family[_suffix]-WeightItalic.
- Asks once per family if all files share the same suffix after '_' to drop it; if a family has mixed suffixes, all suffixes are kept to avoid collisions.
- Asks if you prefer numeric weights (e.g., 900) or textual weights (e.g., Black); Italic is appended when present.
- Output names include the suffix when it is not dropped; different suffixes in the same family are always preserved.

============================
Subsetting
============================
- Uses pyftsubset flavor=woff2, unicodes=U+000-5FF (ASCII + Latin-1 + common accents), compression brotli.
- Typical reduction: large TTF -> much smaller WOFF2 subset.

============================
Folders
============================
- fonts_ttf: input TTFs you want to convert.
- font_lib: output WOFF2 files, organized in subfolders by family.
- fonts_used: original TTFs that were already converted.
""".strip()


def print_menu() -> None:
    print("\n=== TTF -> WOFF2 Converter ===")
    print(MENU_TEXT)


def ask_choice() -> str:
    raw = input("Choice: ").strip()
    return raw


def show_help() -> None:
    print("\n" + HELP_TEXT + "\n")
    input("Press Enter to return to menu...")


def ask_yes_no(question: str, default: bool = False) -> bool:
    hint = "Y/n" if default else "y/N"
    answer = input(f"{question} [{hint}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"s", "sim", "y", "yes"}
