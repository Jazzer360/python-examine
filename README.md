# examine
#### A simple library for examining complex data structures

The main component of this library is the structure parser that allows you to easily see the resulting structure of python object:
```python
>>> import examine
>>> mock_api_response = {
...   'name': 'username',
...   'interests': ['coding', 'snowboarding'],
...   'location': {'country': 'USA', 'state': 'MN'}}
>>> print(examine.Structure(mock_api_response))
dict
  interests - [str]
  location - dict
    country - str
    state - str
  name - str
```

### Installation
```pip install examine```

### Usage
To use this library, you simply pass any object to the `Structure(obj)` constructor. This gives you a Structure object. While not terribly interesting on it's own, it can be passed to the str function (or simply passed to print) to return an easy-to-interpret layout of the object hierarchy.
```python
>>> print(examine.Structure('string'))
str
>>> print(examine.Structure([1, 2, 3]))
[int]
>>> print(examine.Structure([{'key1': 'val1'}, {'key2': 'val2'}]))
[dict]
  *key1 - str
  *key2 - str
>>> print(examine.Structure({'key1': {'subkey1': 'subvalue'}}))
dict
  key1 - dict
    subkey1 - str
>>> examine.Structure('string')
<examine.examine.Structure object at ...>
```

### Display Format
##### Simple cases
The format is pretty simple. The type of the root object used to create the Structure will be the first line (usually a dict or array of dicts):
```python
>>> print(examine.Structure({}))
dict
```
Following that, there will be all of the keys present in the dict, or in the case of a list of dicts, any key present:
```python
>>> print(examine.Structure({'key1': 'val', 'key2': 2.0}))
dict
  key1 - str
  key2 - float
```
##### Common dict structure
When dealing with a list of dicts, any key found in any of the dicts will be listed as keys. If a key is not found in every dict in the list, it is denoted with an asterisk indicating that the key is not always present:
```python
>>> print(examine.Structure([
...   {'key1': 'val1', 'key2': 'val2'},
...   {'key1': 'val1'}]))
[dict]
  key1 - str
  *key2 - str
```
When you are inspecting the common structure of multiple dicts in a list, and the underlying value for a key is sometimes `None`, there will be an asterisk for that key's value type indicating that the underlying value for that key may sometimes be `None`.
```python
>>> print(examine.Structure([{'key': 'val'}, {'key': None}]))
[dict]
  key - *str
```
##### More on lists
When looking at a list of a type that sometimes has a `None` value, the value type will have an asterisk in front of it, indicating that some of the values in the list may be `None`.
```python
>>> print(examine.Structure([1, 2, None]))
[*int]
```
When dealing with a list containing mixed types, it will be indicated with the type `<mixed-type>`:
```python
>>> print(examine.Structure([1, 'str', {'key': 'val'}]))
[<mixed-type>]
```
##### Tuples
Tuples are typically used with non-homogeneous values, and as such, this library tries to give you useful information about the contents of tuples. Here is a simple example of a tuple.
```python
>>> print(examine.Structure(('string', 1)))
(str, int)
```
Since a tuple may contain multiple dicts, and each may have it's own structure, this library does not automatically give you the structure of dicts that are part of a tuple. If you want to find out those structures, you must do so manually.
```python
>>> atuple = ({'key': 'val'}, {'anotherkey': 'anotherval'})
>>> print(examine.Structure(atuple))
(dict, dict)

>>> print(examine.Structure(atuple[0]))
dict
  key - str
  
>>> print(examine.Structure(atuple[1]))
dict
  anotherkey - str
```
##### Putting things together
Here is an example result of a more complicated structure:
```python
>>> print(examine.Structure({
...   'key1': 'val1',
...   'key2': [1, 2, 3],
...   'key3': [{
...     'sub1': 'subval1',
...     'sub2': 1},{
...     'sub1': 'subval1',
...     'sub2': 'str',
...     'sub3': 3}],
...   'key4': {'subkey': 'val'},
...   'key5': [1, 'str', {'key': 'val'}]}))
dict
  key1 - str
  key2 - [int]
  key3 - [dict]
    sub1 - str
    sub2 - <mixed-type>
    *sub3 - int
  key4 - dict
    subkey - str
  key5 - [<mixed-type>]
```
In this case we can determine the following:
- root object is a dict
- root object has the keys: key1, key2, key3, key4, key5
- key1 on root is a string
- key2 on root is an array of ints
- key3 on root is an array of dicts
- key4 on root is a dict
- for the dict held by key4, subkey is a string
- key5 on root is a list of mixed types

For the list of dicts held by key3:
- sub1 is always a string for dicts in that list
- sub2 is always an unknown type for dicts in that list
- sub3 is SOMETIMES an int for dicts in that list
