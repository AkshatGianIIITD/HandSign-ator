# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Homepage.py'],
    pathex=[],
    binaries=[],
    datas=[('Aldrich', 'Aldrich'), ('Lato', 'Lato'), ('Montserrat', 'Montserrat'), ('data_alphabets', 'data_alphabets'), ('bg.jpg', '.'), ('bg2.jpg', '.'), ('34.jpg', '.'), ('beep-329314.mp3', '.'), ('best.pt', '.'), ('best (2).pt', '.'), ('best1.pt', '.'), ('sign_translator.kv', '.')],
    hiddenimports=['kivy_deps.angle', 'kivy_deps.sdl2', 'kivy_deps.glew', 'kivy_deps.gstreamer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Homepage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
