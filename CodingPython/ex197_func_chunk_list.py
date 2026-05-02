"""Ex197 Func Chunk List
"""

def chunk(lst,sz): return [lst[i:i+sz] for i in range(0,len(lst),sz)]
print(chunk([1,2,3,4,5],2))
