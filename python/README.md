This folder contains the following independent python files:-
- [json_type.py](https://github.com/QuantumQoder/standalones/blob/main/python/json_type.py)
- [prototype.py](https://github.com/QuantumQoder/standalones/blob/main/python/prototype.py)
- [sequenced_dict.py](https://github.com/QuantumQoder/standalones/blob/main/python/sequenced_dict.py)

Each one introduing a new feature or implementation of a logic.

## json_type.py

This contains a class which creates a object acting in the exact same manner as a javascript object. The values defined in the object can be accessed as keys, as well as, as attributes. For further details, check the module documentation.

## prototype.py

Python offers object-oriented programming, which is primarily class-based. This module provides with a function "Prototype" which changes the behaviour of a class, whose objects can then be used as prototypes, meaning that child classes can extend from the base object. Not only this, but below this inheritance, every class (or, their object) would act as a prototype

The only side effect would be that prototypes can't be defined as callables.

## sequenced_dict.py

Dictionaries are a great way to create mappings with key-value pair, but the only issue with python's in-built dictionary is that they can't be indexed/sliced. This module provides the class "SequencedDict" which resolves the issue of indexing. Any value in a SequencedDict can be accessed through keys, indices or slices, while still retaining other dictionary functionalities. Also, the ability of indexing and slicing means that SequencedDict's are inherently ordered.