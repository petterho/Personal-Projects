import numpy as np

def from_bin_to_int(bin_):
    return from_n_to_m(bin_, 2, 10)


def from_int_to_bin(int_):
    return from_n_to_m(int_, 10, 2)


def from_n_to_m(number_n, n, m):
    number_m = 0
    i = 0
    while number_n != 0:
        mod_ = number_n % m
        number_m += mod_ * n**i
        print(f'mod_ = {mod_} and n**i = {n**i}')
        i += 1
        number_n = number_n // m
    return number_m


def hammond_code(org_mes):
    message = np.zeros(16, int)
    i = 0
    for j in range(16):
        if j not in [0, 1, 2, 4, 8]:
            message[j] = org_mes[i]
            i += 1
    print(f'Hammond message: \n{message} \n original message: {org_mes}')



if __name__ == '__main__':
    # Bitarray might improve this, but is not used to start with
    my_message = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], int)
    hammond_code(my_message)
