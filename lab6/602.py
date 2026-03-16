def even(n):
    return n % 2 == 0
a = int(input())
b = map(int,input().split())
c = filter(even,b)
print(len(list(c)))