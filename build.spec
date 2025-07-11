# myscript.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('src/gui/images/svg_icons/*', 'src/gui/images/svg_icons'),
    ('src/gui/images/svg_images/*', 'src/gui/images/svg_images'),
    ('src/gui/themes/*', 'src/gui/themes'),
    ('src/settings.json', 'src'),
    ('src/gui/locales/*', 'src/gui/locales')],
    hiddenimports=['getpass', 'secrets', 'asyncio', 'uuid', 'cryptography', 
                    'cryptography.x509', 'cryptography.hazmat.primitives.kdf.pbkdf2'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='DBtective',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='logo.ico')