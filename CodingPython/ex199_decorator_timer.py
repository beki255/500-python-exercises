"""Ex199 Decorator Timer
"""

import time
def timer(f):
    def w(*a,**kw):
        s=time.time(); r=f(*a,**kw); print(f"{f.__name__} took {time.time()-s:.4f}s"); return r
    return w
