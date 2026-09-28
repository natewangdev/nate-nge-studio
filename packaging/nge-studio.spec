# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller onedir spec for NGE-STUDIO."""

from pathlib import Path

block_cipher = None
root = Path(SPECPATH).resolve().parent  # packaging/ → repo root is parent? 
# SPECPATH is packaging/ when running from packaging/nge-studio.spec
repo = Path(SPECPATH).resolve().parent

a = Analysis(
    [str(repo / "src" / "nge_studio" / "__main__.py")],
    pathex=[str(repo / "src")],
    binaries=[],
    datas=[(str(repo / "game_scripts"), "game_scripts")],
    hiddenimports=["nge2", "PySide6"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NGE-STUDIO",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="NGE-STUDIO",
)
