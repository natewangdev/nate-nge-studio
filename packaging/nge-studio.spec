# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller onedir spec for NGE-STUDIO."""

from pathlib import Path

from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_dynamic_libs,
)

block_cipher = None
repo = Path(SPECPATH).resolve().parent

datas = [(str(repo / "game_scripts"), "game_scripts")]
binaries = []
hiddenimports = [
    "nge2",
    "PySide6",
    "rapidocr_onnxruntime",
    "onnxruntime",
    "cv2",
    "numpy",
]

# RapidOCR ships config.yaml + ONNX models as package data (not auto-detected).
datas += collect_data_files("rapidocr_onnxruntime")
# onnxruntime / OpenCV native bits commonly needed by NGE2 vision stack
binaries += collect_dynamic_libs("onnxruntime")
try:
    tmp_ret = collect_all("onnxruntime")
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except Exception:
    pass

a = Analysis(
    [str(repo / "src" / "nge_studio" / "__main__.py")],
    pathex=[str(repo / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name="NGE-STUDIO",
)
