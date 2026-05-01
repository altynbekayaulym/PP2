a = int(input())
b = list(map(int,input().split()))
m = b[0]
for i in range(a):
    if b[i]>m:
        m = b[i]
print(m)