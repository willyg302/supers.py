supers.py

---

Watch JSON objects like James Bond. This boils down to the problem of observing changes in nested dicts and lists.

## Usage

{
    'object'
    'type'
    'name'
    'path'
    'value'
    'oldvalue'
}

event is `[type] [path]`, where type is one of change (matches all), set, delete, or insert. And path is a regex string. `.*` matches everything.

## Credits

- [Reactive-Py](https://github.com/deepanshumehndiratta/reactive-py/blob/master/src/reactive.py)
- [observe.py from EditObj 2](https://github.com/sdemircan/editobj2/blob/master/observe.py)
- [Bunch](https://github.com/dsc/bunch)