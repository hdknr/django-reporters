import logging
import re


class ExcludeImageFilter(logging.Filter):

    def filter(self, record):
        message = record.getMessage()
        if re.search(r"GET\s+.+\.(jpg|png|gif|jpeg)\s+HTTP", message):
            return False
        return super().filter(record)
