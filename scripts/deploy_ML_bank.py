from brownie import ML_Depositary_Bank, ML_Bank_Token
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy():
    account = get_account()
    initial_supply = Web3.toWei(100, "ether")
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    ML_Depositary_Bank.deploy(ml_Bank_Token.address, {"from": account})
    return


def main():
    deploy()
