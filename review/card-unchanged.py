from pathlib import Path
import hashlib
print('Card screen byte-identical:',Path('review/revision-before/screen-4.png').read_bytes()==Path('review/after/screen-4.png').read_bytes())
