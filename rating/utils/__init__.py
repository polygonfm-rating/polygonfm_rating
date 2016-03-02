from datetime import datetime


class TimeElapsed:
    def __enter__(self):
        self.start_date = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def elapsed(self):
        return datetime.now() - self.start_date
