def cycle_generator(lst, n):
    for i in range(n):
        yield from lst

lst = input().split()
n = int(input())
print(' '.join(cycle_generator(lst, n)))