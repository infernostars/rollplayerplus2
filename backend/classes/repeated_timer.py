from typing import Callable, Any
import threading


class RepeatedTimer:
    """Utility class to repeat a function every [interval] seconds.
     Starts on creation, stoppable by stop() and startable with start()."""

    def __init__(self, interval: float, function: Callable, *args: Any, **kwargs: Any):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()  # Reschedule the timer for the next run
        self.function(*self.args, **self.kwargs)

    def start(self):
        """Start or restart the RepeatedTimer."""
        if not self.is_running:
            # Schedule the next run of the function
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Pause or stop the RepeatedTimer."""
        # Cancel the timer if it is currently running
        if self._timer:
            self._timer.cancel()
        self.is_running = False
