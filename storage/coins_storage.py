COINS_FILE = "coins.csv"


def load_coins():
    try:
        with open(COINS_FILE, "r") as f:

            coins = [
                line.strip().upper()
                for line in f.readlines()
                if line.strip()
            ]

            return list(dict.fromkeys(coins))

    except:

        return []


def save_coins(coins):

    with open(COINS_FILE, "w") as f:

        for coin in coins:
            f.write(f"{coin}\n")