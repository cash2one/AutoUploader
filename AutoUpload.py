import sys
import os
import time
import tempfile
import subprocess
import json
import pdb
import logging
import shutil

#todo fix uploading #todo carriage return frame status
#todo watch frame location indefinitely if the supplied location is empty
#todo avoid upscaling video if supplied resolution is smaller than the resolution in the config
#todo copy frames as they being made
#todo email after the video is uploaded
#todo move log to output folder

#todo
# frames/video -> video -> youtube -> email


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
        #todo figure out why it freaks out on frame mode if you put param1 after inputfile
        if gArgs.inputArgIsDir:
            tempBatFile.write(bytes(self.fullBatchPath + self.videoFramerate + self.parameter1 + self.inputFile + self.outputResolution + self.outputFile, 'UTF-8'))
        else:
            tempBatFile.write(bytes(self.fullBatchPath + self.videoFramerate + self.inputFile + self.parameter1 + self.outputResolution + self.outputFile, 'UTF-8'))
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
    
    inputDirectory = ''
    tempInputDirectory = ''
    filePrefix = ''
    fileNumberinglength = ''
    fileSuffix = ''

    def __init__(self, frameDir):
        self.inputDirectory = frameDir
        self.copyTempFrames()
        self.determineFrameAttributes()
        self.removeNonFrameObjects()
        self.getSortedFrameList()
        self.topAndTail()
        self.renameFramesToSortedList()
        

    #copy only image files to temp directory
    def copyTempFrames(self):
        suffixes = ('.png', '.jpg', '.jpeg', '.tga', '.tiff')
        self.tempInputDirectory = os.path.dirname(self.inputDirectory) + "\\temp\\"
        #make temp directory if it doesn't already exist. If it does, clear the directory before we copy anything to it
        if not os.path.isdir(os.path.dirname(gInputPath) + "\\temp\\"):
            os.mkdir(os.path.dirname(gInputPath) + "\\temp\\")
        else:
            for existingFile in os.listdir(self.tempInputDirectory):
                os.remove(self.tempInputDirectory + '\\' + existingFile)

        for file in os.listdir(self.inputDirectory):
            if file.endswith(suffixes):
                shutil.copy(self.inputDirectory + '\\' + file, self.tempInputDirectory + file)
            else:
                print('File ' + file + ' was not copied')
        return

    def determineFrameAttributes(self):
        tempFilename = os.listdir(self.tempInputDirectory)[0]
        print (os.listdir(self.tempInputDirectory)[0]) 

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
        topAmount = gConfig.getValue('Properties', 'NumStartingFramesToSkip')
        tailAmount = gConfig.getValue('Properties', 'NumEndingFramesToSkip')
        currentTrimAmount = 0
        currentCheckIndex = 0
        while True:
            if currentTrimAmount == int(topAmount):
                break
            currentFile = os.listdir(self.tempInputDirectory)[currentCheckIndex]
            if currentFile.startswith(self.filePrefix):
                os.remove(self.tempInputDirectory + "\\" + currentFile)
                currentTrimAmount = currentTrimAmount + 1
            else:
                currentCheckIndex = currentCheckIndex + 1
        

        currentTrimAmount = 0
        currentCheckIndex = 0
        while True:
            if currentTrimAmount == int(tailAmount):
                break
            lastIndex = len(os.listdir(self.tempInputDirectory)) - 1
            currentFile = (os.listdir(self.tempInputDirectory)[lastIndex - currentCheckIndex])
            if currentFile.startswith(self.filePrefix):
                os.remove(self.tempInputDirectory + "\\" + currentFile)
                currentTrimAmount = currentTrimAmount + 1
            else:
                currentCheckIndex = currentCheckIndex + 1
        return

    def renameFramesToSortedList(self):
        count = 0
        for file in os.listdir(self.tempInputDirectory):
            if file.startswith(self.filePrefix): 
                os.rename(self.tempInputDirectory + '\\' + file, self.tempInputDirectory + '\\' + self.filePrefix + str(count).zfill(self.fileNumberinglength) + self.fileSuffix)
                count += 1

        return

    def removeTempFrames(self):
        shutil.rmtree(self.tempInputDirectory)

