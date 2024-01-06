"""
Module Documentation: JSON

The `JSON` class is a versatile class that extends Python's dictionary capabilities with additional functionality for handling JSON-like data structures. It allows you to create and manipulate dictionaries with predefined keys and data types, making it convenient for working with structured data.

Usage:
1. Creating a JSON Object:
   - You can create a `JSON` object by instantiating the class with a dictionary or keyword arguments.

Example:
   ```python
   json = JSON({"a": 1, "b": "B"}, c=3)
   ```

2. Adding and Accessing Values:
   - You can add and access values using keys or attributes, similar to a regular dictionary.
   - Values are assigned and retrieved using square brackets for keys and dot notation for attributes.

Example:
   ```python
   json["d"] = 5
   json.e = 6
   print(f"json['d'] = json.d: {json.d}")
   ```

3. Handling JSON-Like Data:
   - The JSON class can manage nested dictionaries as values.
   - Nested dictionaries are automatically converted into JSON objects, allowing for seamless data manipulation.

Example:
   ```python
   json.payload = {"a": 4}
   print(f"json.payload['a']: {json.payload['a']}")
   ```

4. Error Handling:
   - The class includes error handling for invalid keys, data types, and missing dunder methods.
   - It raises KeyTypeError for unsupported key types and MissingError for objects without __str__ or __repr__ methods.

5. Utility Functions:
   - The class provides various utility functions for dictionary manipulation, such as update, get, delkey, and more.
   - You can also perform common dictionary operations like items(), keys(), and values().

Example:
   ```python
   print(f"len(json): {len(json)}")
   print(f"json.items(): {list(json.items())}")
   ```

6. JSON Serialization and Deserialization:
   - The JSON class offers the ability to dump dictionaries to JSON objects and retrieve dictionaries from JSON objects.
   - You can use the dumps method to convert dictionaries into JSON objects.
   _ You can use the to_dict method to convert JSON objects into dictionaries.

Example:
   ```python
   json_obj = JSON.dumps(a=9, b={"c": 2})
   print(f"json_obj: {json_obj}")
   ```

7. Inheritance and Base Classes:
   - The JSON class can be used as a base class for creating new classes with predefined keys and data types.
   - Attributes without any default value will be set to None.

Example:
   ```python
   class Packet(JSON):
    a: int
    b: float = 0.0
    ```

8. JSON Decorators:
   - The JSON class provides decorators for creating new classes with JSON-like functionality.
   - You can use the @JSON.json decorator to create classes that inherit from JSON.

Example:
   ```python
   @JSON.json
   class Packet:
    a: int = 2
    c: int

Note: The JSON class is designed to simplify working with structured data in Python, providing a convenient way to handle JSON-like data structures with predefined keys and data types.
"""

__author__ = "Pratik Das"

import types
from typing import (Any, Dict, Iterable, Optional, Self, Tuple, TypeVar,
                    overload)


class KeyTypeError(TypeError):
    ...


class MissingError(Exception):
    ...


