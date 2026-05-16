"""
vulnerabilities.py
15 hand-labelled Solidity vulnerability test cases.
"""

VULNERABILITIES = [
    {
        "id": "v001", "title": "Reentrancy Attack", "category": "Reentrancy",
        "severity": "critical", "swc_id": "SWC-107", "cwe_id": "CWE-841",
        "real_exploit": "DAO Hack 2016 — $60M",
        "description": "External call is made before state update, enabling recursive draining.",
        "solidity_snippet": """function withdraw(uint amount) external {
    require(balances[msg.sender] >= amount);
    (bool ok,) = msg.sender.call{value: amount}(""); // ← state not updated yet
    require(ok);
    balances[msg.sender] -= amount; // ← too late
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v002", "title": "Integer Overflow", "category": "Arithmetic",
        "severity": "critical", "swc_id": "SWC-101", "cwe_id": "CWE-190",
        "real_exploit": "BEC Token 2018 — $900M",
        "description": "Unchecked arithmetic causes wrap-around on Solidity <0.8.0.",
        "solidity_snippet": """function transfer(address to, uint256 value) public {
    require(balances[msg.sender] >= value);
    balances[msg.sender] -= value;
    balances[to] += value; // overflow if to == msg.sender
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v003", "title": "Unprotected Selfdestruct", "category": "Access Control",
        "severity": "critical", "swc_id": "SWC-106", "cwe_id": "CWE-284",
        "real_exploit": "Parity Wallet 2017 — $30M",
        "description": "selfdestruct callable by any address, allowing permanent destruction.",
        "solidity_snippet": """function kill() public {
    selfdestruct(payable(msg.sender)); // no access check
}""",
        "detected_by": ["gpt-4", "claude", "gemini"],
    },
    {
        "id": "v004", "title": "Timestamp Dependence", "category": "Randomness",
        "severity": "high", "swc_id": "SWC-116", "cwe_id": "CWE-330",
        "real_exploit": "GovernMental Ponzi — randomness manipulation",
        "description": "block.timestamp can be manipulated by miners within ~15 seconds.",
        "solidity_snippet": """function isWinner() public view returns (bool) {
    return block.timestamp % 15 == 0; // miner-manipulable
}""",
        "detected_by": ["claude"],
    },
    {
        "id": "v005", "title": "Unchecked External Call", "category": "Error Handling",
        "severity": "high", "swc_id": "SWC-104", "cwe_id": "CWE-252",
        "real_exploit": "King of the Ether — fund lock",
        "description": "Return value of .call() is ignored; failed transfers are silent.",
        "solidity_snippet": """function payout(address payable recipient) internal {
    recipient.call{value: prize}(""); // return value ignored
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v006", "title": "Access Control Missing", "category": "Access Control",
        "severity": "critical", "swc_id": "SWC-105", "cwe_id": "CWE-284",
        "real_exploit": "Parity Wallet init() — $30M",
        "description": "Initialisation function callable by anyone after deployment.",
        "solidity_snippet": """function initWallet(address[] memory _owners) public {
    // no check — anyone can reinitialise
    owners = _owners;
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v007", "title": "Front-Running (MEV)", "category": "Transaction Order",
        "severity": "high", "swc_id": "SWC-114", "cwe_id": "CWE-362",
        "real_exploit": "ERC-20 approve front-run — recurring",
        "description": "Attacker watches mempool and frontruns approve/transferFrom sequence.",
        "solidity_snippet": """function approve(address spender, uint256 amount) public returns (bool) {
    allowance[msg.sender][spender] = amount; // no increase/decreaseAllowance
    return true;
}""",
        "detected_by": ["claude", "gpt-4"],
    },
    {
        "id": "v008", "title": "Weak PRNG", "category": "Randomness",
        "severity": "high", "swc_id": "SWC-120", "cwe_id": "CWE-338",
        "real_exploit": "PRNG exploit — Fomo3D 2018",
        "description": "blockhash used as randomness source is predictable by miners.",
        "solidity_snippet": """function random() private view returns (uint) {
    return uint(blockhash(block.number - 1)) % 100;
}""",
        "detected_by": ["gpt-4", "claude", "gemini"],
    },
    {
        "id": "v009", "title": "Unsafe Delegatecall", "category": "Delegatecall",
        "severity": "critical", "swc_id": "SWC-112", "cwe_id": "CWE-829",
        "real_exploit": "Parity Wallet Freeze 2017 — $150M",
        "description": "Delegatecall to user-supplied address allows storage overwrite.",
        "solidity_snippet": """function execute(address target, bytes memory data) external {
    target.delegatecall(data); // arbitrary delegatecall
}""",
        "detected_by": ["gpt-4", "claude"],
    },
    {
        "id": "v010", "title": "Flash Loan Oracle Manipulation", "category": "Oracle",
        "severity": "critical", "swc_id": "SWC-136", "cwe_id": "CWE-682",
        "real_exploit": "Harvest Finance 2020 — $34M",
        "description": "Price oracle reads from an AMM spot price, manipulable within one block.",
        "solidity_snippet": """function getPrice() public view returns (uint) {
    return IUniswapPair(pair).getReserves()[0] / IUniswapPair(pair).getReserves()[1];
}""",
        "detected_by": ["claude", "gpt-4"],
    },
    {
        "id": "v011", "title": "tx.origin Authentication", "category": "Authentication",
        "severity": "medium", "swc_id": "SWC-115", "cwe_id": "CWE-287",
        "real_exploit": "Phishing attack pattern — theoretical",
        "description": "tx.origin authentication bypassed via phishing contract intermediary.",
        "solidity_snippet": """function transfer(address to, uint amount) public {
    require(tx.origin == owner); // should be msg.sender
    balances[to] += amount;
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v012", "title": "Storage Collision (Proxy)", "category": "Proxy Pattern",
        "severity": "critical", "swc_id": "SWC-124", "cwe_id": "CWE-119",
        "real_exploit": "Audius hack 2022 — $6M",
        "description": "Proxy and implementation share slot 0, causing variable collision.",
        "solidity_snippet": """contract Proxy {
    address public implementation; // slot 0
}
contract Logic {
    address public owner; // also slot 0 — collision!
}""",
        "detected_by": ["claude", "gpt-4"],
    },
    {
        "id": "v013", "title": "Signature Replay", "category": "Authentication",
        "severity": "high", "swc_id": "SWC-121", "cwe_id": "CWE-294",
        "real_exploit": "Multichain exploit 2023 — $126M",
        "description": "Signed messages can be replayed on different chains or after expiry.",
        "solidity_snippet": """function execute(bytes32 hash, bytes memory sig) external {
    address signer = ECDSA.recover(hash, sig);
    require(signer == owner); // no nonce, no chainId
}""",
        "detected_by": ["claude", "gpt-4", "gemini"],
    },
    {
        "id": "v014", "title": "Gas Limit DoS", "category": "Denial of Service",
        "severity": "medium", "swc_id": "SWC-128", "cwe_id": "CWE-400",
        "real_exploit": "GovernMental DoS — fund lock",
        "description": "Unbounded loop over a dynamic array can exceed block gas limit.",
        "solidity_snippet": """function distributeRewards() external {
    for (uint i = 0; i < recipients.length; i++) { // unbounded
        recipients[i].transfer(reward);
    }
}""",
        "detected_by": ["gpt-4", "claude", "gemini", "copilot"],
    },
    {
        "id": "v015", "title": "Shadowed State Variable", "category": "Inheritance",
        "severity": "low", "swc_id": "SWC-119", "cwe_id": "CWE-710",
        "real_exploit": "Logic error in production — Compound-style",
        "description": "Child contract declares a variable with the same name as parent, silently shadowing it.",
        "solidity_snippet": """contract Base { address public owner; }
contract Child is Base {
    address public owner; // shadows Base.owner — separate storage slot
}""",
        "detected_by": ["gpt-4", "claude", "gemini"],
    },
]
