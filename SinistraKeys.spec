# -*- mode: python ; coding: utf-8 -*-
# Sinistra Keys - PyInstaller Spec File
# kidD Icarus / kidDicarus Inc.

import os

# Get the directory where this spec file is located
spec_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['sinistra_keys_v4.py'],
    pathex=[spec_dir],
    binaries=[],
    datas=[],
    hiddenimports=['rtmidi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SinistraKeys',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # THIS IS THE KEY - NO CONSOLE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists(os.path.join(spec_dir, 'icon.ico')) else None,
)
