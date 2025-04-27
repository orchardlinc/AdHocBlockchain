from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import hashlib
import names
import numpy as np
import time


class Node:
    """
    Class Node represents an user 
    """
    def __init__(self) -> None:
        """
        Initializes the variables for the class
        - timestamp to get the time
        - name: users full name
        - wallet: users wallet
        """
        self.timestamp = time.time()
        self.name = names.get_full_name()
        self.wallet = Wallet()
        self.trust_level = np.random.randint(0, 11)

    def __repr__(self) -> str:
        """
        A method to return a string of all the information of each user
        Returns:
            str: _description_
        """
        return f"Node (name = {self.name}, {self.wallet}, trust_level = {self.trust_level})"


class Wallet:
    def __init__(self) -> None:
        """
        Initializes the variables for the class
        - fingerprint: a unique identifier for the wallet
        - private_key: the private key of the wallet
        - public_key: the public key of the wallet
        - wallet_id: the id of the wallet
        - balance: the balance of the wallet
        """
        self.fingerprint = None # Placeholder for fingerprint (if used)
        
        # Generate a new Ed25519 private key
        self.private_key = ed25519.Ed25519PrivateKey.generate().private_bytes(
            encoding = serialization.Encoding.Raw,
            format = serialization.PrivateFormat.Raw,
            encryption_algorithm = serialization.NoEncryption()
        )
        # Generate the public key from the private key
        # and convert it to raw bytes
        self.public_key = ed25519.Ed25519PrivateKey.generate().public_key().public_bytes(
            encoding = serialization.Encoding.Raw,
            format = serialization.PublicFormat.Raw
        )
        
        # hashes the private key to create a unique wallet id
        # and converts it to a hexadecimal string
        self.wallet_id = hashlib.sha1(self.private_key).hexdigest()
        self.balance = 0 # Placeholder for balance

    def __repr__(self) -> str:
        """
        A method to return a string of all the information of each wallet
        Returns:
            str: the user's wallet information
        """
        return f"Wallet = (Private Key, Public Key, wallet_id = {self.wallet_id}, balance = {self.balance})"


class Network:
    """
    Class Network represents the network of users
    """
    def __init__(self, num_nodes: int = 100, area_size: int = 1000, step_size: int = 10,
                 transaction_distance: int = 5, witness_distance: int = 250,
                 transaction_probability: float = 0.01) -> None:
        """
        Initializes the variables for the class
        Args:
            num_nodes (int): number of nodes in the network
            area_size (int): size of the area (as in area of the device)
            step_size (int): size of the step (as in the distance between each node)
            transaction_distance (int): distance between the nodes to make a transaction
            witness_distance (int): distance between the nodes to witness a transaction
            transaction_probability (float): probability of making a transaction
        """
        self.num_nodes = num_nodes
        self.area_size = area_size
        self.step_size = step_size
        self.transaction_distance = transaction_distance
        self.witness_distance = witness_distance
        self.transaction_probability = transaction_probability
        self.nodes = [Node() for _ in range(self.num_nodes)]

    def __repr__(self) -> str:
        """
        A method to return a string of all the information of each user
        Returns:
            str: string representation of the network
        """
        # Create a list to store the string representation of the network and each node/user
        user_information = [
            "Network(",
            f"    num_nodes = {self.num_nodes},",
            f"    area_size = {self.area_size},",
            f"    step_size = {self.step_size},",
            f"    transaction_distance = {self.transaction_distance},",
            f"    witness_distance = {self.witness_distance},",
            f"    transaction_probability = {self.transaction_probability},",
            "Nodes:", "-"*150
        ] 
        
        for i, node in enumerate(self.nodes): # enumerate to get index and node
            user_information.append(f" {i+1}. {repr(node)}") # get the string representation of the node by use of repr
            user_information.append(f"" + "-"*150) # addline separators for readability
        user_information.append(")") # append on the closing bracket of each node in the list
        node_rewrite = "\n".join(user_information) # join the list on each new line
        return node_rewrite # return the string representation of the network


if __name__ == "__main__":
    network = Network()
    print(network)