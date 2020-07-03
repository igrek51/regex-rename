# regex-rename
Regular expressions bulk rename tool for multiple files

[![GitHub version](https://badge.fury.io/gh/igrek51%2Fregex-rename.svg)](https://github.com/igrek51/regex-rename)
[![PyPI version](https://badge.fury.io/py/regex-rename.svg)](https://pypi.org/project/regex-rename)
[![Build Status](https://travis-ci.org/igrek51/regex-rename.svg?branch=master)](https://travis-ci.org/igrek51/regex-rename)
[![codecov](https://codecov.io/gh/igrek51/regex-rename/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/regex-rename)

# Usage
enter `regex-rename` for help:

```shell
$ regex-rename 
regex-rename v0.1.0 (nuclear v1.1.5) - Regular expressions bulk rename tool for multiple files

Usage:
regex-rename [OPTIONS] PATTERN [REPLACEMENT]

Arguments:
   PATTERN       - Regex pattern to match filenames
   [REPLACEMENT] - Replacement regex pattern for renamed files. Use \1, \2 syntax to make use of matched groups

Options:
  --version                   - Print version information and exit
  -h, --help [SUBCOMMANDS...] - Display this help and exit
  --rename                    - Does actual renaming files instead of just testing replacement pattern
  --full                      - Enforces matching full filename against pattern
```

# Installation
```shell
pip3 install regex-rename
```

Requirements:

* Python 3.6 (or newer) with pip

# Example

Imagine you've got audio files awfully named like this:
- `Stanis▯aw+Lem+Niezwyci▯▯ony+(0001).mp3`
- `Stanis▯aw+Lem+Niezwyci▯▯ony+(0002).mp3`
- ...
- `Stanis▯aw+Lem+Niezwyci▯▯ony+(0051).mp3`

and you want to rename all of them in manner `01-Niezwyciężony.mp3` (extracting number from the end and put it at the beginning and shortening it to 2 digits by the way).

## Step 1: Testing matching pattern 

Our Regex pattern to match those files and extract 2 digit number should be like this: `.+\(00(\d{2})\).+`

Let's test matching pattern:  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-1.png?raw=true)    
Notice that regex groups are extracted in logs.

## Step 2: Testing replacement pattern

We'd like to replace all files to a pattern: `\1-Niezwyciężony.mp3` (`\1` is a first extracted group from matching pattern)

Let's test it:  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-2.png?raw=true)  

## Step 3: Actual renaming

All above commands were just testing our patterns so that we could experiment with regex patterns. Only when we're sure that everything is matched correctly, we can use `--rename` flag which does the actual renaming:  
![Usage example](https://github.com/igrek51/regex-rename/blob/master/docs/img/screen-3.png?raw=true)  

After that files are named properly:
- `01-Niezwyciężony.mp3`
- `02-Niezwyciężony.mp3`
- ...
- `51-Niezwyciężony.mp3`
