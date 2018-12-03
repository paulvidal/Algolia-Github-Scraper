class QuotaLimitException(Exception):
    """
    An exception warning Github request quota limit has been exceeded
    """
    pass


class RateLimitException(Exception):
    """
    An exception warning Github request rate limit has been exceeded, triggering anti-abuse protection
    """
    pass