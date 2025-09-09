import time

def format_duration(seconds):
    """
    Convert seconds into a human-readable MM:SS format.

    Args:
        seconds (float): Duration in seconds.

    Returns:
        str: Formatted time string.
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def get_current_time():
    """
    Returns current system time in HH:MM:SS format.
    """
    return time.strftime("%H:%M:%S", time.localtime())


def get_elapsed(start_time):
    """
    Calculate time elapsed since a given start timestamp.

    Args:
        start_time (float): A time.time() value.

    Returns:
        float: Seconds elapsed.
    """
    return time.time() - start_time
