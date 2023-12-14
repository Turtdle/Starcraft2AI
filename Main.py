import Bot
from test import test
from Breeder import breed_networks
def main():
    for i in range(4,10):
        breed_networks(str(i))
        test(str(i))

if __name__ == "__main__":
    main()