a = int(input())
b = map(int,input().split())
c = map(int,input().split())
s = 0
for x,y in zip(b,c):
    s += x*y
print(s)
