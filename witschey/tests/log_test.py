from log import


"""

#### Sym, Example

As an example of generating numbers from a distribution, consider the following code.
The logged population has plus, grapes and pears in the ration 2:1:1.
From that population, we can generate another distribution that is nearly the same:

>>> symDemo()
(0.5, 'plums'), (0.265625, 'grapes'), (0.234375, 'pears')]
{'plums': 64, 'grapes': 34, 'pears': 30}

"""

def sym_entropy_demo(n1=10, n2=1000):

    random.seed(7)
    init_fruit = ['plums'] * (n1*2) + ['grapes'] * n1 + ['pears'] * n1
    log = Sym(init_fruit)
    print(json.dumps(log.distribution(), indent=2, sort_keys=True))

    found = Sym([log.ish() for _ in xrange(n2)])
    print(json.dumps(found.distribution(), indent=2, sort_keys=True))
    print(found.counts())

    print('entropy:', found.entropy())
    for x in xrange(15):
        desired = random.randint(1, 5)
        while found._cache.count(x) < desired:
            found += x
    print(json.dumps(found.distribution(), indent=2, sort_keys=True))
    print('entropy:', found.entropy())

def report_demo(n1=10, n2=1000):
    init_fruit = ['plums'] * (n1*2) + ['grapes'] * n1 + ['pears'] * n1
    log = Sym(init_fruit)
    print(log.report().to_str())


if __name__ == "__main__":
    for c in (Sym, Num):
        print(c.__name__, c().__dict__.keys())

    report_demo()
    print()
    print('=' * 50)
    print()

    sym_entropy_demo()

