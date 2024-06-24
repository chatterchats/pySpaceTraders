# pySpaceTraders

pySpaceTrader is a Python-based SDK for the space trading game, **SpaceTraders**, where you can trade goods, explore space, and manage resources. This project is designed to provide a convenient way to access the game\'s API to play the game.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Contact](#contact)

## Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chatterchats/pySpaceTraders.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pySpaceTraders
   ```
3. Install poetry:   
   [Poetry Install Documentation](https://python-poetry.org/docs/#installing-with-the-official-installer)
    

4. Install packages
   ```bash
    poetry install
   ```

## Usage

To utilize the SDK:
```bash
pip install pySpaceTraders
```

```python
from pySpaceTraders import SpaceTraderClient, FactionSymbol

client = SpaceTraderClient(
    agent_symbol="NEWUSER",
    agent_faction=FactionSymbol.COSMIC,
    agent_email="",
    log=True,
    debug=True
)

player = client.my_agent()
>>> player
Agent(
    symbol="NEWUSER", 
    headquarters="AA-BBBB-CC", 
    credits=175000, 
    startingFaction=<FactionSymbol.COSMIC: 'COSMIC'>,
    shipCount=2,
    accountId="abcdefghijklmnopqrstuvwxy"
)

>>> player.symbol
"NEWUSER"
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](.github/CONTRIBUTING.md) for detailed instructions on how to get started.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](.github/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, open an issue on GitHub.
