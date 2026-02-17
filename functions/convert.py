from __future__ import annotations

import re
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from multiprocessing import cpu_count
from pathlib import Path
from typing import Dict, List, Tuple

from fontTools import subset as ft_subset
from functions.paths import Dirs


@dataclass(frozen=True)
class ConversionPlan:
    source_name: str  # filename in fonts_ttf
    family: str
    output_name: str  # name without extension


def sanitize_filename(name: str) -> str:
    trimmed = name.strip()
    without_ext = re.sub(r"\.(ttf|woff2)$", "", trimmed, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", without_ext)
    cleaned = cleaned.strip("-._")
    return cleaned or "font"


def reserve_output_path(base_dir: Path, desired_name: str) -> Path:
    base = sanitize_filename(desired_name)
    candidate = base_dir / f"{base}.woff2"
    counter = 1
    while candidate.exists():
        candidate = base_dir / f"{base}-{counter}.woff2"
        counter += 1
    return candidate


def reserve_destination(ttf_path: Path, target_dir: Path) -> Path:
    candidate = target_dir / ttf_path.name
    counter = 1
    while candidate.exists():
        stem = ttf_path.stem
        candidate = target_dir / f"{stem}-{counter}{ttf_path.suffix}"
        counter += 1
    return candidate


def subset_to_woff2(ttf_path: Path, out_path: Path) -> Tuple[bool, str]:
    args = [
        str(ttf_path),
        "--flavor=woff2",
        f"--output-file={out_path}",
        "--unicodes=U+000-5FF",
    ]

    try:
        # Use fontTools API directly to avoid spawning extra processes (fixes frozen builds).
        ft_subset.main(args)
        return True, ""
    except SystemExit as exc:
        code = exc.code
        if code in (0, None):
            return True, ""
        return False, str(code)
    except Exception as exc:  # pragma: no cover - defensive
        return False, str(exc)


def convert_fonts(dirs: Dirs, plans: List[ConversionPlan]) -> Tuple[List[Path], List[Tuple[Path, str]]]:
    successes: List[Path] = []
    failures: List[Tuple[Path, str]] = []

    families: Dict[str, List[ConversionPlan]] = {}
    for plan in plans:
        families.setdefault(plan.family, []).append(plan)

    total = len(plans)
    done = 0
    lock = threading.Lock()

    def process_family(family: str, family_plans: List[ConversionPlan]) -> None:
        nonlocal done
        for plan in family_plans:
            ttf_path = dirs.fonts_ttf / plan.source_name
            if not ttf_path.exists():
                with lock:
                    failures.append((ttf_path, "TTF file not found."))
                    done += 1
                continue

            family_dir = dirs.font_lib / plan.family
            family_dir.mkdir(parents=True, exist_ok=True)
            output_path = reserve_output_path(family_dir, plan.output_name)
            output_path = reserve_output_path(family_dir, plan.output_name)
            ok, msg = subset_to_woff2(ttf_path, output_path)
            with lock:
                if ok:
                    successes.append(output_path)
                    dest = reserve_destination(ttf_path, dirs.fonts_used)
                    shutil.move(str(ttf_path), dest)
                else:
                    failures.append((ttf_path, msg or "Unknown failure."))
                done += 1

    try:
        try:
            max_workers = max(1, cpu_count() - 2)
        except Exception:
            max_workers = 1
        max_workers = max(1, min(len(families), max_workers))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for family, family_plans in families.items():
                executor.submit(process_family, family, family_plans)

    finally:
        pass

    return successes, failures


def clear_fonts_used(dirs: Dirs) -> int:
    removed = 0
    if dirs.fonts_used.exists():
        for item in dirs.fonts_used.iterdir():
            if item.is_file():
                item.unlink()
                removed += 1
    return removed
