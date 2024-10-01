# House | surplus energy | demand energy | 
# 1 | 20 | 0
# 2 | 0 |  10
# 3 | 15 | 5
# 4 | 0 | 20 
# -1 | 0 | 0

# Transfer Cost: 
# A -> B = 0.01
# A -> C = 0.02
# A -> D = 0.03

# B -> A = 0.01
# B -> C = 0.02
# B -> D = 0.03

# C -> A = 0.02
# C -> B = 0.01
# C -> D = 0.02

# D -> A = 0.03
# D -> B = 0.02
# D -> C = 0.02

class House:
    def __init__(self, name, surplus_energy, demand_energy, transfer_cost):
        self.name = name
        self.surplus_energy = surplus_energy
        self.demand_energy = demand_energy
        self.transfer_cost = transfer_cost
        self.profit = 0
        self.total_cost = 0

    def __str__(self):
        return f"{self.name} | {self.surplus_energy} | {self.demand_energy}"

    def __repr__(self):
        return self.__str__()

    def transfer_energy(self, house):
        transfer_cost = self.transfer_cost[house.name]
        transfer_energy = min(self.surplus_energy, house.demand_energy)
        self.surplus_energy -= transfer_energy
        house.demand_energy -= transfer_energy
        self.profit += (token_price - transfer_cost) * transfer_energy
        house.total_cost += (token_price * transfer_energy)
        return transfer_energy
    
    def get_transfer_cost(self):
        return self.transfer_cost
    
    def get_transfer_cost(self, house):
        return self.transfer_cost[house.name]
    
    def get_total_cost(self):
        return self.total_cost

# Community Grid extends house

class CommunityGrid(House):
    def __init__(self, energy, selling_price, buying_price, token_price=0.12):
        super().__init__('CommunityGrid', energy, 0, {})
        self.selling_price = selling_price # cost to buy energy from grid
        self.buying_price = buying_price   # cost to sell energy to grid
        self.token_price = token_price     # cost of token

    def transfer_energy_from_grid(self, house):
        transfer_energy = min(house.demand_energy, self.surplus_energy)
        self.surplus_energy -= transfer_energy
        house.demand_energy -= transfer_energy
        house.total_cost += (self.selling_price * transfer_energy)
        return transfer_energy

    
    def transfer_energy_to_grid(self, house):
        transfer_energy = house.surplus_energy
        self.surplus_energy += transfer_energy
        house.surplus_energy -= transfer_energy
        house.profit += (self.buying_price - self.token_price) * transfer_energy
        return transfer_energy



def get_most_efficient_energy_transfer_list(houses, community_grid):
    transfer_list = []    
    transfer_from_to_amount = []

    for house in houses:
        if house.demand_energy > 0:
            transfer_energy = community_grid.transfer_energy_from_grid(house)
            if transfer_energy > 0:
                transfer_from_to_amount.append([
                    community_grid.name, house.name, transfer_energy, community_grid.selling_price * transfer_energy
                ])
    
    for house in houses:
        for other_house in houses:
            if house != other_house:
                transfer_list.append((house.get_transfer_cost(other_house), house, other_house))

    transfer_list.sort(
        key=lambda x: x[0]
    )

    for t in transfer_list:
        transfer_energy = t[1].transfer_energy(t[2])
        if transfer_energy > 0:
            transfer_from_to_amount.append([t[1].name, t[2].name, transfer_energy, t[0] * transfer_energy])

    for house in houses:
        if house.surplus_energy > 0:
            transfer_energy = community_grid.transfer_energy_to_grid(house)
            if transfer_energy > 0:
                transfer_from_to_amount.append([
                    house.name, community_grid.name, transfer_energy, community_grid.buying_price * transfer_energy
                ])

    return transfer_from_to_amount


if __name__ == '__main__':
    houses = [
        House('A', 20, 0, {'B': 0.01, 'C': 0.02, 'D': 0.03}),
        House('B', 0, 10, {'A': 0.01, 'C': 0.02, 'D': 0.03}),
        House('C', 15, 0, {'A': 0.02, 'B': 0.01, 'D': 0.02}),
        House('D', 0, 20, {'A': 0.03, 'B': 0.02, 'C': 0.02})
    ]

    token_price = 0.12

    community_grid = CommunityGrid(10, 0.10, 0.15, token_price)

    print("Initial State")
    for house in houses:
        print(house)
    print(community_grid)
    print("\n\n")


    lst = get_most_efficient_energy_transfer_list(houses, community_grid)
    print("Transfer List")
    for t in lst:
        print(f"{t[0]} -> {t[1]}: {t[2]}")
    print("\n\n")

    print("Final State")
    for house in houses:
        print(house)
    print(community_grid)
    print("\n\n")

    print("Profit")
    for house in houses:
        print(f"{house.name}: {round(house.profit, 2)}")
    print("\n\n")

    print("Total Cost")
    for house in houses:
        print(f"{house.name}: {round(house.get_total_cost(), 2)}")
    print("\n\n")

