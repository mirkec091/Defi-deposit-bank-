// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ML_Bank_Token is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("ML_Bank_Token", "MLBT") {
        _mint(msg.sender, initialSupply);
    }

    address[] public stakers;
}
