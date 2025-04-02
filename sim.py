from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import hashlib
import names
import numpy as np


class Node:
    def __init__(self) -> None:
        self.name = names.get_full_name()
        self.wallet = Wallet()
        self.trust_level = np.random.randint(0, 11)

    def __repr__(self) -> str:
        return f"Node(name={self.name}, Wallet(), trust_level={self.trust_level})"


class Wallet:
    def __init__(self) -> None:
        self.private_key = ed25519.Ed25519PrivateKey.generate().private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        self.public_key = ed25519.Ed25519PrivateKey.generate().public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        self.wallet_id = hashlib.sha1(self.private_key).hexdigest()
        self.balance = 0

    def __repr__(self) -> str:
        return f"Wallet(Private Key, Public Key, wallet_id={self.wallet_id}, Balance)"


class Network:
    def __init__(self, num_nodes: int = 100, area_size: int = 1000, step_size: int = 10,
                 transaction_distance: int = 5, transaction_probability: float = 0.01) -> None:
        self.num_nodes = num_nodes
        self.area_size = area_size
        self.step_size = step_size
        self.transaction_distance = transaction_distance
        self.transaction_probability = transaction_probability
        self.nodes = [Node() for _ in range(self.num_nodes)]

    def __repr__(self) -> str:
        return (f"Network(num_nodes={self.num_nodes}, area_size={self.area_size}, "
                f"step_size={self.step_size}, transaction_distance={self.transaction_distance}, "
                f"transaction_probability={self.transaction_probability}, [Node(), ...])")


if __name__ == "__main__":
    node = Node()
    wallet = Wallet()
    network = Network()
    print(node)
    print(wallet)
    print(network)
    print(network.nodes)
