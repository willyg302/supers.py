![supers.py](https://rawgit.com/willyg302/supers.py/master/supers-logo.svg "Shaken, not stirred.")

---

Watch JSON objects like James Bond. This boils down to the problem of observing changes in nested dicts and lists.

## Usage

You can safely do `from supers import *`. This imports the functions `watch()` and `unwatch()`, as well as the two classes `NotifyDict` and `NotifyList`.

### `watch()` and `unwatch()`

Call `watch()` on any dict or list (even nested) -- e.g. the result of `json.loads()` on a valid JSON string -- to begin watching it. This method returns either a `NotifyDict` or `NotifyList` depending on what data structure was passed. You may also pass a listener and a triggering event; `watch(d, listener, 'delete')` is equivalent to `watch(d).on('delete', listener)`.

`unwatch()` simply reverses the process and returns a vanilla dict or list.

```python
def callback(record):
    print '{} {} --> {}'.format(record['type'], record['oldvalue'], record['value'])
    
d = {'a': 1, 'b': 2, 'c': [3, 'd', 4]}
n = watch(d, callback)
n['a'] = 'Hello!'  # prints "set 1 --> Hello!"
n['c'][0] *= 3     # prints "set 3 --> 9"
```

### Events and Listeners

Each `NotifyDict` and `NotifyList` maintains a dictionary of **listeners**, organized into lists keyed by **events**. When some change is made to the watched object, it searches for all matching events and triggers their associated listeners.

An event is a string of the form `[TYPE] [PATH]`. `[TYPE]` must be one of `change` (matches everything), `set`, `delete`, or `insert`. `[PATH]` is written in JavaScript accessor notation.

For example, `change .a[1].b` will be triggered for all changes that occur in the object at the key `b` of the 2nd element of the list at key `a` of the watched object.

For convenience, you can often omit the path entirely if you want to be notified of changes at any level of the object. For example, `delete` will be triggered whenever an item is deleted regardless of its path.

```python
def callback(record):
    print 'Tada!'
    
l = [1, {'a': 2, 'b': ['c', 'd', 'e']}, 3]
n = watch(l, callback, event='change [1].b')
n[2] += 1                    # prints nothing
n[1]['b'][1] += 'oooooood!'  # prints "Tada!"
```

### Callback Record

A listener is a function with a single argument, by convention called the `record`. The `record` is a dict with the following elements:

Attribute  | Description
---------- | -----------
`object`   | The full watched object that triggered this listener
`type`     | Type of change (set, delete, etc.)
`name`     | Key or index of changed element
`path`     | List of keys and indices to access the changed element from `object`
`value`    | New value of changed element (possibly None)
`oldvalue` | Old value of changed element (possibly None)

```python
def callback(record):
    print record
    
d = {'a': 'Hello'}
n = watch(d, callback)
n['a'] += ' world!'  # prints "{'name': 'a', 'object': {'a': 'Hello world!'}, 'value': 'Hello world!', 'oldvalue': 'Hello', 'path': ['a'], 'type': 'set'}"
```

## Credits

- [Reactive-Py](https://github.com/deepanshumehndiratta/reactive-py/blob/master/src/reactive.py)
- [observe.py from EditObj 2](https://github.com/sdemircan/editobj2/blob/master/observe.py)
- [Bunch](https://github.com/dsc/bunch)