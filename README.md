# regex-rename

[![GitHub version (latest SemVer)](https://img.shields.io/github/v/tag/igrek51/regex-rename?label=github&sort=semver)](https://github.com/igrek51/regex-rename)
[![PyPI](https://img.shields.io/pypi/v/regex-rename)](https://pypi.org/project/regex-rename)
[![Github Pages](https://img.shields.io/badge/docs-github.io-blue)](https://igrek51.github.io/regex-rename)
[![codecov](https://codecov.io/gh/igrek51/regex-rename/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/regex-rename)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/igrek51/regex-rename/test.yml?branch=master&label=tests)](https://github.com/igrek51/regex-rename/actions?query=workflow%3Atest)

Bulk rename tool based on regular expressions to rename multiple files at once.

## Quickstart
Renaming multiple files at once:
```shell
$ ls # awful names:
b45XDS-01.mp3  QsEW2s-02.mp3  VF7t6L-03.mp3

$ regex-rename '-(\d+).mp3' '\1_NeverGonnaGiveYouUp.mp3' --rename
[2022-04-09 09:19:15] DEBUG matching regular expression pattern to files: pattern=-(\d+).mp3 replacement=\1_NeverGonnaGiveYouUp.mp3 full_match=False dry_run=False
[2022-04-09 09:19:15] INFO  renaming file: from=b45XDS-01.mp3 to=01_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  renaming file: from=QsEW2s-02.mp3 to=02_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  renaming file: from=VF7t6L-03.mp3 to=03_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  files renamed: renamed=3 mismatched=0

$ ls # now we're talking:
01_NeverGonnaGiveYouUp.mp3  02_NeverGonnaGiveYouUp.mp3  03_NeverGonnaGiveYouUp.mp3
```

## Installation
```shell
pip3 install regex-rename
```

It requires Python 3.7 (or newer) with pip.

## Tutorial

Imagine you have 51 audio files with hideous names like this and you wish to rename them:

- `Stanislaw+Lem+Invincible+(01).mp3` -> `01 The Invincible.mp3`
- `Stanis▯aw+Lem+Invincible+(02 ).mp3` -> `02 The Invincible.mp3`
- `Stanisław_Lem_Invincible (03) .mp3` -> `03 The Invincible.mp3`
- …
- `Stanis▯aw+Lem+Invincible+(51).mp3` -> `51 The Invincible.mp3`

Specifically, you want to place the episode number at the beginning.

### Step 1: Match 

Regular Expressions can be tricky.
We figured out this pattern may match the files and extracts the episode number:
```regexp
(\d+).*mp3
``` 

First, let's check this pattern in a dry run: `regex-rename '(\d+).*mp3'`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-1.png?raw=true)

Pay attention to the extracted regex groups.

### Step 2: Replace

Now, we'd like to replace all files to a pattern: 
```regexp
\1 The Invincible.mp3
``` 
`\1` is a first group extracted by the matching pattern (episode number).

Let's test it by adding the replacement pattern: `regex-rename '(\d+).*mp3' '\1 The Invincible.mp3'`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-2.png?raw=true)  

### Step 3: Execute

All above commands were just dry-run so that we could experiment with regex patterns.
Once we're sure that everything is matched correctly, we can append `--rename` flag, 
which does the actual renaming:  
`regex-rename '(\d+).*mp3' '\1 The Invincible.mp3' --rename`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-3.png?raw=true)  

Finally, files are named properly:

- `01 The Invincible.mp3`
- `02 The Invincible.mp3`
- `03 The Invincible.mp3`
- …
- `51 The Invincible.mp3`

## Beyond the Regex
`regex-rename` also supports some transformations not covered by regular expressions standard:

- Converting to lowercase by adding `\L` before group number:  
`regex-rename '([A-Z]+).mp3' '\L\1.mp3'`  
eg. `AUDIO.mp3` to `audio.mp3`
- Converting to uppercase by adding `\U` before group number:  
`regex-rename '([a-z]+).mp3' '\U\1.mp3'`  
eg. `audio.mp3` to `AUDIO.mp3`
- Padding numbers with leading zeros by adding `\P2`, `\P3`, … (depending on padding length) before group number:  
`regex-rename '(\d+).mp3' '\P2\1.mp3'`  
eg. `1.mp3` to `01.mp3`
- Padding numbers with leading zeros by specifying `--pad-to` parameter:  
`regex-rename '(\d+).mp3' '\1.mp3' --pad-to=2`  
eg. `1.mp3` to `01.mp3`

## More examples

- Extract season and episode numbers, eg. `episode-02x05.mkv` to `S02E05.mkv`:  
  ```shell
  regex-rename '(\d+)x(\d+)' 'S\1E\2.mkv' --rename
  ```
  
- Swap artist with title, eg. `Echoes - Pink Floyd.mp3` to `Pink Floyd - Echoes.mp3`:  
  ```shell
  regex-rename '([^-]+) - ([^-]+)\.mp3' '\2 - \1.mp3' --rename
  ```
  
- Pad leading zeros, eg. `1.mp3` to `001.mp3`:  
  ```shell
  regex-rename '(\d+).mp3' '\P3\1.mp3' --rename
  ```
  
- Convert to lowercase, eg. `SONG.MP3` to `song.mp3`:  
  ```shell
  regex-rename '(.+)' '\L\1' --rename
  ```
  
- Convert to uppercase, eg. `Tool.mp3` to `TOOL.mp3`:  
  ```shell
  regex-rename '(.+)\.mp3' '\U\1.mp3' --rename
  ```
  
- Add prefix, eg. `Doors.mp3` to `The Doors.mp3`:  
  ```shell
  regex-rename '(.+)' 'The \1' --full --rename
  ```
  
- Change extension, eg. `Songbook.apk` to `Songbook.zip`:  
  ```shell
  regex-rename '(.+)\.apk' '\1.zip' --rename
  ```
  
- Turn directories into prefixes and move files, eg. `Pink Floyd/Echoes.mp3` to `Pink Floyd - Echoes.mp3`:  
  ```shell
  regex-rename '(.+)/(.+).mp3' '\1 - \2.mp3' --full --recursive --rename
  ```
  
- Rename files in different directories, preserving their parent directories,
  eg. `app/logs/file-001.log` to `app/logs/file_001.txt`:  
  ```shell
  regex-rename '(.*)/file-([0-9]+).log' '\1/file_\2.txt' --full --recursive --rename
  ```

- Rename files piped from another command like `find`,
  eg. `songs/Jimmi - Voodoo Child.mp3` to `songs/Jimi - Voodoo Child.mp3`:  
  ```shell
  find -iname '*jimmi*' | regex-rename '(.*)/.* - (.*).mp3$' '\1/Jimi - \2.mp3' --rename
  ```


## Usage
Enter `regex-rename` for help:

```shell
$ regex-rename 
regex-rename v1.3.0 - Bulk rename tool based on regular expressions to rename multiple files at once

Usage:
regex-rename [OPTIONS] PATTERN [REPLACEMENT]

Arguments:
   PATTERN       - Regex pattern to match filenames
   [REPLACEMENT] - Replacement regex pattern for renamed files. Use \1, \2 syntax to make use of matched groups

Options:
  --version                   - Print version information and exit
  -h, --help [SUBCOMMANDS...] - Display this help and exit
  -r, --rename                - Does actual renaming files instead of just testing replacement pattern
  --full                      - Enforces matching full filename against pattern
  --recursive                 - Search directories recursively
  --collate                   - Compare source filenames with the replaced names
  --pad-to PAD_TO             - Applies padding with zeros with given length on matched numerical groups
```
