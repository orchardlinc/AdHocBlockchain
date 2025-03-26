# Hi Owen,
# Attached is the base code for the simulation of the Ad Hoc project.
# Currently, it simulates 100 subjects moving within a 1000x1000 area, with a 1% chance of a transaction occurring when
# two individuals are within 1 meter of each other.
# We need to implement the discussed methodology into this code.
# Additionally, it should be structured for scalability—for example, by pre-calculating values,
# saving them to a file, and loading them when the program runs.
# Let me know if you have any questions.
# Best,

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import names
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import time

# Simulation parameters
num_people = 100
area_size = 1000  # 1 km x 1 km represented in meters
step_size = 10  # Maximum step size in meters
transaction_distance = 5  # Adjusted to 5 meters to increase transaction probability
transaction_probability = 0.01  # Increased probability to make transactions more frequent

# Initialize random positions for people
positions = np.random.uniform(0, area_size, (num_people, 2))
transactions = []  # Stores active transaction locations
transaction_circles = []

# Generate random names for each person
people_names = [names.get_full_name() for _ in range(num_people)]

# Generate lightweight public-private key pairs and precompute wallet IDs
def generate_keys():
    keys = []
    wallet_ids = []
    for _ in range(num_people):
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Precompute wallet ID using a lightweight hash function (SHA1 for efficiency)
        wallet_id = hashlib.sha1(private_bytes).hexdigest()
        wallet_ids.append(wallet_id)
        
        keys.append((private_bytes, public_bytes))
    return keys, wallet_ids

ecc_keys, wallet_ids = generate_keys()

# Setup animation
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)
sc = ax.scatter(positions[:, 0], positions[:, 1])
ax.set_title("Random Movement of People in 1 Km x 1 Km Area")
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")

# Function to update positions
def update_positions(positions):
    angles = np.random.uniform(0, 2 * np.pi, num_people)
    steps = np.random.uniform(0, step_size, num_people)
    dx = steps * np.cos(angles)
    dy = steps * np.sin(angles)
    
    # Update positions
    positions[:, 0] += dx
    positions[:, 1] += dy

    # Keep positions within boundaries
    positions[:, 0] = np.clip(positions[:, 0], 0, area_size)
    positions[:, 1] = np.clip(positions[:, 1], 0, area_size)
    
    return positions

# Function to check for transactions
def check_transactions():
    global transactions
    transactions.clear()
    for i in range(num_people):
        for j in range(i + 1, num_people):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist <= transaction_distance and np.random.rand() < transaction_probability:
                transactions.append((i, j))
                print(f"Transaction happened between {people_names[i]} (Wallet: {wallet_ids[i]}) and {people_names[j]} (Wallet: {wallet_ids[j]})")

# Animation update function
def animate(i):
    global positions, transactions, transaction_circles
    positions = update_positions(positions)
    check_transactions()
    
    colors = ['blue'] * num_people  # Default color for all
    for i, j in transactions:
        colors[i] = 'red'
        colors[j] = 'red'
    
    sc.set_offsets(positions)
    sc.set_color(colors)
    fig.canvas.draw_idle()
    
    # Restore original color after 5 seconds
    def reset_colors():
        time.sleep(5)
        sc.set_color(['blue'] * num_people)
        fig.canvas.draw_idle()
    
    if transactions:
        fig.canvas.flush_events()
        fig.canvas.mpl_connect("draw_event", lambda event: reset_colors())

# Run animation continuously
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()