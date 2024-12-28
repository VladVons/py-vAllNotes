# Created: 2024.05.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from IncP.Log import Log
from IncP.SrvBaseEx import TSrvBaseEx
from .Api import ApiCtrl


class TSrvCtrl(TSrvBaseEx):
    def _GetDefRoutes(self) -> list:
        return [
            web.post('/api/{name:.*}', self._rApi),
        ]

    def GetApi(self) -> object:
        return ApiCtrl

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi() only')
