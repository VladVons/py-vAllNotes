# Created: 2024.05.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import time
import json
from aiohttp import web
#
from IncP.Log import Log
from IncP.SrvBaseEx import TSrvBaseEx
from .Api import ApiCtrl


class TSrvCtrl(TSrvBaseEx):
    def _GetDefRoutes(self) -> list:
        return [
            web.post('/apiJson/{name:.*}', self._rApi),
            web.post('/apiBytes/{name:.*}', self._rApiBytes)
        ]

    async def _rApiBytes(self, aRequest: web.Request) -> web.Response:
        Res = {}
        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            CustomHeader = aRequest.headers.get('Custom-Header', '')
            DataIn = json.loads(CustomHeader)
            DataIn['param']['aRequest'] = aRequest
            Api = self.GetApi()
            R = await Api.Exec(Name, DataIn) or {}
            if ('response' in R):
                return R['response']
            #Status = 403 if ('err' in R) else 200
            Status = 200
            Res.update(R)
        Res['info'] = {
            'time': round(time.time() - TimeStart, 4),
            'status': Status
        }
        return web.json_response(Res, status = Status)

    def GetApi(self) -> object:
        return ApiCtrl

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi() only')
