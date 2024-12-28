#!/usr/bin/env python3

import aiohttp
import asyncio

async def Send(aUrl: str, aData: dict, aAuth: None) -> dict:
    Headers = {"Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession(auth=aAuth) as session:
            async with session.post(aUrl, json=aData, headers=Headers) as Response:
                if (Response.status == 200):
                    Data = await Response.read()
                    Res = {'status': Response.status, 'data': Data}
                else:
                    Res = {'status': Response.status}
    except Exception as E:
        EType = type(E).__name__
        Res = {'err': f'{EType}, {E}' , 'status': -1}
    return Res

async def Main():
    Url = "http://localhost:8173/api/test"
    Data = {
      "method": "main",
      "param": {
        "key1": "value1", 
        "key2": "value2"
      }
    }
    Auth = aiohttp.BasicAuth("user01", "passw01")
    Res = await Send(Url, Data, Auth)
    print(Res)

asyncio.run(Main())
