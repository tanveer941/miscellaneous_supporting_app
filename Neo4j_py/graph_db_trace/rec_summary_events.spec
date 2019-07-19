# -*- mode: python -*-

block_cipher = None


a = Analysis(['rec_summary_events.py'],
             pathex=['D:\\TDSM\\MKS_integration_before\\TDSM_auth\\TF\\Graph_database\\Neo4js\\Neo4j_start\\Neo4j_py\\graph_db_trace'],
             binaries=[],
             datas=[],
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
          name='rec_summary_events',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='rec_summary_events')
