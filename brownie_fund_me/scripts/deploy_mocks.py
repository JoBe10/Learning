from brownie import (
    MockV3Aggregator,
    network,
)
from scripts.helpful_scripts import (
    get_account,
)

# Specify values for the MockV3Aggregator constructor
# Decimals is how many decimals the contract should have
DECIMALS = 8
# Initial answer is the starting value
# This is 2,000
INITIAL_VALUE = 200000000000


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE, {"from": account})
    print("Mocks Deployed!")


def main():
    deploy_mocks()
