#!/usr/bin/env python3

# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>


import json
import asyncio
import aiohttp


class TAllNotesApi():
    def __init__(self, aUrl):
        self.Root = aUrl

    async def SendJson(self, aPath: str, aData: dict) -> dict:
        Headers = {'Content-Type': 'application/json'}
        Auth = aiohttp.BasicAuth('user01', 'passw01')

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
        'Content-Type': 'application/octet-stream',
        'Custom-Header': json.dumps(aData)
        }
        Auth = aiohttp.BasicAuth('user01', 'passw01')

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

    # --- VFS

    async def Copy(self, aSrc: str, aDst: str) -> dict:
        Data = {
            'method': 'Copy',
            'param': {
                'aSrc': aSrc,
                'aDst': aDst
            }
        }
        return await self.SendJson('file', Data)

    async def Delete(self, aFileOrDir: str) -> dict:
        Data = {
            'method': 'Delete',
            'param': {
                'aFile': aFileOrDir
            }
        }
        return await self.SendJson('file', Data)

    async def DirCreate(self, aDir: str) -> dict:
        Data = {
            'method': 'DirCreate',
            'param': {
                'aDir': aDir
            }
        }
        return await self.SendJson('file', Data)

    async def Exists(self, aFileOrDir: str) -> dict:
        Data = {
            'method': 'Exists',
            'param': {
                'aFile': aFileOrDir
        }
        }
        return await self.SendJson('file', Data)

    async def FileReadPos(self, aFile: str, aPos: int, aLen: int) -> dict:
        Data = {
            'method': 'ReadPos',
            'param': {
                'aFile': aFile,
                'aPos': aPos,
                'aLen': aLen,
                'aChankSize': 65536
            }
        }
        return await self.SendBytes('file', Data)

    async def FileReadStr(self, aFile: str) -> dict:
        Data = {
            'method': 'ReadStr',
            'param': {
                'aFile': aFile
            }
        }
        return await self.SendJson('file', Data)

    async def FileTruncate(self, aFile: str, aSize: int) -> dict:
        Data = {
            'method': 'Truncate',
            'param': {
                'aFile': aFile,
                'aSize': aSize
            }
        }
        return await self.SendJson('file', Data)

    async def FileWritePos(self, aFile: str, aBytes: bytes, aPos: int) -> dict:
        Data = {
            'method': 'WritePos',
            'param': {
                'aFile': aFile,
                'aPos': aPos,
                'aChankSize': 65536
            }
        }
        return await self.SendBytes('file', Data, aBytes)

    async def FileWriteStr(self, aFile: str, aData: str) -> dict:
        Data = {
            'method': 'WriteStr',
            'param': {
                'aFile': aFile,
                'aData': aData
            }
        }
        return await self.SendJson('file', Data)

    async def Help(self) -> dict:
        Data = {
            'method': 'Help',
            'param': {}
        }
        return await self.SendJson('file', Data)

    async def List(self, aPath: str) -> dict:
        Data = {
            'method': 'List',
            'param': {
                'aPath': aPath
            }
        }
        return await self.SendJson('file', Data)

    async def MassCall(self, aParam: list) -> dict:
        Data = {
            'method': 'MassCall',
            'param': {
                'aParam': aParam
            }
        }
        return await self.SendJson('file', Data)

    async def MassCalls(self, aParam: list) -> dict:
        Data = {
            'method': 'MassCalls',
            'param': {
                'aParam': aParam
            }
        }
        return await self.SendJson('file', Data)

    async def Move(self, aSrc: str, aDst: str) -> dict:
        Data = {
            'method': 'Move',
            'param': {
                'aSrc': aSrc,
                'aDst': aDst
            }
        }
        return await self.SendJson('file', Data)

    async def Size(self, aFileOrDir: str) -> dict:
        Data = {
            'method': 'Size',
            'param': {
                'aFile': aFileOrDir
            }
        }
        return await self.SendJson('file', Data)

    # --- Misc

    async def AppVer(self) -> dict:
        Data = {
            'method': 'AppVer',
            'param': {}
        }
        return await self.SendJson('info', Data)

    async def SysInfo(self) -> dict:
        Data = {
            'method': 'SysInfo',
            'param': {}
        }
        return await self.SendJson('info', Data)


