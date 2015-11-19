"""
mytardisclient utils
"""
def human_readable_size_string(num):
    """
    Returns human-readable string.
    """
    num = float(num)
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.0f %s" % (num, unit)
        num /= 1024.0
    return "%3.0f %s" % (num, 'TB')
