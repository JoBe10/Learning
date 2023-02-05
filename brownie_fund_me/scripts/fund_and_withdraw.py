from brownie import FundMe, MockV3Aggregator
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    eth_price = fund_me.getPrice()
    # mock = MockV3Aggregator[-1]
    # decimals = mock.decimals()
    # print(decimals)
    # answer = mock.latestRoundData()[1]
    # print(answer)
    # mock.updateRoundData(0, 350000000000, 0, 0, {"from": account})
    # print(mock.latestRoundData()[1])
    print(entrance_fee)
    print(
        f"""The current entry fee is {entrance_fee}, which is {entrance_fee / (10 ** 18)} ETH. 
        This is because the entrance fee is hardcoded to be 50 USD and the current ETH price 
        is {eth_price / (10 ** 18)}"""
    )
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
