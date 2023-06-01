a = {'a': 1, 'b': 2, 'c': 3}
for v in a.values():
    print(v)
print(list(a.keys()))
print(['a', 'b', 'c'] == list(a.keys()))