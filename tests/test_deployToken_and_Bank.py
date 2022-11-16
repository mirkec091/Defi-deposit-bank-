from brownie import ML_Bank_Token, accounts, ML_Depositary_Bank, exceptions
from scripts.helpful_scripts import get_account
from web3 import Web3
import pytest


def test_add_check_remove_token():
    initial_supply = Web3.toWei(100, "ether")
    account = accounts[0]
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    ml_Depositary_Bank = ML_Depositary_Bank.deploy(
        ml_Bank_Token.address, {"from": account}
    )
    TEST_token_address = ml_Bank_Token.address
    # add token "TEST"
    ml_Depositary_Bank.add_token("TEST", TEST_token_address)
    # check if token is allowed for staking ( existing "TEST" and non-existing "Wrong name")
    assert ml_Depositary_Bank.check_token("TEST") == True
    assert ml_Depositary_Bank.check_token("Wrong name") == False
    # remove non-existing token "Wrong name"
    with pytest.raises(exceptions.VirtualMachineError):
        ml_Depositary_Bank.remove_token("Wrong name")
    # remove token "TEST"
    assert ml_Depositary_Bank.remove_token("TEST") != ""


def test_deploy_ML_Depostiary_Bank():
    initial_supply = Web3.toWei(100, "ether")
    account = accounts[0]
    account1 = accounts[1]
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    assert ml_Bank_Token.totalSupply() == Web3.toWei(100, "ether")

    ml_Bank_Token.transfer(account1, Web3.toWei(70, "ether"))
    assert ml_Bank_Token.balanceOf(account) == Web3.toWei(30, "ether")
    assert ml_Bank_Token.balanceOf(account1) == Web3.toWei(70, "ether")

    ml_Depositary_Bank = ML_Depositary_Bank.deploy(
        ml_Bank_Token.address, {"from": account1}
    )
    # transferig initial ml_Bank_Tokens to the bank
    initial_bank_amount = Web3.toWei(25, "ether")
    # transferFrom must be approved...token.approve(contract_address, amount, {"from": account})
    ml_Bank_Token.approve(
        ml_Depositary_Bank.address, initial_bank_amount, {"from": account1}
    )
    ml_Depositary_Bank.deposit_ml_Bank_Token(initial_bank_amount, {"from": account1})
    assert ml_Depositary_Bank.getContractBalanceOfToken({"from": account1}) == (
        Web3.toWei(25, "ether")
    )


def test_stake_pay_intrest_unstake_ML_Depostiary_Bank():
    initial_supply = Web3.toWei(100, "ether")
    account = accounts[0]  # owner of token contracts "ml_Bank_Token" and "stake_Token"
    account1 = accounts[1]  # owner of ML_Bank_Token contract
    account2 = accounts[2]  # user of ML_Bank_Token contract
    # deploy two tokens "ml_Bank_Token" and "stake_Token" and transfer tokens to account 1 and 2
    ml_Bank_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    ml_Bank_Token.transfer(account1, Web3.toWei(70, "ether"))
    stake_Token = ML_Bank_Token.deploy(initial_supply, {"from": account})
    stake_Token.transfer(account2, Web3.toWei(70, "ether"))
    ml_Depositary_Bank = ML_Depositary_Bank.deploy(
        ml_Bank_Token.address, {"from": account1}
    )
    # transfer initial ml_Bank_Tokens to the bank
    initial_bank_amount = Web3.toWei(25, "ether")
    # transferFrom must be approved...token.approve(contract_address, amount, {"from": account})
    ml_Bank_Token.approve(
        ml_Depositary_Bank.address, initial_bank_amount, {"from": account1}
    )
    ml_Depositary_Bank.deposit_ml_Bank_Token(initial_bank_amount, {"from": account1})
    assert ml_Depositary_Bank.getContractBalanceOfToken({"from": account1}) == (
        Web3.toWei(25, "ether")
    )
    # add token "TEST"
    ml_Depositary_Bank.add_token("TEST", stake_Token.address)
    stake_amount = Web3.toWei(13, "ether")
    #  before staking , transferFrom must be approved...token.approve(contract_address, amount, {"from": account})
    stake_Token.approve(ml_Depositary_Bank.address, stake_amount, {"from": account2})
    ml_Depositary_Bank.stake_tokens("TEST", stake_amount, {"from": account2})
    assert ml_Depositary_Bank.getContractBalanceOfToken() == Web3.toWei(25, "ether")
    assert ml_Depositary_Bank.getUserBalanceOfToken("TEST"), {
        "from": account2
    } == Web3.toWei(13, "ether")
    # pay intrest from owner of contract "ML_Bank_Token" to the user of contract
    intrest = Web3.toWei(2, "ether")
    ml_Depositary_Bank.pay_intrest(account2, "TEST", intrest, {"from": account1})
    assert ml_Depositary_Bank.getUserBalanceOfToken("TEST", {"from": account2}) == (
        Web3.toWei(13, "ether"),
        Web3.toWei(2, "ether"),
    )

    #   unstake  "TEST" tokens
    ml_Depositary_Bank.unstake_tokens("TEST", {"from": account2})
    assert ml_Depositary_Bank.getUserBalanceOfToken("TEST") == (
        Web3.toWei(0, "ether"),
        Web3.toWei(0, "ether"),
    )
