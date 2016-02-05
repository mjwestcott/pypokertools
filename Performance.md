## A Note on Performance

I was initially attracted to the alternative implementation of cards illustrated
below:

```python
class Card(namedtuple('Card', 'name')):
    __slots__ = ()
    @property
    def rank(self):
        return self.name[0]
    @property
    def suit(self):
        return self.name[1]
    @property
    def numerical_rank(self):
        try:
            return int(self.rank)
        except ValueError:
            if self.rank == 'T':
                return 10
            elif self.rank == 'J':
                return 11
            elif self.rank == 'Q':
                return 12
            elif self.rank == 'K':
                return 13
            elif self.rank == 'A':
                return 14
```

This has a clarity benefit: grouping the code which returns the properties
right there in the class definition. An example similar to the above is used in
the namedtuple documentation, some way down:
https://docs.python.org/3/library/collections.html#collections.namedtuple

However, as you would expect, there is performance cost to that approach
compared to 'pre-computing' the values as in the main implementation I used.
I was interested to find out how great the difference would be. Using the
alternative `@property` approach gave these results in IPython:

```python
test_card = CARDS[0]

%timeit test_card[0]
10000000 loops, best of 3: 63 ns per loop

%timeit test_card.name
10000000 loops, best of 3: 136 ns per loop

%timeit test_get.rank
1000000 loops, best of 3: 413 ns per loop

%timeit test_card.numerical_rank
1000000 loops, best of 3: 404 ns per loop

# An Ace, to trigger the ValueError and if/elif
test_card = CARDS[12]

%timeit test_card.numerical_rank
100000 loops, best of 3: 5.74 µs per loop
```

Whereas, using the 'pre-compute' approach in pokertools.py yields:

```python
test_card = CARDS[0]

%timeit test_card[0]
10000000 loops, best of 3: 59.7 ns per loop

%timeit test_card.name
10000000 loops, best of 3: 133 ns per loop

%timeit test_card.rank
10000000 loops, best of 3: 135 ns per loop

%timeit test_card.numerical_rank
10000000 loops, best of 3: 133 ns per loop

test_card = CARDS[12]

%timeit test_card.numerical_rank
10000000 loops, best of 3: 136 ns per loop
```
