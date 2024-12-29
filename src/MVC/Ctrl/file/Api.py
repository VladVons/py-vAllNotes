# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import io
import json
from aiohttp import web
#
from Inc.VFS.Disk import TFsDisk
from IncP.CtrlBase import TCtrlBase
from Task.SrvCtrl.Api import TApiCtrl

class TABytesIO():
    def __init__(self, aBuf: io.BytesIO):
        self.Buf = aBuf

    async def read(self, aSize: int):
        return self.Buf.read(aSize)

    async def write(self, aData):
        return self.Buf.write(aData)


class TMain(TCtrlBase):
    def __init__(self, aApiCtrl: TApiCtrl):
        super().__init__(aApiCtrl)
        self.Fs = TFsDisk(self.ApiCtrl.ConfApp['dir_data'])

    async def Read(self, aFile: str) -> dict:
        Res = self.Fs.FileRead(aFile)
        return {'data': Res}

    async def ReadPos(self, aFile: str, aRequest: web.Request, aPos: int, aLen: int, aChankSize: int = 65535) -> dict:
        Len = self.Fs.FileSize(aFile)
        if (Len):
            Headers={'Content-Type': 'application/octet-stream', 'Custom-Header': json.dumps({'data': Len})}
            Response = web.StreamResponse(status=200, headers=Headers)
            await Response.prepare(aRequest)
            await self.Fs.FileReadChunkPos(aFile, Response, aChankSize, aPos, aLen)
            await Response.write_eof()
            return {'response': Response}

    async def Write(self, aFile: str, aData: str) -> dict:
        if (isinstance(aData, str)):
            aData = aData.encode()

        Res = self.Fs.FileWrite(aFile, aData)
        return {'data': Res}

    async def WritePos(self, aFile: str, aRequest: web.Request, aPos: int, aChankSize: int = 65535) -> dict:
        Res = await self.Fs.FileWriteChunkPos(aFile, aRequest.content, aChankSize, aPos, aRequest.content_length)
        return {'data': Res}

    async def Size(self, aFile: str) -> dict:
        Len = self.Fs.FileSize(aFile)
        return {'data': Len}

    async def Exists(self, aFile: str) -> dict:
        IsExists = self.Fs.FileExists(aFile)
        return {'data': IsExists}

    async def Delete(self, aFile: str) -> dict:
        IsExists = self.Fs.FileDelete(aFile)
        return {'data': IsExists}

    async def Truncate(self, aFile: str, aSize: int = 0) -> dict:
        Len = self.Fs.Truncate(aFile, aSize)
        return {'data': Len}

    async def DirCreate(self, aFile: str) -> dict:
        IsExists = self.Fs.DirCreate(aFile)
        return {'data': IsExists}
