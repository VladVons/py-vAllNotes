# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Plugin import TPlugin


class TPluginMVC(TPlugin):
    def _Create(self, _aModule: object, _aPath: str) -> object:
        raise NotImplementedError()

    def _GetPath(self, aPath: str) -> str:
        return f'{self.Dir}/{aPath}'

    def IsModule(self, aPath: str) -> bool:
        Path = self._GetPath(aPath)
        for x in ['.py', '/__init__.py']:
            if (os.path.exists(f'{Path}{x}')):
                return True

class TModels(TPluginMVC):
    def __init__(self, aDir: str, aApi):
        super().__init__(aDir)
        self.Name = 'model'
        self.ApiModel = aApi

    def _Create(self, aModule: object, aPath: str) -> object:
        return aModule.TMain(self.ApiModel, self.Dir + '/' + aPath)

class TCtrls(TPluginMVC):
    def __init__(self, aDir: str, aApi):
        super().__init__(aDir)
        self.Name = 'ctrl'
        self.ApiCtrl = aApi

    def _Create(self, aModule: object, _aPath: str) -> object:
        return aModule.TMain(self.ApiCtrl)
