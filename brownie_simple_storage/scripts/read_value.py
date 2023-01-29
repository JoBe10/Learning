from brownie import SimpleStorage, accounts, config


def read_contract():
    # Gets latest deployed instance of the SimpleStorage contract (that's not deployed to a development network)
    # SimpleStorage variable we import is actually just an array (a ContractContainer object to be more specific)
    # so we can just access the most recent deployment using the last index
    simple_storage = SimpleStorage[-1]
    # Brownie has the contract address and ABI saved under deployments so we can immediately interact with the
    # desired contract
    print(simple_storage.retrieve())


def main():
    read_contract()
