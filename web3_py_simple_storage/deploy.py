from solcx import compile_standard, install_solc
import json

with open(
    "C:/Users/gmnya/Blockchain/demos/web3_py_simple_storage/SimpleStorage.sol", "r"
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
    },
    solc_version="0.6.0",
)

with open("compiled_code", "w") as file:
    json.dump(compiled_sol, file)
