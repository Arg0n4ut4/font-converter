# Font Converter (TTF -> WOFF2 subset)

CLI to convert `.ttf` to `.woff2` using `pyftsubset` (fontTools) with Brotli compression and subset `U+000-5FF` (ASCII + Latin-1 + common accents). Detects Google Fonts naming pattern (as of 2026-02-16) and organizes output by family.

## Libraries used

- fonttools (pyftsubset)

## Release (Windows executable)

- A Windows build is available: https://github.com/Arg0n4ut4/font-converter/releases/tag/v1.0.0
- Primary distribution in Releases: a ZIP containing the full `build/` output (recommended). You must download and extract the ZIP `font-converter-win-x64-v1.0.0.zip`.

## Quick start — Windows (downloaded build ZIP)

1. Download the ZIP `font-converter-win-x64-v1.0.0.zip` from the Release above and extract it to a folder.
2. Run `font-converter.exe` from the extracted folder (double-click or run from PowerShell):

```powershell
.
\font-converter.exe
```

3. On first run the program will create these folders beside the executable: `fonts_ttf`, `font_lib`, `fonts_used`.

## Quick start — Linux / macOS (run from source)

The code runs on Linux and macOS when executed from source. The simplest cross-platform option is to run the Python source instead of installing a native binary.

1. Install a recent Python (3.10+; use same major used to develop, e.g. 3.13 if available).
2. Create and activate a virtual environment:

Linux/macOS (bash/zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

macOS (fish):

```fish
python -m venv .venv
source .venv/bin/activate.fish
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the program:

```bash
python main.py
```

## Notes and troubleshooting (macOS / Linux)

- `fonttools` and `brotli` are cross-platform. `pip install` normally installs prebuilt wheels, but on older systems `brotli` may need compilation. If installation fails, install system build tools:
  - Debian/Ubuntu: `sudo apt install build-essential python3-dev`
  - Fedora: `sudo dnf install @development-tools python3-devel`
  - macOS: install Xcode Command Line Tools: `xcode-select --install`
- If running from source, ensure you use a supported Python version and the virtualenv is activated.
- If creating native builds on Linux/macOS with `cx_Freeze`, run the same `python build_exe.py build` on the target OS; the produced binary is specific to that OS.

## Build (developer)

To build a Windows executable:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build_exe.py build
```

To build on Linux/macOS, run the same commands but use the shell activation shown above; the produced binary will be native for the build OS.

## License and legal

This project is released under the MIT License. See `LICENSE` for details.

## Security & responsibility

- This tool performs font conversions. Users are responsible for ensuring they have rights to modify or redistribute any fonts they process.
- Executables are not code-signed; Windows may show SmartScreen warnings for unsigned binaries.

## Files and structure (quick)

- `main.py` — CLI entrypoint and menu.
- `functions/` — conversion logic, naming helpers and path utils.
- `build_exe.py` — cx_Freeze build script.
- `requirements.txt` — runtime/build dependencies.

## Links

- Releases: https://github.com/Arg0n4ut4/font-converter/releases
- fonttools: https://github.com/fonttools/fonttools
- brotli: https://github.com/google/brotli
