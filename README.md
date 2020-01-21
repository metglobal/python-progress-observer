# python-progress-observer
This library will be used for observing actions of the classes.

**Quick Start**

install the package

    pip install git+https://github.com/metglobal/python-progress-observer.git
    
**HOW TO USE IT(BASIC EXAMPLE)**

``` python
class MyProgressObserver(ProgressObserver):
    CALLBACKS = ["my_callback"]
    def my_callback(self, **kwargs):
        print(f"{kwargs['message']}: [{self.current_step}/{self.total_steps}]")

```

`>>> observer = MyProgressObserver()`

`>>> observer.start(total_steps=3, message="I'll start doing something")`

_I'll start doing something: [0/3]_

`>>> observer.step('First action happening')`

_First action happening: [1/3]_

`>>> observer.step(message="Doing something")`

_Doing something [2/3]_

`>>> observer.step(message="Doing something weird")`

Doing something weird [3/3]

`>>> observer.step()`

_Raised StopIteration_ ->> Reached the maximum number of steps


`>>> observer.finish("I have finished doing something")`

_I have finished doing something: [3/3]_

-----------------

**HOW TO USE IT(PARENT CHILD EXAMPLE)**
``` python
class ParentProgressObserver(ProgressObserver):
    CALLBACKS = ["parent_callback"]

    def parent_callback(self, **kwargs):
        print(f"Parent: {kwargs['message']}: [{self.current_step}/{self.total_steps}]")


class ChildProgressObserver(ProgressObserver):
    CALLBACKS = ["child_callback"]

    def child_callback(self, **kwargs):
        print(f"Child: {kwargs['message']}: [{self.current_step}/{self.total_steps}]")

```
``` python
>>> parent = ParentProgressObserver()
>>> child1 = ChildProgressObserver()
>>> child2 = ChildProgressObserver()
```
``` python
>>> child1.start(total_steps=2)
"Child: None: [0/2]"

>>> child2.start(total_steps=3)
"Child: None: [0/3]"

>>> parent.start("I'm starting with two sub processes")
"Parent: I'm starting with two sub processes: [0/5]"

>>> child1.step('first step of child1')
"Child: first step of child1: [1/2]"
"Parent: first step of child1: [1/5]"

>>> child1.step('second step of child1')
"Child: second step of child1: [2/2]"
"Parent: second step of child1: [2/5]"

>>> child2.step('first step of child2')
"Child: first step of child2: [1/3]"
"Parent: first step of child2: [3/5]"

>>> child2.step('second step of child2')
"Child: second step of child2: [2/3]"
"Parent: second step of child2: [4/5]"

>>> child2.step('third step of child2')
"Child: third step of child2: [3/3]"
"Parent: third step of child2: [5/5]"

>>> parent.finish('parent finished')
Error: "child processes not finished yet"

>>> child1.finish('child1 finished')
"Child: child1 finished: [2/2]"

>>> child2.finish('child2 finished')
"Child: child2 finished: [3/3]"

>>> parent.finish('parent finished')
"Parent: parent finished: [5/5]"
```