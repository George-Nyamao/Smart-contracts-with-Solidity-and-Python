from solcx import compile_standard, install_solc
from dotenv import load_dotenv
from web3 import Web3
import json
import os

load_dotenv()

with open(
    "/Users/Morara/Documents/Blockchain/Smart-contracts-with-Solidity-and-Python/web3_py_simple_storage/SimpleStorage.sol",
    "r",
) as file:
    simple_storage_file = file.read()

# Compile ou Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    }
)

with open("compiled_code", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4e54e2ca094b498cad822746857210dc"))
gasPrice = w3.eth.gas_price
chain_id = 4
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# We need to:
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# Build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": gasPrice, "chainId": chain_id, "from": my_address, "nonce": nonce}
)
# Sign transaction using our private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send this signed transaction
print("Deploying contract ...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")
# When working with a contract, you always need:
# Copntract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the Call and getting a return vale
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating contract..")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"gasPrice": gasPrice, "chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction,private_key=private_key)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("Updated!")
print(simple_storage.functions.retrieve().call())