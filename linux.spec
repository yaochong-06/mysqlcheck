
# -*- mode: python ; coding: utf-8 -*-
import sys
import os.path as osp

sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['start.py','data.py','doc.py','mysqlutil.py','binlog2sql.py','binlog2sql_util.py'],
             pathex=['/root/MyCheck'],
             binaries=[],
             datas=[('/root/MyCheck/static','static')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['zmq'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='start',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
