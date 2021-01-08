// SPDX-License-Identifier: MIT
pragma solidity >= 0.5.0;

import "./Ownable.sol";

contract Greeter is Ownable {
  string private _greeting = "Hello, World!";

  function greet() external view returns(string memory) {
    return _greeting;
  }

  function setGreeting(string calldata greeting) external onlyOwner {
    _greeting = greeting;
  }
}
