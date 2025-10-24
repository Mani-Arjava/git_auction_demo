import datetime
from time import timezone

import pendulum

# convert epoch format
date_str = "2025-08-19"
dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
epoch = int(dt.timestamp())
print(epoch)

# epoch to normal format
dt = datetime.datetime.fromtimestamp(1766188800)
print(dt.strftime("%Y-%m-%d"))


def get_epoch_range(last_cycle_end=None):
    now = datetime.now(timezone.utc)

    if last_cycle_end is None:
        # First time → use today 00:00 → today 23:59
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        # Next cycles → continue from last end → today 23:59
        start = last_cycle_end
        end = now.replace(hour=23, minute=59, second=59, microsecond=0)

    return int(start.timestamp()), int(end.timestamp())


# Using pendulum
def get_epoch_range(last_cycle_end=None):
    today = pendulum.today("UTC")

    if last_cycle_end is None:
        start = today.start_of("day")  # 00:00
        end = today.end_of("day")  # 23:59:59
    else:
        start = pendulum.instance(last_cycle_end)
        end = today.end_of("day")

    return start.int_timestamp, end.int_timestamp
