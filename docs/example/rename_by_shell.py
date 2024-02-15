import os

from nuclear import shell

if __name__ == '__main__':
    os.chdir('tests/res/2mp3')
    shell('regex-rename "(\d+)\.(.+)" "\\1_Audio.\\2" --short', raw_output=True)
