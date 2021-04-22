def compare_vectors(vector1, vector2):
    if len(vector1) == len(vector2):
        for i in range(len(vector1)):
            if vector1[i] != vector2[i]:
                return False
        return True
    return False


if __name__ == '__main__':
    vector1 = [1, 2, 3]
    vector2 = [1, 2, 3]
    print(compare_vectors(vector1, vector2))
