from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # We tell pur test that this is the exception we want to occur
    # If we ran the withdraw function without any "with..." statement that is the
    # exception we would get
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})


# Mainnet forking is really powerful because we can simulate testing on the mainnet locally
# This essentially creates a copy of the blockchain and everything on it and we can then do
# simulations in it locally
# Mainnet fork is a built in feature of brownie and works with Infura the same way it does with Rinkeby for example
# To fork from Infura we can just add a network to brownie using the following command:
# <brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie port=8545>
# But performance wise Infura will not be ideal so Patrick actually prefers forking from Alchemy
# by using the http address associated with a project on Alchemy rather than the infura host above