async def Test_File(aUrl: str):
    AN = TAllNotesApi(aUrl)

    #Res = await AN.Help()
    #print('Help', Res)

    Dir = 'dir1/dir2'
    Res = await AN.DirCreate(Dir)
    print('DirCreate', Res)

    Calls = [
        ['DirCreate', ['Dir1']],
        ['DirCreate', ['Dir3/Dir31']],
        ['FileWriteStr', ['Dir4/file1.txt', '* file1 body *']],
        ['FileWriteStr', ['Dir4/file2.txt', '** file2 body **']],
        ['List', ['Dir4']]
    ]
    Res = await AN.MassCalls(Calls)
    print('MassCalls', Res)

    Calls = ['DirCreate', ['Dir3/Dir31'], ['Dir4/Dir41']]
    Res = await AN.MassCall(Calls)
    print('MassCall', Res)

    File = 'vAllNotesApi.py'
    with open(File, 'rb') as F:
        Data = F.read()
        Res = await AN.FileWritePos(f'{Dir}/{File}', Data, 0)
        print('FileWritePos', Res)

    Res = await AN.FileReadPos(f'{Dir}/{File}', 20, 50)
    print('FileReadPos', Res)

    Res = await AN.FileWriteStr(f'{Dir}/test.txt', 'Hello world of python')
    print('FileWriteStr', Res)

    Res = await AN.FileReadStr(f'{Dir}/test.txt')
    print('FileReadStr', Res)

    Res = await AN.Size(Dir)
    print('Size', Res)

    #Res = await AN.Delete('dir1/dir21')
    #Res = await AN.Delete(f'{Dir}/test.txt')
    #print('Delete', Res)

    Res = await AN.Exists(f'{Dir}/test.txt')
    print('Exists', Res)

    Res = await AN.FileTruncate(f'{Dir}/dir3/dump.dat', 10*1000)
    print('FileTruncate', Res)

    Res = await AN.Copy(Dir, 'DirCopy')
    print('Copy', Res)

    Res = await AN.Move('DirCopy', 'Dir3')
    print('Move', Res)

    #Res = await AN.List('')
    #print('List', Res)
    Res = await AN.List('dir1/dir2')
    print('List', Res)
    #Res = await AN.List(f'{Dir}/dir3/dump.dat')
    #print('List', Res)

async def Test_Info(aUrl: str):
    AN = TAllNotesApi(aUrl)

    Res = await AN.AppVer()
    print('AppVer', Res)

    Res = await AN.SysInfo()
    print('SysInfo', Res)

async def Test_Stress(aUrl: str, aCnt: int, aMaxConn: int):
    async def FetchSem(aAN, aSem, aIdx: int):
        nonlocal RemoteDir
        async with aSem:
            Data =  b'x' * (100_000 + aIdx)
            File = f'{RemoteDir}/File_{aIdx}.dat'
            Res = await aAN.FileWritePos(File, Data, 0)
            print('FileWritePos', File, Res)

    AN = TAllNotesApi(aUrl)
    RemoteDir = 'Stress'
    await AN.Delete(RemoteDir)
    Sem = asyncio.Semaphore(aMaxConn)
    Tasks = []
    for i in range(aCnt):
        Task = asyncio.create_task(FetchSem(AN, Sem, i + 1))
        Tasks.append(Task)
    await asyncio.gather(*Tasks)

    Files = await AN.List(RemoteDir)
    print('List', Files)

async def Main():
    UrlApi = 'http://localhost:8173'
    #UrlApi = 'http://it.findwares.com:8173'
    #UrlApi = 'https://it.findwares.com/amn'

    await Test_File(UrlApi)
    #await Test_Info(UrlApi)
    #await Test_Stress(UrlApi, 20, 5)

asyncio.run(Main())
