n = int(input())

for d in [2, 3, 5]:
    while n % d == 0:
        n //= d

if n == 1:
    print("Yes")
else:
    print("No")
