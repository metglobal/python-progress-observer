class ProgressObserver:
    """Progress observer class"""
    CALLBACKS = []

    def __init__(self):
        self.started = False
        self.finished = False
        self.parent = None
        self.children = []
        self.current_step = 0
        self.total_steps = 0
        self.message = None

    @property
    def is_parent(self):
        """if there is no child parent is observer"""
        return not self.children

    def num_of_children_steps(self):
        """returns number of total steps that belongs children"""
        total = 0
        for child in self.children:
            total += child.total_steps
        return total

    def run_callbacks(self, **kwargs):
        """runs all the callbacks in callback list"""
        for callback in self.CALLBACKS:
            getattr(self, callback)(**kwargs)

    def start(self, total_steps=None, message=None):
        """starts the processes"""
        if not total_steps:
            total_steps = self.num_of_children_steps()

        self.total_steps = total_steps
        self.started = True
        self.run_callbacks(start=True, message=message)

    def finish(self, message=None):
        """finishes the processes if all steps are done"""
        if not self.started:
            raise ValueError("Process is not started")
        check = True
        for child in self.children:
            if not child.finished:
                check = False
                break
        if check:
            self.finished = True
            self.run_callbacks(finish=True, message=message)
        else:
            raise ValueError("Child processes not finished yet")

    def set_parent(self, parent):
        """sets parent for children"""
        if self not in parent.children:
            parent.children.append(self)
            self.parent = parent

    def step(self, message=None):
        """each step calls its own callback functions"""
        self.current_step += 1
        if self.current_step <= self.total_steps:
            self.run_callbacks(message=message)
            if self.parent:
                self.parent.step(message)
        else:
            self.current_step -= 1
            raise StopIteration
