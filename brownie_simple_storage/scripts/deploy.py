from brownie import accounts, config

def deploy_simple_storage():
    # account = accounts[0]
    # print(account)
    # account = accounts.load("morara-account")
    # print(account)
    account = accounts.add(config["wallets"]["from_key"])
    print(account)

def main():
    deploy_simple_storage()