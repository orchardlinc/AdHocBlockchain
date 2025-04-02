import sim

import logging  # CURRENTLY UNUSED
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import time

network = sim.Network()
initial_positions = np.random.uniform(0, network.area_size, (network.num_nodes, 2))
transactions = []
trust_threshold = 25
transaction_timestamps = {}
witness_timestamps = {}

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, network.area_size)
ax.set_ylim(0, network.area_size)
sc = ax.scatter(initial_positions[:, 0], initial_positions[:, 1])
ax.set_title("Random Movement of People in 1 Km x 1 Km Area")
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")


def update_positions(positions: np.ndarray = initial_positions) -> np.ndarray:
    global network

    angles = np.random.uniform(0, 2 * np.pi, network.num_nodes)
    steps = np.random.uniform(0, network.step_size, network.num_nodes)
    dx = steps * np.cos(angles)
    dy = steps * np.sin(angles)

    positions[:, 0] += dx
    positions[:, 1] += dy

    positions[:, 0] = np.clip(positions[:, 0], 0, network.area_size)
    positions[:, 1] = np.clip(positions[:, 1], 0, network.area_size)

    return positions


def check_transactions() -> None:
    global initial_positions, network, transactions
    transactions.clear()

    for i in range(network.num_nodes):
        for j in range(i + 1, network.num_nodes):
            dist = np.linalg.norm(initial_positions[i] - initial_positions[j])
            if (dist <= network.transaction_distance and
                    np.random.rand() < network.transaction_probability):
                available_witnesses = [x for x in range(network.num_nodes) if x != i and x != j]
                selected_witnesses = random.sample(available_witnesses, random.randint(1, 10))
                cumulative_trust = sum(network.nodes[w].trust_level for w in selected_witnesses)

                print(f"Calculated trust: {cumulative_trust}")
                if cumulative_trust >= trust_threshold:
                    transactions.append((i, j))
                    print(f"Transaction ACCEPTED Between {network.nodes[i].name} "
                          f"(Wallet: {network.nodes[i].wallet.wallet_id}) & {network.nodes[j].name} "
                          f"(Wallet: {network.nodes[j].wallet.wallet_id})")
                    witness_timestamps[(i, j)] = (selected_witnesses, time.time())
                else:
                    print(f"Transaction REJECTED Between {network.nodes[i].name} "
                          f"(Wallet: {network.nodes[i].wallet.wallet_id}) & {network.nodes[j].name} "
                          f"(Wallet: {network.nodes[j].wallet.wallet_id})")


def animate() -> None:
    global initial_positions, network, transactions, transaction_timestamps, witness_timestamps
    global ax, fig, sc

    positions = update_positions(initial_positions)
    check_transactions()
    current_time = time.time()

    colors = ["blue"] * network.num_nodes

    for (i, j) in list(transaction_timestamps.keys()):
        if current_time - transaction_timestamps[(i, j)] < 5:
            colors[i] = "red"
            colors[j] = "red"
        else:
            del transaction_timestamps[(i, j)]

    for i, j in transactions:
        if (i, j) not in transaction_timestamps:
            transaction_timestamps[(i, j)] = current_time
            available_witnesses = [x for x in range(network.num_nodes) if x != i and x != j]
            selected_witnesses = random.sample(available_witnesses, random.randint(1, 10))
            witness_timestamps[(i, j)] = (selected_witnesses, current_time)

    for (i, j), (witness_nodes, timestamp) in list(witness_timestamps.items()):
        if current_time - timestamp < 5:
            for w in witness_nodes:
                colors[w] = "lime"
        else:
            del witness_timestamps[(i, j)]

    sc.set_offsets(positions)
    sc.set_color(colors)
    fig.canvas.draw_idle()


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
