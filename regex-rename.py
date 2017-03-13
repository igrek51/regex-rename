#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import sys
import os
import re

# Text formatters characters
C_RESET = '\033[0m'
C_BOLD = '\033[1m'
C_DIM = '\033[2m'
C_ITALIC = '\033[3m'
C_UNDERLINE = '\033[4m'

C_BLACK = 0
C_RED = 1
C_GREEN = 2
C_YELLOW = 3
C_BLUE = 4
C_MAGENTA = 5
C_CYAN = 6
C_WHITE = 7

def textColor(colorNumber):
	return '\033[%dm' % (30 + colorNumber)

C_INFO = textColor(C_BLUE) + C_BOLD
C_OK = textColor(C_GREEN) + C_BOLD
C_WARN = textColor(C_YELLOW) + C_BOLD
C_ERROR = textColor(C_RED) + C_BOLD
T_INFO = C_INFO + '[info]' + C_RESET
T_OK = C_OK + '[OK]' + C_RESET
T_WARN = C_WARN + '[warn]' + C_RESET
T_ERROR = C_ERROR + '[ERROR]' + C_RESET

def info(message):
	print(T_INFO + " " + message)

def ok(message):
	print(T_OK + " " + message)

def warn(message):
	print(T_WARN + " " + message)

def error(message):
	print(T_ERROR + " " + message)

def fatalError(message):
	error(message)
	sys.exit()

def shellExec(cmd):
	errCode = subprocess.call(cmd, shell=True)
	if errCode != 0:
		fatalError('failed executing: %s' % cmd)

def popArg(argsDict):
	args = argsDict['args']
	if len(args) == 0:
		return None
	next = args[0]
	argsDict['args'] = args[1:]
	return next

def printHelp():
	print('Usage:')
	print(' regex-rename [options] <pattern> [<replacement>]')
	print('\nOptions:')
	print(' -t, --test\t' + 'test matching pattern and replacement')
	print(' -h, --help\t' + 'display this help and exit')

testEnabled = False
pattern = None
replacement = None

argsDict = {'args': sys.argv[1:]}

if len(argsDict['args']) == 0:
	printHelp()
	sys.exit()

while len(argsDict['args']) > 0:
	arg = popArg(argsDict)
	# help message
	if arg == '-h' or arg == '--help':
		printHelp()
		sys.exit()
	# test matching pattern
	if arg == '-t' or arg == '--test':
		testEnabled = True
	else:
		if pattern is None:
			pattern = arg
		elif replacement is None:
			replacement = arg
		else:
			printHelp()
			fatalError('too many arguments')

# arguments validation
if pattern is None:
	printHelp()
	fatalError('No <pattern> defined')
if replacement is None and not testEnabled:
	printHelp()
	fatalError('No <replacement> defined')

if testEnabled:
	info('Testing matching pattern...')
	info('pattern: ' + pattern)
	if replacement is not None:
		info('replacement: ' + replacement)

matchedCount = 0

for filename in glob.glob('*'):

	try:
		# testing matching pattern first
		if re.match(pattern, filename) == None:
			if testEnabled:
				warn('pattern not matched for file: %s' % filename)
			continue

		matchedCount += 1

		# testing only matching pattern
		if replacement is None and testEnabled:
			ok('pattern matched for file: %s' % filename)
			continue

		# replacing pattern
		newName = re.sub(pattern, replacement, filename)

	except Exception as e:
		# catch invalid regex expressions
		fatalError(str(e))

	if testEnabled:
		ok('pattern matched: %s -> %s' % (filename, newName))
	else:
		info('renaming file: %s -> %s' % (filename, newName))
		# renaming file
		os.rename(filename, newName)

if testEnabled:
	info('Matched files: %d' % matchedCount)
else:
	info('Renamed files: %d' % matchedCount)
