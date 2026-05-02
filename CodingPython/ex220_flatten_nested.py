"""Ex220 Flatten Nested
"""

n=[[1,2],[3,4],[5,6]]
flat=[i for sl in n for i in sl]
print(f"Flat: {flat}")
