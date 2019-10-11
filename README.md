# lru_diskcache
Small utility for storing arguments of function and result on a disk.

```python
import random
from lru_diskcache import lru_diskcache

@lru_diskcache(maxsize=2)
def random_function(a, b=10):
   return random.randint(0, 100)

print(random_function(5))
print(random_function(6))
print(random_function(5))
print(random_function(7))
print(random_function(5))

32
55
32
88
71

cashe_of_random_function/
.. 8934469586086229431.pickle.gz
.. 5144395139612665063.pickle.gz
.. cache_table.json
```
