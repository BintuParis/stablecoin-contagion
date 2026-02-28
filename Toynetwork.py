import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

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
    
    max_iter = 1000
    for iteration in range(max_iter):
        old_pegs = {}
        for name, coin in coins.items():
            old_pegs[name] = coin.get_peg_value(coins)

        converged = True
        for name, coin in coins.items():
            new_peg = coin.get_peg_value(coins)
            if abs(new_peg - old_pegs[name]) > 1e-6:
                converged = False
                break

        if converged:
            print(f"Converged after {iteration+1} iterations")
            break

def reset_all_coins(coins):
    for coin in coins.values():
        coin.reset()

def get_dependency_matrix(coins):
    coin_names = list(coins.keys())
    n = len(coin_names)
    matrix = np.zeros((n, n))

    for i, holder_name in enumerate(coin_names):
        holder_coin = coins[holder_name]
        total_reserves = holder_coin.get_reserve_value(coins)
        
        for asset_name, amount in holder_coin.holdings.items():
            
                j = coin_names.index(asset_name)
                matrix[i][j] = amount / total_reserves

    return matrix, coin_names

def run_scenario(coins, scenario_name, shock_dict):
    print(scenario_name)
    for name, pct in shock_dict.items():
        coins[name].external_assets *= (1 - pct) 
    results = {}
    for name, coin in coins.items():
        results[name] = coin.get_peg_value(coins)
    reset_all_coins(coins)
    return results

s1 = run_scenario(coins, "Scenario 1: CoinA -10%", {"CoinA": 0.10})
s2 = run_scenario(coins, "Scenario 2: ETH crashes 40%", {"CoinB": 0.40, "CoinC": 0.40, "CoinE": 0.40})
s3 = run_scenario(coins, "Scenario 3: CoinB fails", {"CoinB": 1.0})

scenarios = {
    "Scenario 1": s1,
    "Scenario 2": s2,
    "Scenario 3": s3 }

def visualise_network(coins):
    G = nx.DiGraph()
    for name in coins.keys():
        G.add_node(name)
    for holder_name, coin in coins.items():
        for asset_name, amount in coin.holdings.items():
            G.add_edge(holder_name, asset_name, weight=amount)
    nx.draw(G, with_labels = True)
    plt.show()

def visualise_scenarios(scenarios_dict):
    coin_names = list(scenarios_dict["Scenario 1"].keys())
    scenario_names = list(scenarios_dict.keys())
    
    plt.figure(figsize=(10,6))
    x = np.arange(len(coin_names))
    width = 0.25
    
    for i, scenario_name in enumerate(scenario_names):
        values = [scenarios_dict[scenario_name][coin] for coin in coin_names]
        plt.bar(x + i*width, values, width, label=scenario_name)

    plt.xlabel('Coins')
    plt.ylabel('Peg Value ($)')
    plt.title('Stablecoin Peg Values Across Scenarios')
    plt.xticks(x + width, coin_names)
    plt.axhline(y=1.0, color = 'r', linestyle = '--', alpha = 0.5)
    plt.legend()
    plt.show()
 

visualise_scenarios(scenarios)

    