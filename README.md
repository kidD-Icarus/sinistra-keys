# Sinistra Keys

**MIDI RTL/LTR Keyboard Reverser for Notatio Sinistra**

by kidD Icarus / kidDicarus Inc.

---

## What is this?

Sinistra Keys reverses MIDI keyboard input for right-to-left (RTL) music notation reading. Part of the **Notatio Sinistra** system for musicians who naturally process music from right to left.

## Features

- **Multi-keyboard support** — up to 6 keyboards simultaneously
- **Independent routing** — each keyboard → own virtual port → own DAW track
- **Dual center mapping** — set Physical center (what your keyboard sends) and Target center (what you want to hear)
- **RTL/LTR toggle** — switch modes per keyboard
- **Real-time note display** — see input → output transformation
- **Cross-platform** — Mac (IAC Driver) + Windows (loopMIDI)

## Installation

```bash
pip install -r requirements.txt
python sinistra_keys_v4.py
```

## Requirements

- Python 3.8+
- python-rtmidi
- PyQt6
- Virtual MIDI driver:
  - **Windows**: [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
  - **Mac**: IAC Driver (built-in, enable in Audio MIDI Setup)

## Setup

### Windows (loopMIDI)

1. Install loopMIDI
2. Create virtual ports: `Sinistra_1`, `Sinistra_2`, etc.
3. In your DAW, enable these as MIDI inputs
4. In Sinistra Keys:
   - **In**: Your physical keyboard
   - **Out**: Sinistra_X port
   - **Phys**: What note your middle key sends (e.g., E3)
   - **Target**: What note you want to hear (e.g., C4)

### Mac (IAC Driver)

1. Open Audio MIDI Setup
2. Window → Show MIDI Studio
3. Double-click IAC Driver → Enable
4. Add ports as needed
5. Configure in Sinistra Keys same as above

## How It Works

**Formula:** `output = physical_center + target_center - input`

If your keyboard sends E3 when you press the physical middle key, and you want that to play C4:
- Phys = E3 (52)
- Target = C4 (60)
- E3 input → C4 output
- Everything else mirrors around that mapping

## Branding

- **Colors**: Crimson (#8B0000) + Gold (#DAA520)
- **Logo**: k.I. (kidDicarus Inc.)

## License

MIT

---

**kidD Icarus • kidDicarus Inc. • Notatio Sinistra**
