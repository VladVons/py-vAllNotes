# Created: 2024.12.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Info import GetSysInfo
from IncP import GetAppVer
from IncP.CtrlBase import TCtrlBase


class TMain(TCtrlBase):
    async def AppVer(self) -> dict:
        return {'data': GetAppVer()}

    async def SysInfo(self) -> dict:
        return {'data': GetSysInfo()}
