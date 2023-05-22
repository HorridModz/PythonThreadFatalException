# PythonThreadFatalException
A context manager to make threads terminate the whole program


After learning to work with threads in python, I quickly came across a feature I personally did not like: Threads will not terminate the program if they encounter an exception. For example, this script:

```py
import time
from threading import Thread


def my_thread_routine():
  print("Thread: Started thread")
  raise Exception("Thread: I raised an exception, but that's not going to terminate the main thread.")


thread = Thread(target=my_thread_routine)
thread.start()
time.sleep(1)
print("Main thread: I still ran!")
print("Also, there is a 0 exit code!")
```

Produces this output:

```
Thread: Started thread
Exception in thread Thread-1 (my_thread_routine):
Traceback (most recent call last):
  File "C:\Users\zachy\AppData\Local\Programs\Python\Python310\lib\threading.py", line 1009, in _bootstrap_inner
    self.run()
  File "C:\Users\zachy\AppData\Local\Programs\Python\Python310\lib\threading.py", line 946, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\zachy\PycharmProjects\StreamFilter\streamfilter\streamfilter.py", line 7, in my_thread_routine
    raise Exception("Thread: I raised an exception, but that's not going to terminate the main thread.")
Exception: Thread: I raised an exception, but that's not going to terminate the main thread.
Main thread: I still ran!
Also, there is a 0 exit code!

Process finished with exit code 0

```

As you can see, exceptions in threads will only terminate their respective threads, and not the whole program. For what I'm making, this behavior is not desired. So, I created a little context manager to work around this.

Tweaking the above program to use my context manager:

```py
import time
from threading import Thread
import terminate_on_fatal_exception:


def my_thread_routine():
  with terminate_on_fatal_exception():
    print("Thread: Started thread")
    raise Exception("Thread: I raised an exception, but that's not going to terminate the main thread.")


thread = Thread(target=my_thread_routine)
thread.start()
time.sleep(1)
print("Main thread: I still ran!")
print("Also, there is a 0 exit code!")
```

Produces this output:

```
Thread: Started thread
Exception in thread Thread-1 (my_thread_routine):
Traceback (most recent call last):
  File "C:\Users\zachy\PycharmProjects\StreamFilter\setup.py", line 93, in my_thread_routine
    raise Exception("Thread: I raised an exception, which will terminate the main thread and produce an exit code of 1.")
Exception: Thread: I raised an exception, which will terminate the main thread and produce an exit code of 1.

Process finished with exit code 1
```

It can also be used as a decorator:

```py
@terminate_on_fatal_exception
def my_thread_routine():
  print("Thread: Started thread")
  raise Exception("Thread: I raised an exception, which will terminate the main thread and produce an exit code of 1.")
```

Make sure you put it inside the thread - for example, this won't work:

```py
thread = Thread(target=my_thread_routine)
with terminate_on_fatal_exception():
  thread.start()
```
