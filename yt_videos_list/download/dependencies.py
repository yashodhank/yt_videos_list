import os
import sys
import platform

from . import selenium_linux, selenium_macos, selenium_windows
from ..notifications import Common


COMMON_MESSAGE = Common()
APPLICATION_NAME = {
    'macos': {
        # 'driver': 'browser_name'
        'firefox':  'Firefox',
        'opera':    'Opera',
        'chrome':   'Google Chrome',
        'brave':    'Brave Browser',
        'edge':     'Microsoft Edge'
    },
    'linux': {
        'firefox':  'Automatic Selenium dependency download for Windows is not yet supported. Please follow the instructions below to set up the correct selenium dependecy for the firefoxdriver.',
        'opera':    'Automatic Selenium dependency download for Windows is not yet supported. Please follow the instructions below to set up the correct selenium dependecy for the operadriver.',
        'chrome':   'Automatic Selenium dependency download for Windows is not yet supported. Please follow the instructions below to set up the correct selenium dependecy for the chromedriver.'
    },
    'windows': {
        'firefox':  'Mozilla Firefox',
        'opera':    'Opera',
        'chrome':   'Chrome',
        'brave':    'Brave-Browser',
        'edge':     'Edge'
    }
}

def determine_user_os():
    if   platform.system().lower().startswith('darwin'):  return 'macos'
    elif platform.system().lower().startswith('linux'):   return 'linux'
    elif platform.system().lower().startswith('windows'): return 'windows'
    else:
        print(Common().unsupported_os)
        sys.exit()

def download_specific_dependency(driver, user_os):
    selenium_user_os = globals()[f'selenium_{user_os}']
    browser = APPLICATION_NAME[user_os][driver]
    if selenium_user_os.browser_exists(browser):
        full_version_number = selenium_user_os.get_browser_version(browser)
        COMMON_MESSAGE.display_browser_found_information(browser, full_version_number)
        major_version = full_version_number.split('.')[0]
        execute_download_command(driver, user_os, major_version)
    else:
        COMMON_MESSAGE.display_browser_not_found_information(browser, user_os)

def download_all_dependencies(user_os):
    print(COMMON_MESSAGE.automated_driver_update)
    for driver in APPLICATION_NAME[user_os]:
        download_specific_dependency(driver, user_os)

def execute_download_command(driver, user_os, version):
    # indexed values in reverse order to avoid having to map every version to a different element every time a new driver/browser version comes out since all the values get shifted down by 2 with new additions to the top of the list
    row_in_list = {
        'firefox': {
            '79': -1,
            '78': -1,
            '77': -1,
            '76': -1,
            '75': -1,
            '74': -1,
            '73': -1,
            '72': -1,
            '71': -1,
            '70': -1,
            '69': -1,
            '68': -1,
            '67': -1,
            '66': -1,
            '65': -1,
            '64': -1,
            '63': -1,
            '62': -1,
            '61': -1,
            '60': -1,
        },
        'opera': {
            '68': -25,
            '67': -23,
            '66': -21,
            '65': -19,
            '64': -17,
            '63': -15,
            '62': -13,
            # there was no version 61
            '60': -11,
            # there was no version 59
            '58': -9,
            '57': -7,
            '56': -5,
            '55': -3,
            '54': -1,
        },
        'chrome': {
            '81': -19,
            '80': -17,
            '79': -15,
            '78': -13,
            '77': -11,
            '76': -9,
            '75': -7,
            '74': -5,
            '73': -3,
            '72': -1,
            '71': -1
        },
        'brave': {
            '81': -13,
            '80': -11,
            '79': -9,
            '78': -7,
            '77': -5,
            '76': -3,
            '75': -1
        },
        'edge': {
            '81': -5,
            '80': -3,
            '79': -1
        }
    }
    row = row_in_list[driver][version]
    print(f'Now downloading the corresponding selenium driver for {driver} version {version} on {user_os}:')
    print(f'{COMMON_MESSAGE.driver_downloads_for_os[driver][user_os][row-1]} #')
    print(f'{COMMON_MESSAGE.driver_downloads_for_os[driver][user_os][row]}')
    os.system(COMMON_MESSAGE.driver_downloads_for_os[driver][user_os][row])

def download_dependencies():
    user_os = determine_user_os()
    download_all_dependencies(user_os)