#
class Args:

    args = ''
    programDirectory = ''
    inputArg = ''

    inputArgIsFile = False
    inputArgIsDir = False
    argUpload = False

    def __init__(self):
        self.args = sys.argv
        if len(self.args) < 2:
            log('No frame directory supplied. Drag frame folder or movie file onto program.')
            shutdown()

        self.findArguments()
        self.determineInputType()

    def findArguments(self):
        self.programDirectory = os.path.dirname(sys.argv[0])
        self.inputArg = str(sys.argv[1])

        if '-upload' in self.args:
            self.argUpload = True

    #figure out if the input passed in is a directory or a file
    def determineInputType(self):
        if os.path.isdir(self.inputArg):
            self.inputArgIsDir = True
        elif os.path.isfile(self.inputArg):
            self.inputArgIsFile = True
        else:
            log('Error: Could not determine if input was directory or file. Aborting.')
            shutdown()


#todo handle missing config file
class JsonReader:
    data = ''

    def __init__(self):
        with open(gProgramDirectory + '\Config.json') as data_file:
            self.data = json.load(data_file)
        pass

    def getValue(self, category, value):
        return self.data[category][value]
        pass

def convertFramesToVideo(ffmpegCall):
    framesDirectory = framePrepObject.tempInputDirectory
    ffmpegCall.fullBatchPath = gProgramDirectory + '\\' + 'ffmpeg.exe '
    ffmpegCall.videoFramerate = '-r ' + gConfig.getValue('Properties', 'Framerate') + ' '
    ffmpegCall.parameter1 = '-f image2 '
    ffmpegCall.inputFile = '-i ' + '"' + framesDirectory + '\\' + getFilePrefix(os.listdir(framesDirectory + '\\')[0]) + r'.%%04d' + getFileType() + '" '
    ffmpegCall.outputResolution = '-s ' + gConfig.getValue('Properties', 'OutputWidth') + 'x' + gConfig.getValue('Properties', 'OutputHeight') + ' '
    ffmpegCall.outputFileDir = tempfile.gettempdir()+ '\\'
    ffmpegCall.outputFileName = gVideoTitle +'.mp4 '
    ffmpegCall.outputFile = ffmpegCall.outputFileDir + ffmpegCall.outputFileName

    ffmpegCall.createBatchFile()



    return ffmpegCall

def convertVideo():
    ffmpegCall.fullBatchPath = gProgramDirectory + '\\' + 'ffmpeg.exe '
    ffmpegCall.videoFramerate = '-r ' + gConfig.getValue('Properties', 'Framerate') + ' '
    ffmpegCall.parameter1 = '-c:v libx264 '
    ffmpegCall.inputFile = '-i ' + '"' + gInputPath + '" '
    ffmpegCall.outputResolution = '-s ' + gConfig.getValue('Properties', 'OutputWidth') + 'x' + gConfig.getValue('Properties', 'OutputHeight') + ' '
    ffmpegCall.outputFileDir = tempfile.gettempdir()+ '\\'
    ffmpegCall.outputFileName = gVideoTitle +'.mp4'
    ffmpegCall.outputFile = ffmpegCall.outputFileDir + ffmpegCall.outputFileName

    ffmpegCall.createBatchFile()



    return ffmpegCall

def getFrameCount(_frameDir):
    return len(os.listdir(_frameDir))

def getByteCount(_videoFile):
    return os.path.getsize(_videoFile)

#todo rename or refactor this - doing more than one task
def getFileType():
    suffixes = ('.png', '.jpg', '.jpeg', '.tga', '.tiff')
    currentIndex = 0
    while True:
        filename = os.listdir(gInputPath + '\\')[currentIndex]
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
    
