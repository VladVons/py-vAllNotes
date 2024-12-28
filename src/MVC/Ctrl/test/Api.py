# Created: 2024.12.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from IncP.CtrlBase import TCtrlBase


class TMain(TCtrlBase):
    async def main(self, **aData: dict) -> dict:
        return {'x': 'y'}
