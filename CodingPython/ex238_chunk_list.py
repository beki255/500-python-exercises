"""Ex238 Chunk List
"""

lst=[1,2,3,4,5,6,7,8]; sz=3
ch=[lst[i:i+sz] for i in range(0,len(lst),sz)]
print(f"Chunks: {ch}")
