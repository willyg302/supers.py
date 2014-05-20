'''
supers.py: Watch JSON objects like James Bond.

This boils down to the problem of observing changes in nested dicts and lists.





If the object is a dict, we notify of the changed key/value pair
If it's a list, notify of the changed index.

We have to bubble up


References:
 - https://github.com/deepanshumehndiratta/reactive-py/blob/master/src/reactive.py
 - https://github.com/sdemircan/editobj2/blob/master/observe.py
 - https://github.com/dsc/bunch
'''

import json
import collections


__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['NotifyDict', 'NotifyList']


class NotifyBase(object):

	def __init__(self):
		self._listeners = []

	def add_listener(self, listener):
		self._listeners.append(listener)

	def _notify(self):
		for listener in self._listeners:
			listener()


class NotifyDict(collections.MutableMapping, NotifyBase):

	def __init__(self, *args, **kwargs):
		super(NotifyDict, self).__init__()
		self._dict = dict()

	def __repr__(self):
		return repr(self._dict)

	def __len__(self):
		return len(self._dict)

	def __iter__(self):
		return iter(self._dict)

	def __getitem__(self, key):
		return self._dict[key]

	def __setitem__(self, key, value):
		self._dict[key] = value
		self._notify()

	def __delitem__(self, key):
		del self._dict[key]
		self._notify()

	def to_dict():
		# @TODO: This is not recursive (_dict may contain Notify objects)
		return self._dict

	def to_json(self, **options):
		# @TODO: This is not recursive (_dict may contain Notify objects)
		return json.dumps(self._dict, **options)


class NotifyList(collections.MutableSequence, NotifyBase):

	def __init__(self):
		super(NotifyList, self).__init__()
		self._list = list()

	def __repr__(self):
		return repr(self._list)

	def __len__(self):
		return len(self._list)

	def __getitem__(self, index):
		return self._list[index]

	def __setitem__(self, index, value):
		self._list[index] = value

	def __delitem__(self, index):
		del self._list[index]

	def to_list():
		# @TODO: This is not recursive (_list may contain Notify objects)
		return self._list

	def to_json(self, **options):
		# @TODO: This is not recursive (_list may contain Notify objects)
		return json.dumps(self._list, **options)


"""

	def to_dict(self):
		'''For a Fiber f, `f.to_dict()` is an alias for `unfiberify(f)`.'''
		return unfiberify(self)

	@staticmethod
	def from_dict(d):
		'''For a dictionary d, `Fiber.from_dict(d)` is an alias for `fiberify(d)`.'''
		return fiberify(d)

	def toJSON(self, **options):
		'''Serializes this Fiber to JSON. Accepts the same keyword options as `json.dumps()`.'''
		return json.dumps(self, **options)


def fiberify(x):
	'''Recursively converts a dictionary into a Fiber.'''
	if isinstance(x, dict):
		return Fiber((k, fiberify(v)) for k, v in dict.iteritems(x))
	elif isinstance(x, list):
		return list(fiberify(v) for v in x)
	else:
		return x

def unfiberify(x):
	'''Recursively converts a Fiber into a dctionary.'''
	if isinstance(x, dict):
		return dict((k, unfiberify(v)) for k, v in dict.iteritems(x))
	elif isinstance(x, list):
		return list(unfiberify(v) for v in x)
	else:
		return x

"""

if __name__ == "__main__":
	n = NotifyDict()

	def p():
		print 'Hello'
	def w():
		print 'World!'

	n.add_listener(p)
	n.add_listener(w)
	n[2] = 3
	del n[2]
	print n