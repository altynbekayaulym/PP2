n = int(input())
a = list(map(int, input().split()))

for i in range(n):
    is_new = True
    for j in range(i):
        if a[i] == a[j]:
            is_new = False
            break

    if is_new:
        print("YES")
    else:
        print("NO")
