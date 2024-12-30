#!/usr/bin/env python3

# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>


import json
import asyncio
import aiohttp


class TAllNotesFS():
    def __init__(self, aUrl):
        self.Root = aUrl

    async def SendJson(self, aPath: str, aData: dict) -> dict:
        Headers = {"Content-Type": "application/json"}
        Auth = aiohttp.BasicAuth("user01", "passw01")

        try:
            async with aiohttp.ClientSession(auth=Auth) as session:
                async with session.post(f'{self.Root}/apiJson/{aPath}', json=aData, headers=Headers) as Response:
                    if (Response.status == 200):
                        Data = await Response.json()
                        Res = {'status': Response.status, 'responce': Data}
                    else:
                        Res = {'status': Response.status}
        except Exception as E:
            EType = type(E).__name__
            Res = {'err': f'{EType}, {E}' , 'status': -1}
        return Res

    async def SendBytes(self, aPath: str, aData: dict, aBytes: bytes = None) -> dict:
        Headers = {
        "Content-Type": "application/octet-stream",
        "Custom-Header": json.dumps(aData)
        }
        Auth = aiohttp.BasicAuth("user01", "passw01")

        try:
            async with aiohttp.ClientSession(auth=Auth) as Session:
                async with Session.post(f'{self.Root}/apiBytes/{aPath}', data=aBytes, headers=Headers) as Response:
                    if (Response.status == 200):
                        #--- Chank read example
                        # aData.get('aChankSize', 65536)
                        # async for xBlock in Response.content.iter_chunked():
                        #   pass
                        # ---
                        if ('json' in Response.content_type):
                            Data = await Response.json()
                        else:
                            Data = await Response.read()
                    else:
                        Data = None
                    Res = {'responce': Data, 'status': Response.status, 'type': Response.content_type}
        except Exception as E:
            EType = type(E).__name__
            Res = {'err': f'{EType}, {E}' , 'status': -1}
        return Res

    async def FileRead(self, aFile: str) -> dict:
        Data = {
            "method": "Read",
            "param": {
                "aFile": aFile
            }
        }
        return await self.SendJson('file', Data)

    async def FileReadPos(self, aFile: str, aPos: int, aLen: int) -> dict:
        Data = {
            "method": "ReadPos",
            "param": {
                "aFile": aFile,
                "aPos": aPos,
                "aLen": aLen,
                "aChankSize": 65536
            }
        }
        return await self.SendBytes('file', Data)

    async def FileWrite(self, aFile: str, aData: str) -> dict:
        Data = {
            "method": "Write",
            "param": {
                "aFile": aFile,
                "aData": aData
            }
        }
        return await self.SendJson('file', Data)

    async def FileWritePos(self, aFile: str, aBytes: bytes, aPos: int) -> dict:
        Data = {
            "method": "WritePos",
            "param": {
                "aFile": aFile,
                "aPos": aPos,
                "aChankSize": 65536
            }
        }
        return await self.SendBytes('file', Data, aBytes)

    async def FileSize(self, aFile: str) -> dict:
        Data = {
            "method": "Size",
            "param": {
                "aFile": aFile
            }
        }
        return await self.SendJson('file', Data)

    async def FileExists(self, aFile: str) -> dict:
        Data = {
            "method": "Exists",
            "param": {
                "aFile": aFile
        }
        }
        return await self.SendJson('file', Data)

    async def FileDelete(self, aFile: str) -> dict:
        Data = {
            "method": "Delete",
            "param": {
                "aFile": aFile
            }
        }
        return await self.SendJson('file', Data)

    async def FileTruncate(self, aFile: str, aSize: int) -> dict:
        Data = {
            "method": "Truncate",
            "param": {
                "aFile": aFile,
                "aSize": aSize
            }
        }
        return await self.SendJson('file', Data)

    async def DirCreate(self, aFile: str) -> dict:
        Data = {
            "method": "DirCreate",
            "param": {
                "aFile": aFile
            }
        }
        return await self.SendJson('file', Data)

    async def FileList(self, aPath: str) -> dict:
        Data = {
            "method": "List",
            "param": {
                "aPath": aPath
            }
        }
        return await self.SendJson('file', Data)

async def Main():
    #Url = 'http://localhost:8173'
    Url = 'http://1x1.com.ua:8173'

    FS = TAllNotesFS(Url)
    Dir = 'dir1/dir2'

    Res = await FS.DirCreate(Dir)
    print('DirCreate', Res)

    File = 'vAllNotesSend.py'
    with open(File, 'rb') as F:
        Data = F.read()
        Res = await FS.FileWritePos(f'{Dir}/{File}', Data, 0)
        print('FileWritePos', Res)

    Res = await FS.FileReadPos(f'{Dir}/{File}', 20, 50)
    print('FileReadPos', Res)

    Res = await FS.FileWrite(f'{Dir}/test.txt', 'Hello world of python')
    print('FileWrite', Res)

    Res = await FS.FileRead(f'{Dir}/test.txt')
    print('FileRead', Res)

    Res = await FS.FileSize(f'{Dir}/test.txt')
    print('FileSize', Res)

    #Res = await FS.FileDelete(f'{Dir}/test.txt')
    #print('FileDelete', Res)

    Res = await FS.FileExists(f'{Dir}/test.txt')
    print('FileExists', Res)

    Res = await FS.FileTruncate(f'{Dir}/dir3/dump.dat', 10*1000)
    print('FileTruncate', Res)


    Res = await FS.FileList('')
    #Res = await FS.FileList('dir1/dir2/dir3')
    print('FileList', Res)


asyncio.run(Main())