import threading


class TaskInProcessException(BaseException):
    pass


class TaskThread(threading.Thread):

    """
    A thread object that repeats a task.

    :param task
        A ``function``. This param is the task to execute when
         run_task is called.
    """
    daemon = True
    '''
    Threads marked as daemon will be terminated.
    '''
    def __init__(self, task):
        self.task = task
        self.start_task_event = threading.Event()
        self.running = True
        self.running_lock = threading.Lock()
        self.in_task = False
        self.args

    def run(self):
        """
        called by threading.Thread, this runs in the new thread.
        """
        while self.start_task_event.wait():
            if not self.running:
                return
            with self.running_lock:
                self.start_task_event.clear()
            self.task(*self.args, **self.kwargs)
            with self.running_lock:
                self.in_task = False

    def run_task(self, *args, **kwargs):
        """
        run an instance of the task.

        :param *args
            The arguments to pass to the task.

        :param **kwargs
            The keyword arguments to pass to the task.
        """
        # Don't allow this call if the thread is currently
        # in a task.
        with self.running_lock:
            if self.in_task:
                raise TaskInProcessException()
            self.in_task = True

        self.args = args
        self.kwargs = kwargs
        # Wake up the thread to do it's thing
        self.start_task_event.set()

    def join(self):
        """
        Wait for the task to finish
        """
        self.running = False
        self.start_task_event.set()
        super(TaskThread, self).join()
