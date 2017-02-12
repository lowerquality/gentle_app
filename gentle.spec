# -*- mode: python -*-

block_cipher = None
import os

data_files = []
for dirpath in ['www', 'exp']:
    data_files.append((dirpath, dirpath))
data_files.append(('ffmpeg', ''))
for extname in ['m3', 'k3']:
    data_files.append((os.path.join('ext', extname), 'ext'))

a = Analysis(['gentle.py'],
             pathex=[os.path.abspath(os.curdir)],
             binaries=None,
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gentle',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gentle')
app = BUNDLE(coll,
             name='gentle.app',
             icon='gentle.icns',
             bundle_identifier=None,
             info_plist={
                 'NSHighResolutionCapable': 'True'
             })

