# Ad Hoc Simulation for Peer-to-Peer Transaction Protocols

## Objective
This project simulates a network of mobile devices to model peer-to-peer transactions using ad hoc networking. The simulation mimics the behavior of 100 subjects moving in a 1000x1000 area. The goal is to implement the methodology discussed in our paper on decentralized mobile payment systems using Bluetooth and offline transaction validation.

## About
This paper, Transactions in the Wild: A Secure, Offline Architecture for Ad-Hoc Mobile Payments, is co-authored by Dr. Sima Jafarikhah, Dr. Hosam Alamleh, Laura Estremera, Owen Richard, Nathaneal Roberts, and Ben Eskra. The paper explores the complexities and challenges of decentralized mobile payment systems, focusing on offline transactions in ad hoc networks. Our research examines peer-to-peer transaction protocols, cryptographic techniques like SPUFs and ECC, and the feasibility of these systems in real-world applications. This simulation, part of our ongoing work, aims to model the behavior of mobile devices in a dynamic environment and test the scalability and security of decentralized payment systems.

## Abstract
This paper presents a secure offline mobile payment system without internet connectivity, centralized servers, or third-party authorities. The system leverages synthetic physically unclonable functions for device authentication, Elliptic Curve Cryptography for secure transactions, and a witness-based validation mechanism to enable peer-to-peer payments via Bluetooth in ad-hoc environments. The design enhances security and user privacy by eliminating the need to store private keys. The proposed solution is well-suited for use in remote regions, disaster-stricken areas, and temporary events where conventional payment infrastructure is unavailable. We detail the system’s core, including key generation, transaction validation, and the decentralized witness mechanism offering a practical and infrastructure-independent approach to secure offline payments.

## Code Overview
This Python-based simulation runs on Kali Linux and models the interaction of mobile devices within a specified area. It simulates the following:

- 100 mobile devices moving within a 1000x1000 meter area.
- A 1% chance of a transaction occurring when two individuals come within 1 meter of each other.
- Pre-calculation of transaction data, which can be saved and reloaded to optimize simulation runtime.

### Key Features
- **Device Movement:** Mobile devices move randomly within the defined area, with speed and movement patterns adjustable.
- **Transaction Simulation:** Each time two devices come within 1 meter, there is a chance (1%) that a transaction occurs.
- **Transaction Validation:** The simulation includes placeholder functions for transaction validation based on cryptographic protocols like SPUFs and ECC.
- **Scalability:** The simulation can handle larger numbers of subjects and area sizes by saving and loading pre-calculated values for efficiency.

## Running the Simulation
1. Clone this repository:
   ```bash
   git clone https://github.com/orchardlinc/AdHocBlockchain.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulation:
   ```bash
   python networkSimulation.py
   ```

4. Customize the simulation parameters by modifying the configuration files as needed.

## TODO
- **Methodology Implementation:** Incorporate the discussed cryptographic techniques (SPUFs, ECC) for transaction validation.
- **Optimization for Scalability:** Implement methods to pre-calculate and store transaction data, allowing for faster simulations with larger scales.
- **Advanced Transaction Validation:** Introduce peer-to-peer validation protocols, leveraging decentralized systems for secure transaction verification.

## Conclusion
This simulation aims to provide an efficient model for testing mobile payment systems, focusing on offline transactions in decentralized ad hoc networks. It will serve as a foundation for further work on enhancing security protocols in mobile financial transactions.
