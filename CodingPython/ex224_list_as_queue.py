"""Ex224 List As Queue
"""

from collections import deque
q=deque(); q.append(1); q.append(2)
print(f"Dequeued: {q.popleft()}")
