"""
Storage module for managing coins watchlist persistence.
"""
from typing import List


COINS_FILE = "coins.csv"


def load_coins() -> List[str]:
    """
    Load coins from storage file.
    
    Returns:
        List of unique coin tickers in uppercase
    """
    try:
        with open(COINS_FILE, "r") as f:
            coins = [
                line.strip().upper()
                for line in f.readlines()
                if line.strip()
            ]
            # Remove duplicates while preserving order
            return list(dict.fromkeys(coins))
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading coins: {e}")
        return []


def save_coins(coins: List[str]) -> bool:
    """
    Save coins to storage file.
    
    Args:
        coins: List of coin tickers to save
        
    Returns:
        True if save successful, False otherwise
    """
    try:
        with open(COINS_FILE, "w") as f:
            for coin in coins:
                f.write(f"{coin.upper()}\n")
        return True
    except Exception as e:
        print(f"Error saving coins: {e}")
        return False


def add_coin(coin: str) -> bool:
    """
    Add a single coin to watchlist (if not already present).
    
    Args:
        coin: Coin ticker to add
        
    Returns:
        True if added, False if already exists or error
    """
    coins = load_coins()
    coin_upper = coin.upper()
    
    if coin_upper in coins:
        return False
    
    coins.append(coin_upper)
    return save_coins(coins)


def remove_coin(coin: str) -> bool:
    """
    Remove a coin from watchlist.
    
    Args:
        coin: Coin ticker to remove
        
    Returns:
        True if removed, False if not found or error
    """
    coins = load_coins()
    coin_upper = coin.upper()
    
    if coin_upper not in coins:
        return False
    
    coins.remove(coin_upper)
    return save_coins(coins)
