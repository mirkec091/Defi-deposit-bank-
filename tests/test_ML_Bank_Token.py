from brownie import ML_Bank_Token, accounts
from scripts.helpful_scripts import get_account


def test_deploy_ML_Bank_Token_Ganache():
    initial_supply = 300000000000000000
    account = accounts[0]
    account1 = accounts[1]
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    assert ml_Bank_Token.totalSupply() == 300000000000000000
    ml_Bank_Token.transfer(account1, 70000000000000000)
    print(ml_Bank_Token.balanceOf(account))
    print(ml_Bank_Token.balanceOf(account1))


def test_deploy_ML_Bank_Token_Goerli():
    initial_supply = 300000000000000000
    account = get_account()
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    assert ml_Bank_Token.totalSupply() == 300000000000000000
    print(ml_Bank_Token.balanceOf(account))


def test_approve_ML_Bank_Token():
    account = get_account()
    # address of token receiver
    contract_address = "0xef32e84E1baF1fc46F925a79a9021c2b79F2f8C4"
    amount = 2000000000000000
    ml_Bank_Token = ML_Bank_Token[-1]
    print("miro", ml_Bank_Token.address)
    ml_Bank_Token.approve(contract_address, amount, {"from": account})
