def not_assign(i, a=0):
    if i > 0:
        a += 1
        i -= 1
        a = not_assign(i, a)
    return a


def not_assign2(i, a):
    if i > 0:
        i -= 1
        a[i] = i
        not_assign2(i, a)
    return a


a = [0] * 10
print(not_assign2(len(a), a))


print(not_assign(10, 0))
