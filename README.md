# regex-rename

[![GitHub version](https://badge.fury.io/gh/igrek51%2Fregex-rename.svg)](https://github.com/igrek51/regex-rename)
[![PyPI version](https://badge.fury.io/py/regex-rename.svg)](https://pypi.org/project/regex-rename)
[![Build Status](https://travis-ci.org/igrek51/regex-rename.svg?branch=master)](https://travis-ci.org/igrek51/regex-rename)
[![codecov](https://codecov.io/gh/igrek51/regex-rename/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/regex-rename)
[![Github Pages](https://img.shields.io/badge/docs-github.io-blue)](https://igrek51.github.io/regex-rename)

Bulk rename tool based on regular expressions to rename multiple files at once.

## Quickstart
Renaming multiple files at once:
```shell
$ ls # awful names:
b45XDS-01.mp3  QsEW2s-02.mp3  VF7t6L-03.mp3

$ regex-rename '-(\d+).mp3' '\1_NeverGonnaGiveYouUp.mp3' --rename
[2022-04-09 09:19:15] DEBUG matching regex pattern pattern=-(\d+).mp3 replacement=\1_NeverGonnaGiveYouUp.mp3 full_match=False padding=None testing_mode=False
[2022-04-09 09:19:15] INFO  renaming file from=QsEW2s-02.mp3 to=02_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  renaming file from=VF7t6L-03.mp3 to=03_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  renaming file from=b45XDS-01.mp3 to=01_NeverGonnaGiveYouUp.mp3
[2022-04-09 09:19:15] INFO  files renamed count=3

$ ls # now we're talking:
01_NeverGonnaGiveYouUp.mp3  02_NeverGonnaGiveYouUp.mp3  03_NeverGonnaGiveYouUp.mp3
```

## Installation
```shell
pip3 install regex-rename
```

It requires Python 3.7 (or newer) with pip.

## Example

Imagine you've got audio files awfully named like this and you want to rename them:

- `Stanis▯aw+Lem+Invincible+(1).mp3` -> `01 The Invincible.mp3`
- `Stanis▯aw+Lem+Invincible+(2 ).mp3` -> `02 The Invincible.mp3`
- `Stanisław_Lem_Invincible (3) .mp3` -> `03 The Invincible.mp3`
- …
- `Stanis▯aw+Lem+Invincible+(51).mp3` -> `51 The Invincible.mp3`

Specifically, you want to extract the episode number, move it at the beginning,
and apply a 2-digit padding to it.

### Step 1: Check the matching pattern 

The Regex pattern to match these files and 
extract episode number from parentheses may be as follows: 
`(\d+).*mp3` 
(it contains a number and ends with `mp3`)

Let's check if the files are matched properly: `regex-rename '(\d+).*mp3'`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-1.png?raw=true)

Pay attention to the extracted regex groups.

### Step 2: Check the replacement pattern

We'd like to replace all files to a pattern: 
`\1 The Invincible.mp3` 
(`\1` is a first extracted group from matching pattern).

Regex can't easily pad numbers with zeros. 
Fortunately, we can use `--pad-to=2` parameter to obtain 2-digit numbers.

Let's test it by adding the replacement pattern: `regex-rename '(\d+).*mp3' '\1 The Invincible.mp3' --pad-to=2`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-2.png?raw=true)  

### Step 3: Actual renaming

All above commands were just testing our patterns so that we could experiment with regex patterns. 
Once we're sure that everything is matched correctly, we can use `--rename` flag, 
which does the actual renaming:  
`regex-rename '(\d+).*mp3' '\1 The Invincible.mp3' --pad-to=2 --rename`  
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


## Usage
enter `regex-rename` for help:

```shell
$ regex-rename 
regex-rename v1.0.0 (nuclear v1.2.3) - Bulk rename tool based on regular expressions to rename multiple files at once

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
  --pad-to PAD_TO             - Applies padding with zeros with given length on matched numerical groups
```
