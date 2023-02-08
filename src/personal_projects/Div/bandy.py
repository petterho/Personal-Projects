import random as rnd

def bandy_gjetting():
    for i in range(18):
        chance = rnd.random()
        if chance>0.6:
            print('H')
        elif chance<0.4:
            print('B')
        else:
            print('U')
if __name__ == '__main__':
    bandy_gjetting()
