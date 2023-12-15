import Bot
from test import test
from Breeder import breed_networks
def main():
    for i in range(0,100):
        test(str(i))
        breed_networks(str(i))


if __name__ == "__main__":
    main()