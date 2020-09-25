from PIL import Image
from pathlib import Path

for file_path in Path('C:\\Users\\bjoern\\data\\raw\\mushrooms').glob('**/*.jpg'):
    print('Check: %s' % file_path)

    im = Image.open(file_path)
    im.verify()

    print('Done.')
