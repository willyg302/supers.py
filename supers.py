import json
import collections


__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['NotifyDict', 'NotifyList', 'watch', 'unwatch']


class NotifyBase(object):

	def __init__(self):
		self._listeners = []  # @TODO: Keep track of type/path filter

	def on(self, event, listener):
		if listener is not None:
			self._listeners.append(listener)
		return self

	def _notify(self, type, name):
		# @TODO: Only call listeners filtered by type/path
		for listener in self._listeners:
			listener({
				'object': self,
				'type': type,
				'name': name
			})

	def _listen(self, record):
		# @TODO: Modify to add information about "bubbling up"
		self._notify(record['type'], record['name'])

	def to_json(self, **options):
		return json.dumps(unwatch(self), **options)


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
		self._dict[key] = watch(value, self._listen)
		self._notify('__setitem__', key)  # @TODO: Full record

	def __delitem__(self, key):
		del self._dict[key]
		self._notify('__delitem__', key)  # @TODO: Full record

	def to_dict(self):
		return unwatch(self)

	@staticmethod
	def from_dict(d):
		if not isinstance(d, dict):
			raise TypeError('You must pass a dict!')
		return watch(d)


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
		self._list[index] = watch(value, self._listen)
		self._notify('__setitem__', index)  # @TODO: Full record

	def __delitem__(self, index):
		del self._list[index]
		self._notify('__delitem__', index)  # @TODO: Full record

	def to_list(self):
		return unwatch(self)

	@staticmethod
	def from_list(l):
		if not isinstance(l, list):
			raise TypeError('You must pass a list!')
		return watch(l)



def watch(x, listener=None, event='change .*'):
	if isinstance(x, (NotifyDict, NotifyList)):
		return x.on(event, listener)
	elif isinstance(x, dict):
		n = NotifyDict()
		for k, v in dict.iteritems(x):
			n[k] = watch(v, n._listen)
		return n.on(event, listener)
	elif isinstance(x, list):
		n = NotifyList()
		for v in x:
			n.append(watch(v, n._listen))
		return n.on(event, listener)
	else:
		return x


def unwatch(x):
	if isinstance(x, NotifyDict):
		x = x._dict
	elif isinstance(x, NotifyList):
		x = x._list
	if isinstance(x, dict):
		return dict((k, unwatch(v)) for k, v in dict.iteritems(x))
	elif isinstance(x, list):
		return list(unwatch(v) for v in x)
	else:
		return x


if __name__ == "__main__":
	def p(record):
		print record

	d = {'a': 1, 'b': 2, 'd': {'e': 5, 'f': 6}}
	#n = watch(d, p)
	#n['c'] = 3
	#del n['d']['e']

	n2 = NotifyDict.from_dict(d)
	n2.on('change .*', p)
	n2['x'] = {'y': 8, 'z': 9}
	n2['x']['z'] = 10
	del n2['x']