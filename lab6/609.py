n = int(input())
a = input().split()
b = input().split()
k = input()
res = dict(zip(a,b))
if k in res:
        print(res[k])
else:
    print("Not found")