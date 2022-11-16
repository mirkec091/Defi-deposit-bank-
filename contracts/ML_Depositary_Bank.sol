// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function allowance(address owner, address spender)
        external
        view
        returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ML_Depositary_Bank is Ownable {
    address public ml_Bank_Token;

    // mapping of    address => tokenID => ammount
    mapping(address => mapping(string => uint256)) public stakers_balance;
    mapping(address => mapping(string => uint256))
        public stakers_balance_intrest;
    mapping(address => mapping(string => bool)) public hasStaked;
    mapping(address => mapping(string => bool)) public isStaking;
    mapping(string => bool) public allowed_tokens;
    mapping(string => address) public tokens_addresses;

    // in constructor pass in the address for your custom bank token
    // that will be used to pay interest
    constructor(address _ml_Bank_Token) {
        ml_Bank_Token = _ml_Bank_Token;
    }

    function add_token(string memory _tokenID, address _token_address) public {
        allowed_tokens[_tokenID] = true;
        tokens_addresses[_tokenID] = _token_address;
    }

    function remove_token(string memory _tokenID) public {
        require(
            allowed_tokens[_tokenID] == true,
            " already removed or does not existing token"
        );
        allowed_tokens[_tokenID] = false;
    }

    function check_token(string memory _tokenID) public view returns (bool) {
        return allowed_tokens[_tokenID];
    }

    function getContractBalanceOfToken() public view returns (uint256) {
        return IERC20(ml_Bank_Token).balanceOf(address(this));
    }

    function getUserBalanceOfToken(string memory _token)
        public
        view
        returns (uint256, uint256)
    {
        return (
            stakers_balance[msg.sender][_token],
            stakers_balance_intrest[msg.sender][_token]
        );
    }

    function deposit_ml_Bank_Token(uint256 _amount) public onlyOwner {
        // Trasnfer _ml_Bank_Token tokens to contract for rewards
        IERC20(ml_Bank_Token).transferFrom(msg.sender, address(this), _amount);
    }

    function stake_tokens(string memory _tokenID, uint256 _amount) public {
        require(allowed_tokens[_tokenID] == true, " not supported token");
        // Trasnfer  tokens to contract for staking
        IERC20(tokens_addresses[_tokenID]).transferFrom(
            msg.sender,
            address(this),
            _amount
        );
        stakers_balance[msg.sender][_tokenID] =
            stakers_balance[msg.sender][_tokenID] +
            _amount;
        // Check if the sender is already a staker
        if (!isStaking[msg.sender][_tokenID]) {
            isStaking[msg.sender][_tokenID] = true;
            hasStaked[msg.sender][_tokenID] = true;
        }
    }

    function unstake_tokens(string memory _tokenID) public {
        // get the user balance i USDC
        uint256 balance = stakers_balance[msg.sender][_tokenID];
        uint256 balance_intrest = stakers_balance_intrest[msg.sender][_tokenID];
        // check if the balance > o
        require(balance > 0);
        // transfer busd to user's account
        IERC20(tokens_addresses[_tokenID]).transfer(msg.sender, balance);
        // reset staking balance map to 0
        stakers_balance[msg.sender][_tokenID] = 0;
        // check if the balance > o
        if (balance_intrest > 0) {
            // transfer busd to user's account
            IERC20(ml_Bank_Token).transfer(msg.sender, balance_intrest);
            // reset staking balance intrest map to 0
            stakers_balance_intrest[msg.sender][_tokenID] = 0;
        }
        // update the staking status
        isStaking[msg.sender][_tokenID] = false;
    }

    function pay_intrest(
        address _adresss,
        string memory _tokenID,
        uint256 _intrest
    ) public onlyOwner {
        stakers_balance_intrest[_adresss][_tokenID] =
            stakers_balance_intrest[_adresss][_tokenID] +
            _intrest;
    }
}
