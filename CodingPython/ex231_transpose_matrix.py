"""Ex231 Transpose Matrix
"""

m=[[1,2,3],[4,5,6]]
t=[[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
print(f"Transpose: {t}")
