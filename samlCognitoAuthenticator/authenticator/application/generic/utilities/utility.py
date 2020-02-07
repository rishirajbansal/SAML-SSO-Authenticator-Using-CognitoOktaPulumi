import time


class Utility:

    current_time_in_milli = lambda: int(round(time.time() * 1000))

    @staticmethod
    def safe_trim(string):
        if string is None or string.strip() == '':
            return ''
        else:
            return string.strip()
