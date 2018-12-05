# -*- mode: python -*-

block_cipher = None


a = Analysis(['ONU.py'],
             binaries=[],
             datas=[
             ('UNO_cards_deck.png', '.'),
             ('UNO_cards_deck_brighter2.png', '.'),
             ('poker_table.png', '.'),
             ('ONU_card_back.png', '.'),
             ('sans.ttf', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ONU',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
