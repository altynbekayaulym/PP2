a = int(input())
b = list(map(int,input().split()))
summa = 0
for i in range(a):
    if b[i]>0:
        summa += 1
print(summa)