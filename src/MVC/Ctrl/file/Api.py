# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from aiohttp import web
#
from Inc.Util.ModHelp import GetClass
from Inc.VFS.Disk import TFsDisk
from IncP.CtrlBase import TCtrlBase
from Task.SrvCtrl.Api import TApiCtrl

# class TABytesIO():
#     def __init__(self, aBuf: io.BytesIO):
#         self.Buf = aBuf

#     async def read(self, aSize: int):
#         return self.Buf.read(aSize)

#     async def write(self, aData):
#         return self.Buf.write(aData)


class TMain(TCtrlBase):
    def __init__(self, aApiCtrl: TApiCtrl):
        super().__init__(aApiCtrl)
        self.Fs = TFsDisk(self.ApiCtrl.ConfApp['dir_data'])

    async def Copy(self, aSrc: str, aDst: str) -> dict:
        '''
        copy file or directory from aSrc to aDst.
        '''
        Res = self.Fs.Copy(aSrc, aDst)
        return {'data': Res}

    async def Delete(self, aFile: str) -> dict:
        '''
        delete file or directory.
        '''
        IsExists = self.Fs.Delete(aFile)
        return {'data': IsExists}

    async def DirCreate(self, aDir: str) -> dict:
        '''
        create directory.
        '''
        IsExists = self.Fs.DirCreate(aDir)
        return {'data': IsExists}

    async def Exists(self, aFile: str) -> dict:
        IsExists = self.Fs.Exists(aFile)
        return {'data': IsExists}

    async def Help(self) -> list:
        '''
        get this brief help.
        '''
        Data = GetClass(self)
        Api = [[x[2], x[3].strip()] for x in Data]
        Res = sorted(Api, key=lambda x: x[0])
        return Res

    async def List(self, aPath: str) -> dict:
        '''
        get file list from directory.
        '''
        Files = self.Fs.List(aPath)
        return {'data': Files}

    async def MassCall(self, aParam: list) -> dict:
        '''
        Multiple call in one request.
        aParam = ['DirCreate', ['Dir3/Dir31'], ['Dir4/Dir41']]
        '''
        Res = self.Fs.MassCall(aParam)
        return {'data': Res}

    async def MassCalls(self, aParam: list) -> dict:
        '''
        Multiple calls in one request.
        aParam = [
            ['DirCreate', ['Dir3/Dir31']],
            ['List', ['Dir3']]
        ]
        '''
        Res = self.Fs.MassCalls(aParam)
        return {'data': Res}

    async def Move(self, aSrc: str, aDst: str) -> dict:
        '''
        move/rename file or directory.
        '''
        Res = self.Fs.Move(aSrc, aDst)
        return {'data': Res}

    async def ReadPos(self, aFile: str, aRequest: web.Request, aPos: int, aLen: int, aChankSize: int = 65535) -> dict:
        '''
        read binary file into sream by chukcs
        '''
        Len = self.Fs.Size(aFile)
        if (Len):
            Headers={'Content-Type': 'application/octet-stream', 'Custom-Header': json.dumps({'data': Len})}
            Response = web.StreamResponse(status=200, headers=Headers)
            await Response.prepare(aRequest)
            await self.Fs.FileReadChunkPos(aFile, Response, aChankSize, aPos, aLen)
            await Response.write_eof()
            return {'response': Response}

    async def ReadStr(self, aFile: str) -> dict:
        '''
        read text file.
        '''
        Res = self.Fs.FileReadStr(aFile)
        return {'data': Res}

    async def Size(self, aFile: str) -> dict:
        '''
        get size file or directory.
        '''
        Len = self.Fs.Size(aFile)
        return {'data': Len}

    async def Truncate(self, aFile: str, aSize: int = 0) -> dict:
        '''
        create file or set file size.
        '''
        Len = self.Fs.FileTruncate(aFile, aSize)
        return {'data': Len}

    async def WritePos(self, aFile: str, aRequest: web.Request, aPos: int, aChankSize: int = 65535) -> dict:
        '''
        write binary file from sream by chukcs
        '''
        Res = await self.Fs.FileWriteChunkPos(aFile, aRequest.content, aChankSize, aPos, aRequest.content_length)
        return {'data': Res}

    async def WriteStr(self, aFile: str, aData: str) -> dict:
        '''
        write text file.
        '''
        Res = self.Fs.FileWriteStr(aFile, aData)
        return {'data': Res}
