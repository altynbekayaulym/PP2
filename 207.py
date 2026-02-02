a = int(input())
b = list(map(int,input().split()))
maxval = b[0]
pos = 1

for i in range(1, a):
    if b[i] > max_val:
        max_val = b[i]
        pos = i + 1

print(pos)
        