#todo generic way to get the file extension of any passed in path with an optional ability to filter entries
def getFileExtension(fileName, filter = []):
    while True:
        characterIndex = len(filename) - 1
        while True:
            if filename[characterIndex] == '.':
                break
            characterIndex -= 1
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
    dirList = os.listdir(gInputPath)
    dirList.sort()
    currentLastFileSearchIndex = 1
    while True:
        lastFrameName = dirList[len(dirList) - currentLastFileSearchIndex]
        if getFilePrefix(lastFrameName) == getFilePrefix(os.listdir(gInputPath + '\\')[0]): #if the prefixes of the first and last file match
            return lastFrameName
        currentLastFileSearchIndex = currentLastFileSearchIndex + 1

def watchDirectoryForFrames(_currentFrameCount):
    while True:
        _lastframeCount = _currentFrameCount
        _currentFrameCount = getFrameCount(gInputPath)

        if (_lastframeCount == _currentFrameCount):
            break

        print('Last frame count: ' + str(_lastframeCount))
        print('Current frame count: ' + str(_currentFrameCount))
        sleepInterval = float(gConfig.getValue('Properties', 'FrameDirectoryWatchInterval'))
        time.sleep(sleepInterval)
    return _currentFrameCount

def watchVideoFile(_currentByteCount):
    while True:
        _lastByteCount = _currentByteCount
        _currentByteCount = getByteCount(gInputPath)

        if (_lastByteCount == _currentByteCount):
            break

        print('Last byte count: ' + str(_lastByteCount))
        print('Current byte count: ' + str(_currentByteCount))
        sleepInterval = float(gConfig.getValue('Properties', 'FrameDirectoryWatchInterval'))
        time.sleep(sleepInterval)
    return _currentByteCount

def countFrames():
    # watch directory for frames
    currentFrameCount = 0
    currentFrameCount = watchDirectoryForFrames(currentFrameCount)

    if currentFrameCount < int(gConfig.getValue('Properties', 'MinimumFrameCount')):
        log('Error: Supplied frame directory has fewer than MinimumFrameCount files after waiting for the FrameDirectoryWatchInterval in config.json. Either select the correct directory or increase FrameDirectoryWatchInterval time')
        shutdown()

    log('Found ' + str(currentFrameCount) + ' frames in directory. Starting sequence creation...')

def countBytes():
    # watch directory for frames
    currentByteCount = 0
    currentByteCount = watchVideoFile(currentByteCount)

    log('Found ' + str(currentByteCount) + ' bytes in file. Starting conversion...')

def uploadToYoutube():
    fullBatchPath = gProgramDirectory + '\\Python34\\python.exe ' + gProgramDirectory + '\\upload_video.py --file '
    videoPath = '"' + os.path.dirname(gInputPath) + '\\' + ffmpegCall.outputFileName + '" '
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

gInputPath = str(sys.argv[1])


log('Frame directory: ' + gInputPath)

#read config file
gConfig = JsonReader()

if gArgs.inputArgIsDir:
    countFrames()
else:
    countBytes()


if gArgs.inputArgIsDir:
    # top and tail frames and rename them into an ordered sequence
    framePrepObject = FramePrep(gInputPath)

# when frames are no longer being created, convert
ffmpegCall = FFmpegObject()

if gArgs.inputArgIsDir:
    convertFramesToVideo(ffmpegCall)
    framePrepObject.removeTempFrames()
else:
    convertVideo()



# move video out of temp directory into the directory of the script
shutil.move(ffmpegCall.outputFile, os.path.dirname(gInputPath) + '\\' + ffmpegCall.outputFileName)
log('Output video moved to ' + gInputPath + '\\' + ffmpegCall.outputFileName)

if gArgs.argUpload == True:
    uploadToYoutube()
else:
    print("No -upload parameter passed. Skipping upload")


# send email notification
