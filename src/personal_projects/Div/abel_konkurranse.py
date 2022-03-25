value_ = 0
for i in range(1, 2020):
    value_ = 1 / (1/i + value_)
print(value_)

sider = 50
muligheter = []
for i in range(2, sider + 1 - 1):
    for j in range(i+1, sider + 1):
        muligheter.append((i, j))
print(muligheter)
print(len(muligheter))


