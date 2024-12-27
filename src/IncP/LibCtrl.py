# Created: 2024.12.27
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Var.Dict import DeepGetByList, GetDictDefs
from .Log import Log


def ResGetItem(aData: dict, aName: str) -> str:
    return aData['res'].get(aName, '')
