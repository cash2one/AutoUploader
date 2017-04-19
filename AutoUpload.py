import sys
import os
import time
import tempfile
import subprocess
import json
import pdb
import logging
import shutil

#todo carriage return frame status
#todo watch frame location indefinitely if the supplied location is empty
#todo avoid upscaling video if supplied resolution is smaller than the resolution in the config
#todo copy frames as they being made
#todo email after the video is uploaded
#todo move log to output folder

"""
normal process
normal process without upload
quick convert existing video
"""

class FFmpegObject:
	fullBatchPath = ''
	videoFramerate = ''
	parameter1 = ''
	inputFile = ''
	outputResolution = ''
	outputFileDir = ''
	outputFileName = ''
	outputFile = ''

	def createBatchFile(self):
		# Create temporary batch file to call ffmpeg
		tempBatFile = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
		tempBatFile.write(bytes(self.fullBatchPath + self.videoFramerate + self.parameter1 + self.inputFile + self.outputResolution + self.outputFile, 'UTF-8'))
		tempBatFile.close()

		log('Batch arguments: ' + self.fullBatchPath + self.videoFramerate + self.parameter1 + self.inputFile + self.outputResolution + self.outputFile)
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
		

	#copy only image files to temp directory
	def copyTempFrames(self):
		suffixes = ('.png', '.jpg', '.jpeg', '.tga', '.tiff')
		self.tempFramesDirectory = self.framesDirectory + "\\temp\\"
		#make temp directory if it doesn't already exist. If it does, clear the directory before we copy anything to it
		if not os.path.isdir(framesDirectory + "\\temp\\"):
			os.mkdir(framesDirectory + "\\temp\\")
		else:
			for existingFile in os.listdir(self.tempFramesDirectory):
				os.remove(self.tempFramesDirectory + '\\' + existingFile)

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
		currentCheckIndex = 0
		while True:
			if currentTrimAmount == int(topAmount):
				break
			currentFile = os.listdir(self.tempFramesDirectory)[currentCheckIndex]
			if currentFile.startswith(self.filePrefix):
				os.remove(self.tempFramesDirectory + "\\" + currentFile)
				currentTrimAmount = currentTrimAmount + 1
			else:
				currentCheckIndex = currentCheckIndex + 1
		

		currentTrimAmount = 0
		currentCheckIndex = 0
		while True:
			if currentTrimAmount == int(tailAmount):
				break
			lastIndex = len(os.listdir(self.tempFramesDirectory)) - 1
			currentFile = (os.listdir(self.tempFramesDirectory)[lastIndex - currentCheckIndex])
			if currentFile.startswith(self.filePrefix):
				os.remove(self.tempFramesDirectory + "\\" + currentFile)
				currentTrimAmount = currentTrimAmount + 1
			else:
				currentCheckIndex = currentCheckIndex + 1
		return

	def renameFramesToSortedList(self):
		count = 0
		for file in os.listdir(self.tempFramesDirectory):
			if file.startswith(self.filePrefix): 
				os.rename(self.tempFramesDirectory + '\\' + file, self.tempFramesDirectory + '\\' + self.filePrefix + str(count).zfill(self.fileNumberinglength) + self.fileSuffix)
				count += 1

		return

	def removeTempFrames(self):
		shutil.rmtree(self.tempFramesDirectory)

#
class Args:

	args = ''
	programDirectory = ''

	argUpload = False

	def __init__(self):
		args = sys.argv
		if len(sys.argv) < 2:
			log('No frame directory supplied. Drag frame folder or movie file onto program.')
			shutdown()

		self.findArguments()

	def findArguments(self):
		self.programDirectory = os.path.dirname(sys.argv[0])

		if '-upload' in self.args:
			self.argUpload = True

class JsonReader:
	data = ''

	def __init__(self):
		pass

