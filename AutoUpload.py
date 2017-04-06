import sys
import os
import time
import tempfile
import subprocess
import json
import pdb
import logging
import re

#todo cut first and last frame
#todo account for frames not starting at 0

def getFrameCount():
	return len(os.listdir(framesDirectory))

def getFileType():
	filename = os.listdir(framesDirectory + '\\')[0]
	characterIndex = len(filename) - 1
	while True:
		if filename[characterIndex] == '.':
			break
		characterIndex = characterIndex - 1
	return str((filename[characterIndex:]))
	
def getFilePrefix(filename):
	# filename = os.listdir(framesDirectory + '\\')[0]
	characterIndex = 0
	while True:
		if filename[characterIndex] == '.':
			break
		characterIndex = characterIndex + 1
	return str(filename[:characterIndex])

#todo handle mismatch with only 2 files (could cause infinite loop)
def getLastFrameName():
	dirList = os.listdir(framesDirectory)
	dirList.sort()
	currentLastFileSearchIndex = 1
	while True:
		lastFrameName = dirList[len(dirList) - currentLastFileSearchIndex]
		if getFilePrefix(lastFrameName) == getFilePrefix(os.listdir(framesDirectory + '\\')[0]): #if the prefixes of the first and last file match
			return lastFrameName
		currentLastFileSearchIndex = currentLastFileSearchIndex + 1

def log(logMessage):
	logging.debug(time.strftime("%H%M%S", time.localtime()) + ': ' + logMessage)
	print(logMessage)

def shutdown():
	exit('Program ended. Press any key to close window.')

# watch directory for frames

if len(sys.argv) < 2:
	log('No frame directory supplied. Drag frame folder onto program.')
	shutdown()

programDirectory = os.path.dirname(sys.argv[0])
framesDirectory = str(sys.argv[1])
lastframeCount = 0
currentFrameCount = 0

# Setup log file for each session
logging.basicConfig(filename=programDirectory + '\log-' + time.strftime("%H%M%S%d%m%y", time.localtime()) + '.log',level=logging.DEBUG)

log('Frame directory: ' + framesDirectory)

#read config file
with open(programDirectory + '\Config.json') as data_file:
 	data = json.load(data_file)

#todo handle missing config file

while True:
	lastframeCount = currentFrameCount
	currentFrameCount = getFrameCount()

	if (lastframeCount == currentFrameCount):
		break

	print('Last frame count: ' + str(lastframeCount))
	print('Current frame count: ' + str(currentFrameCount))
	sleepInterval = float(data['Properties']['FrameDirectoryWatchInterval'])
	time.sleep(sleepInterval)


if currentFrameCount < float(data['Properties']['MinimumFrameCount']):
	log('Error: Supplied frame directory has fewer than MinimumFrameCount files after waiting for the FrameDirectoryWatchInterval in config.json. Either select the correct directory or increase FrameDirectoryWatchInterval time')
	shutdown()

log('Found ' + str(currentFrameCount) + ' frames in directory. Starting sequence creation...')

# delete last frame
lastFrameName = getLastFrameName()
print(framesDirectory +'\\'+ lastFrameName)
print(framesDirectory + r'\\_' + lastFrameName)
os.rename(framesDirectory +'\\'+ lastFrameName, framesDirectory + r'\\_' + lastFrameName)


# when frames are no longer being created, convert
#todo set output resolution from config

fullBatchPath = programDirectory + '\\' + 'ffmpeg.exe '
videoFramerate = '-r ' + data['Properties']['Framerate'] + ' '
parameter1 = '-f image2 -start_number 2 '
inputFile = '-i ' + '"' + framesDirectory + '\\' + getFilePrefix(os.listdir(framesDirectory + '\\')[0]) + r'.%%04d' + getFileType() + '" '

outputFileDir = tempfile.gettempdir()+ '\\'
outputFileName = 'render-'+ time.strftime("%H%M%S%d%m%y", time.localtime()) +'.mp4'
outputFile = outputFileDir + outputFileName

# Create temporary batch file to call ffmpeg
tempBatFile = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
tempBatFile.write(fullBatchPath + videoFramerate + parameter1 + inputFile + outputFile)
tempBatFile.close()

log('Batch arguments: ' + fullBatchPath + videoFramerate + parameter1 + inputFile + outputFile)
log('Batch file created.')

print(tempBatFile.name)

subprocess.call(tempBatFile.name)

log('Batch program returned')

#remove temp batch file
os.remove(tempBatFile.name)

# move video out of temp directory into the directory of the script
os.rename(outputFile, programDirectory + '\\' + outputFileName)
log('Output video moved to ' + programDirectory + '\\' + outputFileName)

# upload to youtube

