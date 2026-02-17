from __future__ import annotations

from functions.cli import ask_choice, ask_yes_no, print_menu, show_help
from functions.convert import ConversionPlan, clear_fonts_used, convert_fonts
from functions.paths import build_paths, ensure_directories, list_ttf_files
from functions.naming import build_output_name, family_suffixes, parse_all
import sys


def handle_conversion() -> None:
    dirs = build_paths()
    ensure_directories(dirs)

    ttf_files = list_ttf_files(dirs)
    if not ttf_files:
        print("\nNo .ttf files found in fonts_ttf.")
        return

    fonts = parse_all([p.name for p in ttf_files])
    families = sorted({f.family for f in fonts})
    print("\nDetected families: " + " | ".join(families))

    # Naming preference: numeric vs text weight labels.
    use_numeric = ask_yes_no("Prefer numeric weight labels (900) instead of text (Black)?", default=False)

    # Suffix decision per family (only if all share the same suffix).
    suffix_map = family_suffixes(fonts)
    drop_suffix_families: set[str] = set()
    for family in families:
        suffixes = suffix_map.get(family, set())
        if len(suffixes) == 1:
            suffix_value = next(iter(suffixes))
            if ask_yes_no(f"Remove suffix '_{suffix_value}' from family {family}?", default=True):
                drop_suffix_families.add(family)

    plans: list[ConversionPlan] = []
    for font in fonts:
        drop = font.family in drop_suffix_families
        output_name = build_output_name(font, use_numeric=use_numeric, drop_suffix=drop)
        plans.append(ConversionPlan(source_name=font.filename, family=font.family, output_name=output_name))

    successes, failures = convert_fonts(dirs, plans)

    if successes:
        print("\nFiles generated in font_lib:")
        for out_path in successes:
            print(f"- {out_path.name}")
    if failures:
        print("\nConversion failures:")
        for path, reason in failures:
            print(f"- {path.name}: {reason}")


def handle_clear_used() -> None:
    dirs = build_paths()
    ensure_directories(dirs)
    removed = clear_fonts_used(dirs)
    print(f"Removed {removed} file(s) from fonts_used.")


def main() -> int:
    import multiprocessing as _mp
    # Support multiprocessing in frozen executables on Windows
    if getattr(sys, "frozen", False):
        _mp.freeze_support()

    dirs = build_paths()
    ensure_directories(dirs)

    while True:
        print_menu()
        choice = ask_choice()
        if choice == "1":
            handle_conversion()
        elif choice == "2":
            handle_clear_used()
        elif choice == "3":
            show_help()
        elif choice == "0":
            print("Exiting...")
            return 0
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    raise SystemExit(main())