def convertFramesToVideo(ffmpegCall):
	framesDirectory = framePrepObject.tempFramesDirectory
	ffmpegCall.fullBatchPath = gProgramDirectory + '\\' + 'ffmpeg.exe '
	ffmpegCall.videoFramerate = '-r ' + data['Properties']['Framerate'] + ' '
	ffmpegCall.parameter1 = '-f image2 '
	ffmpegCall.inputFile = '-i ' + '"' + framesDirectory + '\\' + getFilePrefix(os.listdir(framesDirectory + '\\')[0]) + r'.%%04d' + getFileType() + '" '
	ffmpegCall.outputResolution = '-s ' + data['Properties']['OutputWidth'] + 'x' + data['Properties']['OutputHeight'] + ' '
	ffmpegCall.outputFileDir = tempfile.gettempdir()+ '\\'
	ffmpegCall.outputFileName = gVideoTitle +'.mp4'
	ffmpegCall.outputFile = ffmpegCall.outputFileDir + ffmpegCall.outputFileName

	ffmpegCall.createBatchFile()



	return ffmpegCall

def getFrameCount(_frameDir):
	return len(os.listdir(_frameDir))

def getFileType():
	suffixes = ('.png', '.jpg', '.jpeg', '.tga', '.tiff')
	currentIndex = 0
	while True:
		filename = os.listdir(framesDirectory + '\\')[currentIndex]
		characterIndex = len(filename) - 1
		while True:
			if filename[characterIndex] == '.':
				break
			characterIndex = characterIndex - 1
			fileExtension = str((filename[characterIndex:]))
			if fileExtension in suffixes:
				return str((filename[characterIndex:]))
			else:
				currentIndex += 1
	
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

def uploadToYoutube():
	fullBatchPath = gProgramDirectory + '\\Python34\\python.exe ' + gProgramDirectory + '\\upload_video.py --file '
	videoPath = '"' + gProgramDirectory + '\\' + ffmpegCall.outputFileName + '" '
	videoTitleParam = ' --title "' + gVideoTitle + '"'
	tempBatFile = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
	tempBatFile.write(bytes(fullBatchPath + videoPath + videoTitleParam, 'UTF-8'))
	tempBatFile.close()

	log('Batch file created.')

	print(tempBatFile.name)

	subprocess.call(tempBatFile.name)

	log('Batch program returned')

	#remove temp batch file
	os.remove(tempBatFile.name)


def log(logMessage):
	logging.debug(time.strftime("%H%M%S", time.localtime()) + ': ' + logMessage)
	print(logMessage)

def shutdown():
	exit('Program ended. Press any key to close window.')


#process input arguments
gArgs = Args()
gProgramDirectory = gArgs.programDirectory

# Setup log file for each session
logging.basicConfig(filename=gProgramDirectory + '\log-' + time.strftime("%H%M%S%d%m%y", time.localtime()) + '.log',level=logging.DEBUG)

gVideoTitle = input('Enter video title: ')

framesDirectory = str(sys.argv[1])


log('Frame directory: ' + framesDirectory)

#read config file
#todo handle missing config file
with open(gProgramDirectory + '\Config.json') as data_file:
 	data = json.load(data_file)


# watch directory for frames
currentFrameCount = 0
currentFrameCount = watchDirectoryForFrames(currentFrameCount)


if currentFrameCount < float(data['Properties']['MinimumFrameCount']):
	log('Error: Supplied frame directory has fewer than MinimumFrameCount files after waiting for the FrameDirectoryWatchInterval in config.json. Either select the correct directory or increase FrameDirectoryWatchInterval time')
	shutdown()

log('Found ' + str(currentFrameCount) + ' frames in directory. Starting sequence creation...')

# top and tail frames and rename them into an ordered sequence
framePrepObject = FramePrep(framesDirectory)

# when frames are no longer being created, convert
ffmpegCall = FFmpegObject()
convertFramesToVideo(ffmpegCall)

framePrepObject.removeTempFrames()

# move video out of temp directory into the directory of the script
shutil.move(ffmpegCall.outputFile, framesDirectory + '\\' + ffmpegCall.outputFileName)
log('Output video moved to ' + framesDirectory + '\\' + ffmpegCall.outputFileName)

if '-upload' in sys.argv:
	uploadToYoutube()
else:
	print("No -upload parameter passed. Skipping upload")


# send email notification
