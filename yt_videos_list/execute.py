from . import program
from .notifications import Common, ModuleMessage, ScriptMessage
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import platform
import time
import os

commonMessage = Common()
sMessage = ScriptMessage()

def verifyWriteFormat(fileType, writeFormat, fileName, fileExtension):
    if fileType is True and writeFormat == 'x':
        filename = f'{fileName}VideosList.{fileExtension}'
        fileExists = True if os.path.isfile(f'./{filename}') else False

        def newWriteFormat():
            userResponse = input()
            if 'proceed' in userResponse.strip().lower():
                return 'w'
            elif 'skip' in userResponse.strip().lower():
                return 0
            else:
                print ('\n' + commonMessage.invalidResponse)
                commonMessage.fileAlreadyExistsPrompt(filename)
                return newWriteFormat()

        if fileExists is True:
            commonMessage.fileAlreadyExistsWarning(filename)
            commonMessage.fileAlreadyExistsPrompt(filename)
            return newWriteFormat()
        return 'x'

    else:
        return writeFormat

def setupDriver(userDriver):
    if 'firefox' in userDriver:
        return webdriver.Firefox
    elif 'chrome' in userDriver:
        return webdriver.Chrome
    elif 'opera' in userDriver:
        return webdriver.Opera
    elif 'safari' in userDriver:
        return webdriver.Safari
    else:
        print (commonMessage.invalidDriver)
        return 'invalid'

def logic(channel, channelType, fileName, txt, txtWriteFormat, csv, csvWriteFormat, docx, docxWriteFormat, chronological, headless, scrollPauseTime, userDriver, executionType):
    mMessage = ModuleMessage()
    commonMessage = Common()
    channel = channel.strip().strip('/')
    channelType = channelType.strip().strip('/')

    def determineFileName(fileName):
        if fileName is not None:
            return fileName
        else:
            return channel

    fileName = determineFileName(fileName)

    txtWriteFormat = verifyWriteFormat(txt, txtWriteFormat, fileName, 'txt')
    csvWriteFormat = verifyWriteFormat(csv, csvWriteFormat, fileName, 'csv')
    docxWriteFormat = verifyWriteFormat(docx, docxWriteFormat, fileName, 'docx')

    if userDriver is None:
        print (mMessage.runningDefaultDriver) if executionType == 'module' else print (sMessage.runningDefaultDriver)
        print (mMessage.showDriverOptions) if executionType == 'module' else print (sMessage.showDriverOptions)
        userDriver = 'firefox'

    driver = setupDriver(userDriver)
    if driver == 'invalid':
        return

    programStart = time.perf_counter()
    try:
        if headless is False: # opens Selenium browsing instance
            driver = driver()
            if executionType == 'module':
                print (mMessage.runInHeadless)
                print (mMessage.runInHeadlessExample)
        else: # headless is True
            if userDriver == 'firefox':
                options = selenium.webdriver.firefox.options.Options()
                options.headless = True
                driver = driver(options=options)
            if userDriver == 'chrome':
                # options = selenium.webdriver.chrome.options.Options()
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                driver = driver(chrome_options=options)
            if userDriver == 'opera':
                # Opera driver MRO: WebDriver -> OperaDriver -> selenium.webdriver.chrome.webdriver.WebDriver -> selenium.webdriver.remote.webdriver.WebDriver -> builtins.object
                # options = selenium.webdriver.chrome.options.Options()
                # options.headless = True
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                driver = driver(options=options)
                print (commonMessage.unsupportedOperaHeadless)
            if userDriver == 'safari':
                driver = driver()
                print (commonMessage.unsupportedSafariHeadless)
    except selenium.common.exceptions.WebDriverException as e:
        # selenium.common.exceptions.WebDriverException: Message: 'BROWSERdriver' executable needs to be in PATH. Please see https://................
        # for some reason this also catches selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of BROWSERDriver only supports BROWSER version ##
        commonMessage.seleniumDependencyError(e)
        if platform.system().lower().startswith('darwin'):
            userOS = 'macos'
        elif platform.system().lower().startswith('windows'):
            userOS = 'windows'
        elif platform.system().lower().startswith('linux'):
            userOS = 'linux'
        else:
            print (commonMessage.unsupportedOS)
            return

        if userDriver != 'safari':
            commonMessage.tellUserToDownloadDriver(userDriver)
        commonMessage.displayDependencySetupInstructions(userDriver, userOS)
        return

    with driver:
        videosList = program.scrollToBottom(channel, channelType, driver, scrollPauseTime)
        if len(videosList) == 0:
            print (commonMessage.noVideosFound)
            print (mMessage.checkChannelType) if executionType == 'module' else print (sMessage.checkChannelType)
            return
        if txt is True:
            program.writeToTxt(videosList, channel, fileName, txtWriteFormat, chronological)
            # saveToMemWriteToTxt(videosList, channel, fileName, writeFormat) # slightly slower than writing to disk directly
        if csv is True:
            program.writeToCsv(videosList, channel, fileName, csvWriteFormat, chronological)

    programEnd = time.perf_counter()
    totalTime = programEnd - programStart
    print(f'This program took {totalTime} seconds to complete.\n')
