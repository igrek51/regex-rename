# regex-rename
Regular expressions bulk rename tool for multiple files

[![GitHub version](https://badge.fury.io/gh/igrek51%2Fregex-rename.svg)](https://github.com/igrek51/regex-rename)
[![PyPI version](https://badge.fury.io/py/regex-rename.svg)](https://pypi.org/project/regex-rename)
[![Build Status](https://travis-ci.org/igrek51/regex-rename.svg?branch=master)](https://travis-ci.org/igrek51/regex-rename)
[![codecov](https://codecov.io/gh/igrek51/regex-rename/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/regex-rename)

# Quickstart
Renaming multiple files at once:
```shell
$ ls
01.mp3  02.mp3

$ regex-rename --rename '(\d+).mp3' '\1_Greatest_Hits.mp3'
[2021-03-04 00:27:23] [DEBUG] matching regex pattern testing_mode=False pattern=(\d+).mp3 replacement=\1_Greatest_Hits.mp3 full_match=False padding=None
[2021-03-04 00:27:23] [INFO ] renaming file from=01.mp3 to=01_Greatest_Hits.mp3
[2021-03-04 00:27:23] [INFO ] renaming file from=02.mp3 to=02_Greatest_Hits.mp3
[2021-03-04 00:27:23] [INFO ] files renamed count=2

$ ls
01_Greatest_Hits.mp3  02_Greatest_Hits.mp3
```

# Usage
enter `regex-rename` for help:

```shell
$ regex-rename 
regex-rename v0.1.1 (nuclear v1.1.5) - Regular expressions bulk rename tool for multiple files

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
  --pad-to PAD_TO             - Applies padding with zeros with given length on matched numerical groups
```

# Installation
```shell
pip3 install regex-rename
```

Requirements:

* Python 3.6 (or newer) with pip

# Example

Imagine you've got audio files awfully named like this:
- `Stanis▯aw+Lem+Invincible+(1).mp3`
- `Stanis▯aw+Lem+Invincible+(2 ).mp3`
- `Stanisław_Lem_Invincible (3) .mp3`
- ...
- `Stanis▯aw+Lem+Invincible+(51).mp3`

and you want to rename all of them in a manner `01 The Invincible.mp3` (extracting number from the end and put it at the beginning and padding it to 2 digits by the way).

## Step 1: Testing matching pattern 

Our Regex pattern to match those files and extract number from parentheses should be like this: `.+\((\d+) ?\).+`

Let's test matching pattern: `regex-rename '.+\((\d+) ?\).+'`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-1.png?raw=true)    
Notice that regex groups are extracted in logs.

## Step 2: Testing replacement pattern

We'd like to replace all files to a pattern: `\1 The Invincible.mp3` (`\1` is a first extracted group from matching pattern).
Regex can't easily pad numbers with zeros. Fortunately, we can use `--pad-to=2` to obtain 2-digit numbers

Let's test it: `regex-rename '.+\((\d+) ?\).+' '\1 The Invincible.mp3' --pad-to=2`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-2.png?raw=true)  

## Step 3: Actual renaming

All above commands were just testing our patterns so that we could experiment with regex patterns. Only when we're sure that everything is matched correctly, we can use `--rename` flag which does the actual renaming:  
`regex-rename '.+\((\d+) ?\).+' '\1 The Invincible.mp3' --pad-to=2 --rename`  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-3.png?raw=true)  

From now files are named properly:
- `01 The Invincible.mp3`
- `02 The Invincible.mp3`
- `03 The Invincible.mp3`
- ...
- `51 The Invincible.mp3`


# Beyond the Regex
`regex-rename` also supports some transformations not covered by regular expressions standard:
- Converting to lowercase by adding `\L` before group number:  
`regex-rename '([A-Z]+).mp3' '\L\1.mp3'`
- Converting to uppercase by adding `\U` before group number:  
`regex-rename '([a-z]+).mp3' '\U\1.mp3'`
- Padding numbers with zeros by specifying `--pad-to` parameter:  
`regex-rename '(\d+).mp3' '\1.mp3' --pad-to=2`
