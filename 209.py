a = int(input())
b = list(map(int,input().split()))
maxval = b[0]
minval = b[0]
for i in range(1,a):
    if b[i]>maxval:
        maxval = b[i]
    elif b[i]<minval:
        minval = b[i]

for i in range(a):
    if b[i] == maxval:
        b[i] = minval

print(*b)