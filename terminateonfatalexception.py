import sys
import os
import traceback
import threading


class terminate_on_fatal_exception():
    """
    Context / decorator manager to terminate the whole program on a fatal exception, even in threads
    If not used in a thread, the result of your code will be no different with or without this

    Works by getting traceback with traceback.format_exc(), writing traceback to sys.stderr,
    then exiting with os._exit(1)

    Example Usage as Context Manager:
    import threading

    def my_thread_routine():
        print("Starting thread...")
        with terminate_on_fatal_exception():
            do_stuff()


    thread = threading.Thread(target=my_thread_routine)
    thread.start()


    Example Usage as Decorator:
    import threading

    @terminate_on_fatal_exception
    def my_thread_routine():
        print("Starting thread...")
        do_stuff()


    thread = threading.Thread(target=my_thread_routine)
    thread.start()
    """
    def __init__(self, func=None):
        """
        For decorator
        """
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        For decorator
        """
        try:
            return self.func(*args, **kwargs)
        except Exception:
            self._terminate_program_with_traceback()

    def __enter__(self):
        """
        For context manager
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        For context manager
        """
        if exc_type is not None:
            self._terminate_program_with_traceback()

    @staticmethod
    def _terminate_program_with_traceback():
        error_traceback = ""
        if threading.get_ident() != threading.main_thread().ident:
            error_traceback += f"Exception in thread {threading.current_thread().name}:\n"
        error_traceback += traceback.format_exc()
        print(error_traceback, file=sys.stderr)
        os._exit(1)
