# Created: 2024.12.27
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import IncP.LibCtrl as Lib
from Task.SrvCtrl.Api import TApiCtrl


class TCtrlBase():
    def __init__(self, aApiCtrl: TApiCtrl):
        self.ApiCtrl = aApiCtrl
        self.ApiModel = None

    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get

    @property
    def Name(self) -> str:
        return self.ApiCtrl.Name

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        return await self.ApiModel(aMethod, aData)

    async def ExecModelImport(self, aMethod: str, aData: dict) -> dict:
        Res = await self.ApiModel(aMethod, aData)
        if (isinstance(Res, dict) and ('tag' in Res) and ('head' in Res)):
            Res = Lib.TDbList().Import(Res)
        return Res
