from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# To deploy to a permanent ganache we can use the ganache app on our machine and follow the video
# from 5:36:50
# If we want to deploy to a ganache chain and want brownie to remember those deployments (by default it
# doesn't do this for development chains) we can add a network (this step will be the same for adding
# any network like avalanche or polygon as well) using the following command:
# brownie networks add [environment] [id] host=[host] [KEY=VALUE, ...] (see https://eth-brownie.readthedocs.io/en/stable/network-management.html)
# "brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=5777"
# "brownie networks add Ethereum ganache-local host=http://0.0.0.0:8545 chainid=1337" in video
# Once deployed, we will see the chainid show up in the "build>deployments" folder alongside
# goerli (5) and any other chains we deployed to from brownie


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # When working with a local ganache chain we have an issue: the price feed contracts
        # don't exist on the local chain
        # To get around this we can do two things:
        # 1. Forking - work on a forked simulated chain
        # 2. Deploy mocks - deploy a "fake" price feed contract on our ganache local development chain
        # so that we can interact with it locally
        # This is a common design practice across all software development industries
        # Mock contracts in brownie are typically placed in a "test" folder under "contracts"
        # chainlink-mix Github has a lot of mock contracts that we can use!
        # See here: https://github.com/smartcontractkit/chainlink-mix/tree/main/contracts/test
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # In order to make it easy to interact with our contracts on Etherscan for example we need to verify
        # them - can be done manually but way more efficient to do by setting a "verify" variable in the
        # config file
        # More info: when doing this manually we can't us ethe "@chainlink" imports as etherscan doesn't
        # understand that but we put the actual contract code in there - called "flattening"
        # This is automatically done when using the brownie built-in verification
        # To be able to verify the contract we need to set the "ETHERSCAN_TOKEN" environment variable
        # The .get() makes sure we don't run into index errors if we forget to add "veify"
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
