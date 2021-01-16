from pathlib import Path
for fp in Path('.').iterdir():
     if fp.is_dir():
         for _fp in fp.iterdir():
             print(f'processing {_fp.name}')
             with open(_fp, 'b', encoding='utf8') as reader:
                 md.seek(2)
                 md = reader.read().strip()
             with open(_fp, 'w', encoding='utf8') as writer:
                 writer.write(md)
                 