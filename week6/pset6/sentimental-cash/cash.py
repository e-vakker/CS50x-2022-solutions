# Import library cs50
from cs50 import get_float
# Global variables
coins = 0
cash = 0
# Type of coins for dollars
type_of_coins = [0.25, 0.10, 0.05, 0.01]


def main():
    # Ask the user for the amount of change
    while True:
        cash = get_float("Change owed: ")
        if cash > 0:
            break
    # Coin Counting Function
    coins = simulate_counting(cash)
    # Printing the number of coins
    print(int(coins))


def simulate_counting(cash):
    coins = 0
    for i in range(4):
        if round(cash, 3) >= type_of_coins[i]:
            buffer_coins = round(cash, 3) // type_of_coins[i]
            cash = round(cash, 3) - round(buffer_coins * type_of_coins[i], 3)
            coins += buffer_coins
    return coins


if __name__ == "__main__":
    main()