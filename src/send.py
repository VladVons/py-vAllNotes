#!/usr/bin/env python3

# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>


import json
import asyncio
import aiohttp


async def SendJson(aUrl: str, aData: dict) -> dict:
    Headers = {"Content-Type": "application/json"}
    Auth = aiohttp.BasicAuth("user01", "passw01")

    try:
        async with aiohttp.ClientSession(auth=Auth) as session:
            async with session.post(aUrl, json=aData, headers=Headers) as Response:
                if (Response.status == 200):
                    Data = await Response.json()
                    Res = {'status': Response.status, 'responce': Data}
                else:
                    Res = {'status': Response.status}
    except Exception as E:
        EType = type(E).__name__
        Res = {'err': f'{EType}, {E}' , 'status': -1}
    return Res

async def SendBytes(aUrl: str, aData: dict, aBytes: bytes = None) -> dict:
    Headers = {
      "Content-Type": "application/octet-stream",
      "Custom-Header": json.dumps(aData)
    }
    Auth = aiohttp.BasicAuth("user01", "passw01")

    try:
        async with aiohttp.ClientSession(auth=Auth) as session:
            async with session.post(aUrl, data=aBytes, headers=Headers) as Response:
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


async def FileRead(aFile: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Read",
      "param": {
        "aFile": aFile
      }
    }
    return await SendJson(Url, Data)

async def FileReadPos(aFile: str, aPos: int, aLen: int) -> dict:
    Url = "http://localhost:8173/apiBytes/file"
    Data = {
      "method": "ReadPos",
      "param": {
        "aFile": aFile,
        "aPos": aPos,
        "aLen": aLen,
        "aChankSize": 65536
      }
    }
    return await SendBytes(Url, Data)

async def FileWrite(aFile: str, aData: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Write",
      "param": {
        "aFile": aFile,
        "aData": aData
      }
    }
    return await SendJson(Url, Data)

async def FileWritePos(aFile: str, aBytes: bytes, aPos: int) -> dict:
    Url = "http://localhost:8173/apiBytes/file"
    Data = {
      "method": "WritePos",
      "param": {
        "aFile": aFile,
        "aPos": aPos,
        "aChankSize": 65536
      }
    }
    return await SendBytes(Url, Data, aBytes)

async def FileSize(aFile: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Size",
      "param": {
        "aFile": aFile
      }
    }
    return await SendJson(Url, Data)

async def FileExists(aFile: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Exists",
      "param": {
        "aFile": aFile
      }
    }
    return await SendJson(Url, Data)

async def FileDelete(aFile: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Delete",
      "param": {
        "aFile": aFile
      }
    }
    return await SendJson(Url, Data)

async def FileTruncate(aFile: str, aSize: int) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "Truncate",
      "param": {
        "aFile": aFile,
        "aSize": aSize
      }
    }
    return await SendJson(Url, Data)

async def DirCreate(aFile: str) -> dict:
    Url = "http://localhost:8173/apiJson/file"
    Data = {
      "method": "DirCreate",
      "param": {
        "aFile": aFile
      }
    }
    return await SendJson(Url, Data)


async def Main():
    Dir = 'dir1/dir2'

    Res = await DirCreate(Dir)
    print('DirCreate', Res)

    File = 'send.py'
    with open(File, 'rb') as F:
      Data = F.read()
      Res = await FileWritePos(f'{Dir}/{File}', Data, 0)
      print('FileWritePos', Res)

    Res = await FileReadPos(f'{Dir}/{File}', 20, 50)
    print('FileReadPos', Res)

    Res = await FileWrite(f'{Dir}/test.txt', 'Hello world of python')
    print('FileWrite', Res)

    Res = await FileRead(f'{Dir}/test.txt')
    print('FileRead', Res)


    Res = await FileSize(f'{Dir}/test.txt')
    print('FileSize', Res)

    #Res = await FileDelete(f'{Dir}/test.txt')
    #print('FileDelete', Res)

    Res = await FileExists(f'{Dir}/test.txt')
    print('FileExists', Res)

    Res = await FileTruncate(f'{Dir}/dump.dat', 10*1000)
    print('FileTruncate', Res)

asyncio.run(Main())
