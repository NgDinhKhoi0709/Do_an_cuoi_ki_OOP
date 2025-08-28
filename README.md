## Battle Legends (OOP Project)

An OOP-based 2D fighting game built with Python, Pygame, and OpenCV.

Repository: [`NgDinhKhoi0709/Do_an_cuoi_ki_OOP`](https://github.com/NgDinhKhoi0709/Do_an_cuoi_ki_OOP)

### Features
- **Menu, Tutorial, Character Selection, Pause, Winner screens** with video backgrounds
- **Three characters**: Warrior, Wizard, Hero (sprite-sheet animations)
- **Sound effects and background music**

### Requirements
Install with:
```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```text
pygame
opencv-python
pillow
```

### How to Run
Run from the repository root to ensure asset paths resolve correctly.

- Preferred (module mode):
```bash
python -m assets.main
```

- Alternatively (script mode):
```bash
python assets/main.py
```

### Controls
- Player 1: A/D to move, W to jump, T/Y to attack
- Player 2: Left/Right to move, Up to jump, Numpad 2/3 to attack
- ESC to Pause

### Project Structure
```text
Do_an_cuoi_ki_OOP/
  assets/
    audio/
    fonts/
    images/
      background/
      hero/
      warrior/
      wizard/
    __init__.py
    button.py
    fighter.py
    main.py        # Entry point (also runnable via `python -m assets.main`)
    merge.py       # Utility: build combined sprite sheet for Hero
    docstring.py   # Utility: print docstrings from main module
  README.md
  requirements.txt
```

### Notes on Asset Paths
- `assets/main.py` now resolves files relative to its own folder, so running from any working directory works.
- If you add new assets, place them under `assets/` and reference them via the same relative layout as existing files.

### Development Tips
- Use module mode (`python -m assets.main`) to avoid import/path issues.
- Keep sprite-sheet frame sizes consistent when updating character sprites.

### Credits
- Code, assets organization and documentation based on the repository at [`NgDinhKhoi0709/Do_an_cuoi_ki_OOP`](https://github.com/NgDinhKhoi0709/Do_an_cuoi_ki_OOP).


