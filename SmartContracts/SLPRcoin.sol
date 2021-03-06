pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/IERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Pausable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/access/roles/MinterRole.sol";


contract SLPRcoin is MinterRole, ERC20Detailed, ERC20Mintable, ERC20Pausable {
    
    // Create a constructor that gets run whenever the contract is migrated. This constructor takes arguments 
    // that customize the token. These arguments get passed into the DetailedERC20contract.
    constructor(
        string memory _name, 
        string memory _symbol, 
        uint initial_supply
        )
        
        ERC20Detailed(_name, _symbol, 18)
        public
    {

    }
}
