from collections import defaultdict
import time

class SimpleRateLimiter:
    def __init__(self, max_requests=5, window_seconds=3):
        self.window = window_seconds
        self.max_requests = max_requests
        self.users = defaultdict(list)

    def is_allowed(self, user_id):
        now = time.time()
        self.users[user_id] = [
            t for t in self.users[user_id] if now - t < self.window
        ]
        if len(self.users[user_id]) >= self.max_requests:
            return False
        self.users[user_id].append(now)
        return True

rate_limiter = SimpleRateLimiter()