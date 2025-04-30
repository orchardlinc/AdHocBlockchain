import networkComponents

# import logging  # CURRENTLY UNUSED
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time

# Moved everyting to a class to get rid of the global variables
# and to make it easier to read and understand - O
class Simulation:
    def __init__(self, network: networkComponents.Network) -> None:
        """
        Initializes the simulation with the given network.

        Args:
            network (Network): The network to be simulated.
        """
        # Set up the network adn initial variables
        self.network = network
        self.initial_positions = np.random.uniform(0, network.area_size, (network.num_nodes, 2))
        self.transactions = []
        self.trust_threshold = 25
        self.transaction_timestamps = {}
        self.witness_timestamps = {}
        
        # setup for matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim(0, network.area_size)
        self.ax.set_ylim(0, network.area_size)
        self.ax.set_title("Random Movement of Individuals in 1 Km x 1 Km Area")
        self.ax.set_xlabel("X Position (m)")
        self.ax.set_ylabel("Y Position (m)")
        self.sc = self.ax.scatter(self.initial_positions[:, 0], self.initial_positions[:, 1])
            
    def update_positions(self) -> np.ndarray:
        """
        Update the positions of the nodes in the network based on their movement.

        """
        angles = np.random.uniform(0, 2 * np.pi, self.network.num_nodes) # random angles for each node
        steps = np.random.uniform(0, self.network.step_size, self.network.num_nodes) # random steps for each node
        dx = steps * np.cos(angles) # x movement for each node
        dy = steps * np.sin(angles) # y movement for each node

        self.initial_positions[:, 0] += dx # x position update
        self.initial_positions[:, 1] += dy # y position update

        # Ensure nodes stay within the area boundaries
        self.initial_positions[:, 0] = np.clip(self.initial_positions[:, 0], 0, self.network.area_size)
        self.initial_positions[:, 1] = np.clip(self.initial_positions[:, 1], 0, self.network.area_size)

    # Note: Need to find a better way to reduce the time complexity of this function
    #       Currently O(n^2) - O
    def check_transactions(self) -> None:
        """
        Check for transactions between nodes based on their positions and trust levels.
        """
        self.transactions.clear()

        # Check for transactions between all pairs of nodes
        for i in range(self.network.num_nodes):
            for j in range(i + 1, self.network.num_nodes):
                dist = np.linalg.norm(self.initial_positions[i] - self.initial_positions[j]) # distance between the two nodes
                # Check if the distance is within the transaction distance and if a transaction should occur
                if (dist <= self.network.transaction_distance and
                        np.random.rand() < self.network.transaction_probability):
                    selected_witnesses = self.select_witnesses(i, j)
                    cumulative_trust = sum(self.network.nodes[w].trust_level for w in selected_witnesses)

                    print(f"Calculated trust: {cumulative_trust}")
                    # Check if the cumulative trust is above the threshold
                    if cumulative_trust >= self.trust_threshold:
                        self.transactions.append((i, j))
                        print(f"Transaction ACCEPTED Between {self.network.nodes[i].name} "
                              f"(Wallet: {self.network.nodes[i].wallet.wallet_id}) & {self.network.nodes[j].name} "
                              f"(Wallet: {self.network.nodes[j].wallet.wallet_id})")
                        self.witness_timestamps[(i, j)] = (selected_witnesses, time.time())
                    else:
                        print(f"Transaction REJECTED Between {self.network.nodes[i].name} "
                              f"(Wallet: {self.network.nodes[i].wallet.wallet_id}) & {self.network.nodes[j].name} "
                              f"(Wallet: {self.network.nodes[j].wallet.wallet_id})")
    
    
    def select_witnesses(self, node_one: int, node_two: int) -> list:
        """
        Select witnesses for a transaction between two nodes.
        Args:
            node_one (int): Index of the first node.
            node_two (int): Index of the second node.

        Returns:
            list: List of selected witness nodes.
        """
        selected_witnesses = [] # List to store the selected witness nodes
        # Check all nodes in the network to see if they are within the witness distance of both nodes
        for k in range(self.network.num_nodes):
            if k != node_one and k != node_two:
                dist_one = np.linalg.norm(self.initial_positions[node_one] - self.initial_positions[k]) # distance between node_one and k
                dist_two = np.linalg.norm(self.initial_positions[node_two] - self.initial_positions[k])

                if (dist_one <= self.network.witness_distance and
                        dist_two <= self.network.witness_distance):
                    selected_witnesses.append(k)

        return selected_witnesses
    
    def animate(self, frame) -> None:
        """
        Update the animation frame.
        Args:
            frame : The current frame number.
        """
        self.update_positions()
        self.check_transactions()
        current_time = time.time()
        
        colors = ["blue"] * self.network.num_nodes

        # Check for recent transactions and update their colors
        for (i, j) in list(self.transaction_timestamps.keys()):
            if current_time - self.transaction_timestamps[(i, j)] < 5:
                colors[i] = "red"
                colors[j] = "red"
            else:
                del self.transaction_timestamps[(i, j)]

        # Check for new transactions and update their timestamps
        for i, j in self.transactions:
            if (i, j) not in self.transaction_timestamps:
                self.transaction_timestamps[(i, j)] = current_time
                selected_witnesses = self.select_witnesses(i, j)
                self.witness_timestamps[(i, j)] = (selected_witnesses, current_time)

        # Check for witness nodes and update their colors
        for (i, j), (witness_nodes, timestamp) in list(self.witness_timestamps.items()):
            if current_time - timestamp < 5:
                for w in witness_nodes:
                    colors[w] = "lime"
            else:
                del self.witness_timestamps[(i, j)]

        self.sc.set_offsets(self.initial_positions)
        self.sc.set_facecolor(colors)
        self.fig.canvas.draw_idle()


# Initialize the network and simulation

if __name__ == "__main__":
    sim = Simulation(networkComponents.Network())
    ani = animation.FuncAnimation(sim.fig, sim.animate, interval=50)
    plt.show()


