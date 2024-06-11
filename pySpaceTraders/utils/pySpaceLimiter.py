"""
:author: GH feba66
:copyright: © 2023 Felix Baumkötter"""

import time
from datetime import datetime, timedelta
from functools import wraps
from threading import Lock, Semaphore
from typing import Any


class Limiter:
    points: int
    duration: float
    sema: Semaphore
    time: datetime | None
    lock: Lock

    def __init__(self, points: int = 2, duration: float = 1) -> None:
        self.points: int = points
        self.duration: float = duration
        self.sema = Semaphore(points)
        self.time = None
        self.lock = Lock()

    def check_reset(self):
        with self.lock:
            if self.time is not None and (datetime.now() - self.time).total_seconds() > 0:
                self.sema._value = self.points
                self.time = None
                return True
        return False

    def aquire(self):
        if self.time is None:
            with self.lock:
                if self.time is None:  # weird but im thinking about an edge case here
                    self.time = datetime.now()
                    self.time += timedelta(seconds=self.duration)
        return self.sema.acquire(blocking=False)

    def time_to_reset(self):
        return (self.time - datetime.now()).total_seconds() if self.time is not None else 0

    def sleep(self):
        time.sleep(max((self.duration - self.time_to_reset()) * 0.95, 0.01))

    def __call__(self, func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.check_reset()

            while not self.aquire():
                if not self.check_reset():
                    self.sleep()

            # print(f"{datetime.utcnow()} ", end="")
            r = func(*args, **kwargs)
            return r

        return wrapper


class BurstyLimiter:
    static: Limiter
    burst: Limiter

    def __init__(self, static, burst) -> None:
        self.static = static
        self.burst = burst

    def __call__(self, func) -> Any:

        @wraps(func)
        def wrapper(*args, **kwargs):
            global start
            self.static.check_reset()
            self.burst.check_reset()

            while (not self.static.aquire()) and (not self.burst.aquire()):
                if not self.static.check_reset() and not self.burst.check_reset():
                    time.sleep(max(min(self.static.time_to_reset(), self.burst.time_to_reset()) * 0.95, 0))

            # print(f"{datetime.utcnow()} ", end="")
            r = func(*args, **kwargs)
            return r

        return wrapper
