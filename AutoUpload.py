import sys
import os
import time
import tempfile
import subprocess
import json
import pdb

#todo config file
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
	
def getFilePrefix():
	filename = os.listdir(framesDirectory + '\\')[0]
	characterIndex = 0
	while True:
		if filename[characterIndex] == '.':
			break
		characterIndex = characterIndex + 1
	return str(filename[:characterIndex])



# watch directory for frames

if len(sys.argv) < 2:
	exit("No frame directory supplied. Drag frame folder onto program.")

programDirectory = os.path.dirname(sys.argv[0])
print ('program directory:' + programDirectory)
framesDirectory = str(sys.argv[1])
lastframeCount = 0
currentFrameCount = 0

while True:
	lastframeCount = currentFrameCount
	currentFrameCount = getFrameCount()

	if (lastframeCount == currentFrameCount):
		break

	print('Last frame count: ' + str(lastframeCount))
	print('Current frame count: ' + str(currentFrameCount))
	time.sleep(1)


# when frames are no longer being created, convert

#read config file
pdb.set_trace()
with open(programDirectory + '\Config.json') as data_file:
 	data = json.load(data_file)

videoFramerate = '-r ' + data['Properties']['Framerate'] + ' '
print ('framerate: ' + videoFramerate)

#todo specifiy framerate
fullBatchPath = programDirectory + '\\' + 'ffmpeg.exe '
parameter1 = '-f image2 '
inputFile = '-i ' + '"' + framesDirectory + '\\' + getFilePrefix() + r'.%%04d' + getFileType() + '" '

outputFile = 'C:\Users\Cameron\AppData\Local\Temp\out.mp4'

# Create temporary batch file to call ffmpeg
tempBatFile = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
tempBatFile.write(fullBatchPath + parameter1 + inputFile + outputFile)
tempBatFile.close()
print(tempBatFile.name)

subprocess.call(tempBatFile.name)

os.remove(tempBatFile.name)

# upload to youtube

