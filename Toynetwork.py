class Stablecoin:
    def __init__(self, name, total_supply, external_assets, holdings):
        self.name, self.total_supply, self.external_assets, self.original_external_assets, self.holdings = name, total_supply, external_assets, external_assets, holdings

    def get_reserve_value(self,coins):
        total = self.external_assets
        for coin_name, amount in self.holdings.items():
            if coin_name in coins:
                other_coin = coins[coin_name]
                peg_value = other_coin.get_peg_value(coins)
                total += amount * peg_value
        return total
    
    def get_peg_value(self, coins):
        self.coins = coins
        total_reserve_value = self.get_reserve_value(coins)
        peg = total_reserve_value / self.total_supply if self.total_supply > 0 else 0
        return peg
    
    def reset(self):
        self.external_assets = self.original_external_assets

# Holdings
coin_a_holdings = {}
coin_b_holdings = {"CoinA": 300}
coin_c_holdings = {"CoinA": 100}
coin_d_holdings = {"CoinB": 150}
coin_e_holdings = {"CoinD": 200}

Coin_a = Stablecoin(
    name = "CoinA",
    total_supply=1000,
    external_assets=1000,
    holdings=coin_a_holdings
)
Coin_b = Stablecoin(
    name = "CoinB",
    total_supply=500,
    external_assets=200,
    holdings=coin_b_holdings
)
Coin_c = Stablecoin(
    name = "CoinC",
    total_supply=500,
    external_assets=400,
    holdings=coin_c_holdings
)
Coin_d = Stablecoin(
    name = "CoinD",
    total_supply=200,
    external_assets=50,
    holdings=coin_d_holdings
)
Coin_e = Stablecoin(
    name = "CoinE",
    total_supply=300,
    external_assets=100,
    holdings=coin_e_holdings
)

coins = {
    "CoinA": Coin_a,
    "CoinB": Coin_b,
    "CoinC": Coin_c,
    "CoinD": Coin_d,
    "CoinE": Coin_e
}

""""
for coin in coins.values():
    peg_value = coin.get_peg_value(coins)
    print(f"{coin.name} peg: {peg_value}")
"""

# Apply Shock to CoinA
def apply_shock(coins, target_coin, shock_percentage = 0.10):
    if target_coin in coins.keys():
            coins[target_coin].external_assets *= (1 - shock_percentage)
    for coin in coins.values():
        peg_value = coin.get_peg_value(coins)
        print(f"{coin.name} peg: ${peg_value:.3f}")

def reset_all_coins(coins):
    for coin in coins.values():
        coin.reset()

apply_shock(coins, "CoinA", 0.10)
print("\nAfter reset:")
reset_all_coins(coins)
for coin in coins.values():
    print(f"{coin.name} peg: ${coin.get_peg_value(coins):.3f}")

