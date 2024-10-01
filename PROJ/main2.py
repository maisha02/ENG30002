import hashlib
import random
import time

# Class to represent the community battery
class CommunityBattery:
    def __init__(self, capacity=100):
        self.capacity = capacity  # Maximum storage capacity of the battery
        self.energy_stored = 0  # Initial energy stored in the battery

    def store_energy(self, amount):
        if self.energy_stored + amount <= self.capacity:
            self.energy_stored += amount
            print(f"Community Battery: Stored {amount:.2f} kWh. Total stored: {self.energy_stored:.2f} kWh")
            return True
        else:
            print(f"Community Battery: Cannot store {amount:.2f} kWh. Battery full!")
            return False

    def withdraw_energy(self, amount):
        if self.energy_stored >= amount:
            self.energy_stored -= amount
            print(f"Community Battery: Withdrew {amount:.2f} kWh. Remaining: {self.energy_stored:.2f} kWh")
            return amount
        else:
            print(f"Community Battery: Not enough energy to withdraw {amount:.2f} kWh!")
            return 0

    def get_stored_energy(self):
        return self.energy_stored

# Define the Block class to store transactions
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index  # Position of the block in the chain
        self.previous_hash = previous_hash  # Hash of the previous block
        self.timestamp = timestamp  # Timestamp of block creation
        self.transactions = transactions  # Transactions included in the block
        self.hash = self.calculate_hash()  # The block's own hash

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __str__(self):
        return (f"Block #{self.index} [Hash: {self.hash}]\n"
                f"Previous Hash: {self.previous_hash}\n"
                f"Timestamp: {time.ctime(self.timestamp)}\n"
                f"Transactions: {self.transactions}\n")

# Define the VirtualNode class to simulate energy production and consumption
class VirtualNode:
    def __init__(self, node_id, initial_energy=0):
        self.node_id = node_id  # Unique identifier for the node
        self.energy_balance = initial_energy  # Initial energy balance (NRG tokens)
        self.energy_production_rate = random.uniform(0.5, 1.5)  # Simulated energy production rate
        self.energy_consumption_rate = random.uniform(0.5, 1.5)  # Simulated energy consumption rate

    def consume_energy(self):
        # Consume energy based on the consumption rate
        consumed_energy = min(self.energy_balance, self.energy_consumption_rate * random.uniform(0.8, 1.2))
        self.energy_balance -= consumed_energy
        print(f"{self.node_id}: Consumed {consumed_energy:.2f} kWh")
        return consumed_energy

    def manage_remaining_energy(self, produced_energy, community_battery, blockchain):
        remaining_energy = self.energy_balance + produced_energy

        if remaining_energy > 0:
            print(f"{self.node_id}: Managing {remaining_energy:.2f} kWh of remaining energy")

            # First try to store in the community battery
            if community_battery.store_energy(remaining_energy):
                self.energy_balance = 0  # All remaining energy is stored
                blockchain.add_transaction(f"{self.node_id} stored {remaining_energy:.2f} kWh in the community battery")
            else:
                # If the battery is full, store the energy in the house's balance
                self.energy_balance += remaining_energy
                blockchain.add_transaction(f"{self.node_id} stored {remaining_energy:.2f} kWh in own balance")
                print(f"{self.node_id}: Stored {remaining_energy:.2f} kWh in own balance")

    def produce_energy(self, community_battery, blockchain):
        produced_energy = self.energy_production_rate * random.uniform(0.8, 1.2)
        print(f"{self.node_id}: Produced {produced_energy:.2f} kWh")
        return produced_energy

    def trade_energy(self, other_node, amount, blockchain):
        if self.energy_balance >= amount:
            self.energy_balance -= amount
            other_node.energy_balance += amount
            print(f"{self.node_id} traded {amount:.2f} NRG with {other_node.node_id}")
            blockchain.add_transaction(f"{self.node_id} traded {amount:.2f} NRG with {other_node.node_id}")
            return True  # Trade successful
        print(f"{self.node_id} failed to trade {amount:.2f} NRG with {other_node.node_id} (Insufficient balance)")
        return False  # Trade failed due to insufficient balance

    def get_balance(self):
        return self.energy_balance

# Define the Blockchain class to manage the virtual transactions
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Blockchain starts with a genesis block
        self.pending_transactions = []  # Transactions waiting to be included in a block

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        print(f"Transaction added: {transaction}")

    def mine_pending_transactions(self, community_battery):
        # Add the state of the community battery to the block
        self.add_transaction(f"Community Battery: {community_battery.get_stored_energy():.2f} kWh stored")
        
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, time.time(), self.pending_transactions)
        self.chain.append(new_block)
        print(new_block)  # Print the new block details
        self.pending_transactions = []  # Reset pending transactions after mining

    def update_balance(self, node_id, balance):
        self.add_transaction(f"Update balance: {node_id} has {balance:.2f} NRG")

# Initialize the blockchain
blockchain = Blockchain()

# Create the community battery
community_battery = CommunityBattery(capacity=100)  # Adjust capacity as needed

# Create virtual nodes (houses)
num_nodes = 5  # Number of virtual houses
nodes = [VirtualNode(node_id=f"House_{i+1}") for i in range(num_nodes)]

# Simulate energy consumption, production, and trading
def simulate_energy(nodes, blockchain, community_battery):
    for node in nodes:
        node.consume_energy()  # Consume energy first
        produced_energy = node.produce_energy(community_battery, blockchain)  # Then produce energy
        node.manage_remaining_energy(produced_energy, community_battery, blockchain)  # Manage the remaining energy
        blockchain.update_balance(node.node_id, node.get_balance())

def simulate_trading(nodes, blockchain):
    for node in nodes:
        trade_partner = random.choice(nodes)
        if node != trade_partner:
            trade_amount = random.uniform(1, 5)  # Random trade amount
            node.trade_energy(trade_partner, trade_amount, blockchain)

# Simulation loop for multiple time steps
def run_simulation(steps):
    for time_step in range(steps):  # Simulate `steps` time steps
        print(f"\n--- Time Step {time_step + 1} ---")
        simulate_energy(nodes, blockchain, community_battery)
        simulate_trading(nodes, blockchain)
        blockchain.mine_pending_transactions(community_battery)  # Include community battery state in the block

# Run the simulation 
run_simulation(3)

# Optional: Print the entire blockchain to see all blocks
print("\n--- Blockchain ---")
for block in blockchain.chain:
    print(block)
