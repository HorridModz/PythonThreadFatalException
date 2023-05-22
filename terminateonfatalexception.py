import sys
import os
import threading
import traceback
from contextlib import contextmanager


@contextmanager
def terminate_on_fatal_exception() -> None:
    """
    Context manager to terminate the whole program on a fatal exception, even in threads
    If not used in a thread, the result of your code will be no different with or without this

    Works by getting traceback with traceback.format_exc(), writing traceback to sys.stderr,
    then exiting with os._exit(1)

    Example Usage:
    import threading

    def my_thread_routine():
        print("Starting thread...")
        with terminate_on_fatal_exception():
            do_stuff()


    thread = threading.Thread(target=my_thread_routine)
    thread.start()
    """
    try:
        yield
    except Exception:
        error_traceback = ""
        if threading.get_ident() != threading.main_thread().ident:
            error_traceback += f"Exception in thread {threading.current_thread().name}:\n"
        error_traceback += traceback.format_exc()
        sys.stderr.write(error_traceback)
        os._exit(1)
