"""
Module Documentation: PrototypeFactory

This module defines a decorator called 'Prototype' that can be used to dynamically create classes, or extend them for that matter, in order for the class' object to behave as a prototype for its child classes. In other words, the decorator allows you to perform prototype-based programming in python. The only side effect is that the objects, defined as the prototype can not be used as callables.

Usage:
1. Creating a Prototype:
   - Use the Prototype function to make a prototype of your class

Example:
   ```python
   class Foo:
       def __init__(self, *args, **kwds):
           pass
   Foo_prototype = Prototype(Foo, *args, **kwds)
   ```

2. Converting your class to create prototype:
   - Use the Prototype function to convert your class to create prototype

Example:
   ```python
   class Foo:
       def __init__(self, *args, **kwds):
           pass
   Foo = Prototype(Foo)
   Foo_prototype = Foo(*args, **kwds)
   ```

3. Protoype Decorator:
   - The Prototype function can also be used as a class decorator

Example:
   ```python
   @Prototype
   class Foo:
       def __init__(self, *args, **kwds):
           pass
   Foo_prototype = Foo(*args, **kwds)
   ```

4. Inheritance and Base Classes:
   - The Prototype function can also acts a base class for your class to inherit from
   - The only catch is that the prototype can not be used as a callable.

Example:
   ```python
   class Foo(Prototype):
       def __init__(self, *args, **kwds):
           pass
   Foo_prototype = Foo(*args, **kwds)
   ```

2. Use Cases and Examples:
   - Creating prototypes and instantiating new classes.
   - Defining attributes for new classes on the fly.

Example:
   # Creating a prototype and using it to create new instances
   class BaseClass:
       pass

   proto = Prototype(BaseClass, "NewClass", (BaseClass,), {"attribute": 42})
   new_instance = proto()

   # Creating multiple prototypes with different attributes
   class AnotherBaseClass:
       pass

   proto_2 = Prototype(AnotherBaseClass, "AnotherNewClass", (AnotherBaseClass,), {"attribute": "example"})
   new_instance_2 = proto_2()

3. Class: PrototypeMeta
   - Contains methods to control the creation behavior of the Prototype class.

Methods:
   - __new__(cls, name, bases, namespace) -> Self: Creates a new instance of the metaclass.

4. Function: Prototype
   - Dynamically creates classes based on the specified attributes using metaprogramming techniques.

Parameters:
   - __cls: type: Class to be instantiated.
   - *args: Variable positional arguments.
   - **kwds: Variable keyword arguments.

Returns:
   - Union[type, object]: Returns a new class or object instance based on the provided arguments.

Functionality:
   - Constructs new classes using metaprogramming techniques by utilizing __new__, __init__, and __call__ methods.

Note: This module allows for prototype-based programming, useful for classless scenarios. The only side effect is that prototype classes can't be callable.
"""

__author__ = "Pratik Das"

from typing import Optional, Self, Tuple, Type, Union


def Prototype(__cls: Optional[type] = None, *args, **kwds) -> Union[type, object]:
    __cls = __cls or type(
        "Prototype", (), {"__new__": lambda cls, *args, **kwds: object.__new__(cls)}
    )

    def __new__(cls, *args, **kwds) -> Self:
        if (
            len(args) == 3
            and isinstance(args[0], str)
            and isinstance(args[1], tuple)
            and isinstance(args[2], dict)
        ):
            cls.__subcls_name = args[0]
            cls.__subcls_bases = tuple(
                arg if isinstance(arg, type) else arg.__class__ for arg in args[1]
            )
            cls.__subcls_ns = args[2]
        return __cls.__new__(cls)

    def __call__(self, *args, **kwds) -> object:
        __new_cls = type(self.__subcls_name, self.__subcls_bases, self.__subcls_ns)
        return __new_cls(*args, **kwds)

    __new_cls = type(
        __cls.__name__,
        (__cls,),
        {"__new__": __new__, "__call__": __call__},
    )
    if args or kwds:
        return __new_cls(*args, **kwds)
    return __new_cls


def _prototype_mro_entries(bases) -> Tuple[Type[Prototype()]]:
    assert Prototype in bases
    return (Prototype(),)


Prototype.__mro_entries__ = _prototype_mro_entries