class JSON:
    _VT = TypeVar("_VT")

    def __init_subclass__(cls) -> None:
        # Class variables provided with a default
        # value will be present in dir(cls),
        for attr in cls.__annotations__:
            if attr not in dir(cls):
                # but the ones absent from dir(cls)
                # are defaulted to None
                setattr(cls, attr, None)

    @overload
    def __init__(self, __map: Dict[str, _VT]) -> None:
        ...

    @overload
    def __init__(self, map: Dict[str, _VT], **kwds) -> None:
        ...

    @overload
    def __init__(self, **kwds) -> None: ...

    def __init__(self, map: Dict[str, _VT] = {}, **kwds) -> None:
        # Class variables will be absent from self.__dict__,
        # thus it needs to be updated explicitly with the
        # values provided to the class variables
        for k in self.__annotations__ or []: # When the initializer
            # is directly called, then self.__annotations__ will be none
            self[k] = getattr(self.__class__, k)
        self.update(map, **kwds)

    @overload
    def update(self, __map: Dict[str, _VT]) -> None:
        ...

    @overload
    def update(self, map: Dict[str, _VT], **kwds) -> None:
        ...

    @overload
    def update(self, **kwds) -> None: ...

    def update(self, map: Dict[str, _VT] = {}, **kwds) -> None:
        for k, v in map.items():
            self[k] = v
        for k, v in kwds.items():
            self[k] = v
        # __annotations__ needs to be popped from __dict__
        self.pop("__annotations__", None)

    def delkey(self, __key: str) -> None:
        del self.__dict__[__key]

    __delattr__ = __delitem__ = delkey

    def getvalue(self, __key: str) -> Optional[_VT]:
        if __key in self.__dict__:
            return self.__dict__[__key]
        self.__dict__[__key] = None

    __getattr__ = __getitem__ = getvalue

    def haskey(self, __key: str) -> bool:
        return __key in self.__dict__

    __hasattr__ = __contains__ = haskey

    def setvalue(self, __key: str, __value: _VT) -> None:
        if isinstance(__key, str):
            pass
        elif isinstance(__key, object):
            if isinstance(__key, type):
                raise KeyTypeError(f"{__key} cannot be a 'type'")
            if hasattr(__key, "__str__"):
                __key = str(__key)
            elif hasattr(__key, "__repr__"):
                __key = repr(__key)
            else:
                raise MissingError(f"__str__ or __repr__ dunder missing in {__key}")
        else:
            raise KeyTypeError(
                f"{__key} must be a string or an object(with __str__ or __repr__ dunder), but not a type itself"
            )
        if isinstance(__value, dict):
            __value = types.new_class(
                "".join(w.capitalize() for w in __key.split("_")), (JSON,)
            )(__value)
        self.__dict__[__key] = __value

    __setattr__ = __setitem__ = setvalue

    def __len__(self) -> int:
        return len(self.__dict__)

    def __iter__(self) -> Iterable[str]:
        for key in self.__dict__:
            yield key

    def __copy__(self) -> Self:
        return __class__(self.to_dict())

    def copy(self) -> Self:
        return self.__copy__()

    def clear(self) -> None:
        self.__dict__.clear()

    @overload
    def get(self, __key: str) -> Optional[_VT]:
        ...

    @overload
    def get(self, __key: str, __default: _VT) -> _VT:
        ...

    def get(self, __key: str, __default: Optional[_VT] = None) -> Optional[_VT]:
        return self.__dict__.get(__key, __default)

    def items(self) -> Iterable[Tuple[str, _VT]]:
        return self.to_dict().items()

    def keys(self) -> Iterable[str]:
        return self.to_dict().keys()

    @overload
    def pop(self, __key: str) -> _VT: ...

    @overload
    def pop(self, __key: str, __default: _VT) -> Optional[_VT]: ...

    def pop(self, __key: str, __default: Optional[_VT] = None) -> _VT:
        return self.__dict__.pop(__key, __default)

    def popitem(self) -> Tuple[str, _VT]:
        return self.__dict__.popitem()

    @overload
    def setdefault(self, __key: str) -> Optional[_VT]:
        ...

    @overload
    def setdefault(self, __key: str, __default: _VT) -> _VT:
        ...

    def setdefault(self, __key: str, __default: Optional[_VT] = None) -> Optional[_VT]:
        return self.__dict__.setdefault(__key, __default)

    def values(self) -> Iterable[_VT]:
        return self.to_dict().values()

    def __eq__(self, __other: Self) -> bool:
        return self.__dict__ == __other.__dict__

    def join(self, __other: Self) -> Self:
        for k, v in __other.__dict__.items():
            self.__dict__[k] = v
        return self

    __or__ = __ior__ = join

    def __ror__(self, __other: Self) -> Self:
        return __other.join(self)

    def __str__(self) -> str:
        return (
            "{"
            + ", ".join(f"{key}: {str(val)}" for key, val in self.__dict__.items())
            + "}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            + ", ".join(f"{key} = {repr(val)}" for key, val in self.__dict__.items())
            + ")"
        )

    @overload
    @classmethod
    def fromkeys(cls, __iterable: Iterable[str]) -> Self: ...

    @overload
    @classmethod
    def fromkeys(cls, __iterable: Iterable[str], __value: _VT) -> Self: ...

    @classmethod
    def fromkeys(cls, __iterable: Iterable[str], __value: Optional[_VT] = None) -> Self:
        self = cls()
        for key in __iterable:
            self[key] = __value
        return self

    @overload
    @staticmethod
    def dumps(__map: Dict[str, Any]) -> Self: ...

    @overload
    @staticmethod
    def dumps(map: Dict[str, Any], **kwds) -> Self: ...

    @overload
    @staticmethod
    def dumps(**kwds) -> Self: ...

    @staticmethod
    def dumps(map: Dict[str, Any] = {}, **kwds) -> Self:
        return JSON(map, **kwds)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v.to_dict() if isinstance(v, JSON) else v for k, v in self.__dict__.items()}

    @staticmethod
    def json(__cls: type) -> type:
        # The base classes must be in order of __cls, JSON,
        # so as not to overwrite the dunders in __cls
        __new_cls = types.new_class(__cls.__name__, (__cls, JSON))
        # Inheritance does not carry over the __annotations__
        # from the base classes to child class,
        # that's why it needs to be explicitly updated
        __new_cls.__annotations__.update(__cls.__annotations__)
        __new_cls.__init_subclass__()
        return __new_cls


if __name__ == "__main__":
    print(f"{(json := JSON({"a": 1, "b": "B"}, c=3))=}")
    json["d"] = 5
    json.e = 6
    print(f"json['d'] = {json.d=}")
    print(f"json.e = {json["e"]=}")
    json.d = 3
    json["e"] = 7
    print(f"{json=}")
    json.payload = {"a": 4}
    print(f"json.payload = {dict(a = 4)}\n{json["payload"]=}")
    print(f"{json["payload"].a=}")
    print(f"{json.payload.a=}")
    print(f"{json.payload["a"]=}")
    print(f"{json["payload"]["a"]=}")
    print(f"{"g" in json=}")
    print(f"{json["g"]=}")
    print(f"{"f" in json=}")
    print(f"{json.f=}")
    print(f"{"h" in json=}")
    print(f"{json=}")
    print(f"{repr(json)=}")
    print(f"{len(json)=}")
    print(f"json.items(): {list(json.items())}")


    print("\nDictionaries can be dumped")
    print(f"{repr(JSON.dumps(a = 9, b = {"c": 2}))=}")
    print("and JSON can be converted to pure dictionary")
    print(f"{json.to_dict()=}")

    print("\nCan also be used a base class")

    class Packet(JSON):
        a: int
        b: float = 0.0

    print("class Packet(JSON):\n    a: int\n    b: float = 0.0")
    print(f"{(packet := Packet(a=2, b=6))=}")
    print(f"{repr(packet)=}")
    packet.pay_load = {"src": "n1", "dst": "n2"}
    print(f"packet.pay_load = {dict({"src": "n1", "dst": "n2"})}")
    print(f"{packet=}")
    print(f"{repr(packet)=}")

    print("\nDecorators are also available")

    @JSON.json
    class Packet:
        a: int = 2
        c: int

    print("@JSON.json\nclass Packet:\n    a: int = 2\n    c: int")
    print(f"{Packet(a=6, b=5)=}")
    print(f"{Packet({"c": 3})=}")
