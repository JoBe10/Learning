from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    # Whenever you make a transaction (and deploying a contract is just a transaction)
    # you need to add a "from" key with the account in a dictionary
    # From EThereum documentation : "To deploy a smart contract, you merely send an Ethereum transaction
    # containing the compiled code of the smart contract without specifying any recipient."
    # Check out https://ethereum.org/en/developers/docs/smart-contracts/deploying/ for more info
    # Remember: before being able to deploy a smart contract you always need to compile it, which
    # is necessary so that you web app and the EVM can understand it
    # -> compilation turns a smart contract into bytecode whcih the EVM needs to run it
    # -> compiler also creates the Application Binary Interface (ABI) which your web app
    # needs to understand the contract and call it's functions
    # -> ABI is a JSON file that describes the smart contract and its functions, thereby
    # bridging the gap between Web2 and Web3
    simple_storage = SimpleStorage.deploy({"from": account})
    # BEcause the below is a view (call) function we don't need to add the {"from": account}
    stored_value = simple_storage.retrieve()
    print(stored_value)
    # Because this is a transaction (state change) we need the {"from": account}
    transaction = simple_storage.store(15, {"from": account})
    # Wait for 1 block
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    # 3 ways to get account
    # 1. Local chain - ganache-cli will spin up 10 accounts we can use using istanbul hardfork
    # etc. -> access using accounts[0] for example
    # 2. Add accounts to brownie - using the "brownie accounts new <name>" syntax
    # -> have done this and created "goerli-account" which is password encrypted
    # -> this apparently is the most secure method as it's not stored in Github
    #  and it is password protected (pswrd is Blslf with no number)
    # -> can be retrieved using accounts.load("<name>")
    # 3. Environment variables & brownie config - save private key as environment variable
    # -> easy and no password required everytime you run a script
    # -> prone to error so should be used only for testing private keys!!
    # -> added using the .add(config["wallets"]["from_key"]) function
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
