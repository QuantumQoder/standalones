"""
Module Documentation: SequencedDict

The SequencedDict class is an extension of the UserDict class from the collections module, providing a dictionary-like data structure with additional features for indexing and slicing keys. It maintains the order of keys and allows you to access items using keys, integers, or slices.

Usage:
1. Creating an SequencedDict:
   - You can create an SequencedDict using the constructor with a dictionary or keyword arguments.

Example:
   d = SequencedDict({"a": 1, "b": 2}, c=3)

2. Accessing Items:
   - Access items using keys, integers, or slices.
   - Keys can be accessed using square brackets just like a regular dictionary.
   - Integers and slices can be used to access keys and corresponding values.

Examples:
   - Accessing by key: d['a'] or d['b']
   - Accessing by integer index: d[0] (key 'a') or d[1] (key 'b')
   - Accessing by slice: d[1:] (keys 'b' and 'c')

3. Modifying Items:
   - You can add, modify, or remove items using standard dictionary methods like __setitem__ and __delitem__.

Example:
   - Adding a new item: d['d'] = 4
   - Modifying an existing item: d['a'] = 10
   - Removing an item: del d['b']

4. Additional Features:
   - SequencedDict maintains the order of keys in the order they were added.
   - If a key is added multiple times, it will still appear only once in the order.
   - The class provides additional methods for indexing and slicing the dictionary.

Example:
   - Slicing by index: d[1:3] (keys 'b' and 'c')
   - Slicing by reverse index: d[-2:] (keys 'b' and 'c')

5. Error Handling:
   - If you try to access a key, integer, or slice that doesn't exist, a KeyError will be raised.

Example:
   - Accessing a non-existing key: d['x']
   - Accessing a non-existing integer index: d[5]
   - Accessing a non-existing slice: d[2:4]

6. Inheriting from UserDict:
   - The SequencedDict class is inherited from the UserDict class, providing dictionary-like behavior.

Example:
   - You can use standard dictionary methods like len(d), 'in' operator, etc.

Note: This class is a convenient way to work with dictionaries while keeping track of the order of keys and offering advanced slicing and indexing capabilities.
"""

__author__ = "Pratik Das"

from collections import UserDict
from typing import Dict, List, Optional, TypeVar, Union, overload, override

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class SequencedDict(UserDict):
    @overload
    def __init__(self, __dict: Dict[_KT, _VT]) -> None:
        ...

    @overload
    def __init__(self, dict: Dict[_KT, _VT], **kwds) -> None:
        ...

    @overload
    def __init__(self, **kwds) -> None:
        ...

    def __init__(self, dict: Optional[Dict[_KT, _VT]] = None, **kwds) -> None:
        self.__keys: List[_KT] = []
        UserDict.__init__(self, dict, **kwds)

    @override
    def __setitem__(self, __key: _KT, __item: _VT) -> None:
        UserDict.__setitem__(self, __key, __item)
        if __key not in self.__keys:
            self.__keys.append(__key)

    @overload
    def __getitem__(self, __key: int) -> Dict[_KT, _VT]:
        ...

    @overload
    def __getitem__(self, __key: slice) -> Dict[_KT, _VT]:
        ...

    @overload
    def __getitem__(self, __key: _KT) -> _VT:
        ...

    def __getitem__(self, __key: Union[_KT, int, slice]) -> Union[_VT, Dict[_KT, _VT]]:
        return UserDict.__getitem__(self, __key)

    @overload
    def __missing__(self, __key: int) -> Dict[_KT, _VT]:
        ...

    @overload
    def __missing__(self, __key: slice) -> Dict[_KT, _VT]:
        ...

    def __missing__(self, __key: Union[int, slice]) -> Dict[_KT, _VT]:
        if isinstance(__key, int) and __key < len(self):
            k: _KT = self.__keys[__key]
            return {k: self.data[k]}
        if isinstance(__key, slice):
            ks: List[_KT] = self.__keys[__key]
            return {k: self.data[k] for k in ks}
        raise KeyError(__key)

    @overload
    def __delitem__(self, __key: int) -> None:
        ...

    @overload
    def __delitem__(self, __key: slice) -> None:
        ...

    @overload
    def __delitem__(self, __key: _KT) -> None:
        ...

    @override
    def __delitem__(self, __key: Union[_KT, int, slice]) -> None:
        try:
            del self.data[__key]
            del self.__keys[__key]
        except KeyError:
            if isinstance(__key, int) and __key < len(self):
                k: _KT = self.__keys[__key]
                del self.data[k]
                del self.__keys[k]
            if isinstance(__key, slice):
                ks: List[_KT] = self.__keys[__key]
                for k in ks:
                    del self.data[k]
                    del self.__keys[k]
            raise KeyError(__key)

if __name__ == "__main__":
    print(f"{(d := SequencedDict({"a": 1, "b": 2}, c=3))=}")
    print(f"{d['a']=}")
    print(f"{d[2]=}")
    print(f"{d[-1]=}")
    print(f"{d[1:]=}")
    print(f"{d[:4]=}")
