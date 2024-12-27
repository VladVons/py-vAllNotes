#Created:     2024.12.27
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


__version__ = '1.0.1'
__date__ =  '2024.12.27'
__author__ = 'Vladimir Vons'
__email__ = 'VladVons@gmail.com'
__url__ = 'http://oster.com.ua'


def GetAppVer() -> dict:
    return {
        'app_name': 'vAllNotes',
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  f'{__author__ }, {__email__}',
        'home': __url__
    }