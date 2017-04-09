import sys
import os
import time
import tempfile
import subprocess
import json
import pdb
import logging
import shutil

#todo cut first and last frame
#todo account for frames not starting at 0

class FFmpegObject:
	fullBatchPath = ''
	videoFramerate = ''
	parameter1 = ''
	inputFile = ''
	outputFileDir = ''
	outputFileName = ''
	outputFile = ''

	def createBatchFile(self):
		# Create temporary batch file to call ffmpeg
		tempBatFile = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
		tempBatFile.write(bytes(self.fullBatchPath + self.videoFramerate + self.parameter1 + self.inputFile + self.outputFile, 'UTF-8'))
		tempBatFile.close()

		log('Batch arguments: ' + self.fullBatchPath + self.videoFramerate + self.parameter1 + self.inputFile + self.outputFile)
		log('Batch file created.')

		print(tempBatFile.name)

		subprocess.call(tempBatFile.name)

		log('Batch program returned')

		#remove temp batch file
		os.remove(tempBatFile.name)

#copy all frames to a temp location
#determine the filetype of the frames
#remove any files that aren't of that type
#sort the frames into alphabetical order
#top and tail the frames
#rename the frames into an ordered sequence
class FramePrep:
	
	framesDirectory = ''
	tempFramesDirectory = ''
	filePrefix = ''
	fileNumberinglength = ''
	fileSuffix = ''

	def __init__(self, frameDir):
		self.framesDirectory = frameDir
		self.copyTempFrames()
		self.determineFrameAttributes()
		self.removeNonFrameObjects()
		self.getSortedFrameList()
		self.topAndTail()
		self.renameFramesToSortedList()
		shutdown()

	#copy only image files to temp directory
	def copyTempFrames(self):
		suffixes = ('.png', '.jpg', '.jpeg', '.tga', '.tiff')
		if not os.path.isdir(framesDirectory + "\\temp\\"):
			os.mkdir(framesDirectory + "\\temp\\")
		self.tempFramesDirectory = self.framesDirectory + "\\temp\\"
		for file in os.listdir(self.framesDirectory):
			if file.endswith(suffixes):
				shutil.copy(self.framesDirectory + '\\' + file, self.tempFramesDirectory + file)
			else:
				print('File ' + file + ' was not copied')
		return

	def determineFrameAttributes(self):
		tempFilename = os.listdir(self.tempFramesDirectory)[0]
		print (os.listdir(self.tempFramesDirectory)[0]) 

		#get the file extension
		characterIndex = len(tempFilename) - 1
		while True:
			if tempFilename[characterIndex] == '.':
				break
			characterIndex = characterIndex - 1
		self.fileSuffix = str((tempFilename[characterIndex:]))

		tempFilename = str((tempFilename[:characterIndex]))
		print(tempFilename)

		#find how many sequence numbers exist
		characterIndex = len(tempFilename) - 1
		numeralDigits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
		while True:
			if not tempFilename[characterIndex] in numeralDigits:
				break
			characterIndex = characterIndex - 1
		self.fileNumberinglength = (len(tempFilename) - 1) - characterIndex

		self.filePrefix = str((tempFilename[:characterIndex + 1]))
		print('numbering length: ' + str(self.fileNumberinglength))
		print(tempFilename)		

		#FirstPersonExampleMap.0001.jpg
		return

	def removeNonFrameObjects(self):
		return

	def getSortedFrameList(self):
		return

	def topAndTail(self):
		topAmount = data['Properties']['NumStartingFramesToSkip']
		tailAmount = data['Properties']['NumEndingFramesToSkip']
		currentTrimAmount = 0
		while True:
			if currentTrimAmount == topAmount:
				break
			print(os.listdir()[0])
			#os.remove(os.listdir()[0])
			currentTrimAmount = currentTrimAmount + 1
		return

	def renameFramesToSortedList(self):
		return

def prepareFrames(framesDirectory):
	framePrepObject = FramePrep(framesDirectory)

def convertFramesToVideo(ffmpegCall):
	ffmpegCall.fullBatchPath = programDirectory + '\\' + 'ffmpeg.exe '
	ffmpegCall.videoFramerate = '-r ' + data['Properties']['Framerate'] + ' '
	ffmpegCall.parameter1 = '-f image2 -start_number 2 '
	ffmpegCall.inputFile = '-i ' + '"' + framesDirectory + '\\' + getFilePrefix(os.listdir(framesDirectory + '\\')[0]) + r'.%%04d' + getFileType() + '" '

	ffmpegCall.outputFileDir = tempfile.gettempdir()+ '\\'
	ffmpegCall.outputFileName = 'render-'+ time.strftime("%H%M%S%d%m%y", time.localtime()) +'.mp4'
	ffmpegCall.outputFile = ffmpegCall.outputFileDir + ffmpegCall.outputFileName

	ffmpegCall.createBatchFile()

	return ffmpegCall

def getFrameCount(_frameDir):
	return len(os.listdir(_frameDir))

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

def watchDirectoryForFrames(_currentFrameCount):
	while True:
		_lastframeCount = _currentFrameCount
		_currentFrameCount = getFrameCount(framesDirectory)

		if (_lastframeCount == _currentFrameCount):
			break

		print('Last frame count: ' + str(_lastframeCount))
		print('Current frame count: ' + str(_currentFrameCount))
		sleepInterval = float(data['Properties']['FrameDirectoryWatchInterval'])
		time.sleep(sleepInterval)
	return _currentFrameCount

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

# Setup log file for each session
logging.basicConfig(filename=programDirectory + '\log-' + time.strftime("%H%M%S%d%m%y", time.localtime()) + '.log',level=logging.DEBUG)

log('Frame directory: ' + framesDirectory)

#read config file
with open(programDirectory + '\Config.json') as data_file:
 	data = json.load(data_file)

#todo handle missing config file
currentFrameCount = 0
currentFrameCount = watchDirectoryForFrames(currentFrameCount)


if currentFrameCount < float(data['Properties']['MinimumFrameCount']):
	log('Error: Supplied frame directory has fewer than MinimumFrameCount files after waiting for the FrameDirectoryWatchInterval in config.json. Either select the correct directory or increase FrameDirectoryWatchInterval time')
	shutdown()

log('Found ' + str(currentFrameCount) + ' frames in directory. Starting sequence creation...')

# delete last frame
prepareFrames(framesDirectory)
lastFrameName = getLastFrameName()
print(framesDirectory +'\\'+ lastFrameName)
print(framesDirectory + r'\\_' + lastFrameName)
os.rename(framesDirectory +'\\'+ lastFrameName, framesDirectory + r'\\_' + lastFrameName)


# when frames are no longer being created, convert
#todo set output resolution from config

ffmpegCall = FFmpegObject()
convertFramesToVideo(ffmpegCall)

# move video out of temp directory into the directory of the script
shutil.move(ffmpegCall.outputFile, programDirectory + '\\' + ffmpegCall.outputFileName)
log('Output video moved to ' + programDirectory + '\\' + ffmpegCall.outputFileName)

# upload to youtube

# send email notification