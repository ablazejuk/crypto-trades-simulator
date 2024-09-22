# Crypto Trades Simulator

**Crypto Trades Simulator** is a Python-based GUI application that simulates cryptocurrency trades using real-time data from the CoinGecko API. The application allows users to "buy" cryptocurrencies with a simulated balance, view the value of their holdings, and persist their data between sessions.

## Features

- **Real-Time Pricing**: Fetches real-time cryptocurrency prices in BRL from the CoinGecko API.
- **Simulated Trading**: Allows users to buy fractions of cryptocurrencies using a simulated balance.
- **Data Persistence**: Saves and loads the user's balance and cryptocurrency holdings across sessions.
- **User-Friendly Interface**: A simple and intuitive GUI built with Tkinter.
- **Automatic Updates**: Automatically refreshes cryptocurrency prices every minute.

## Installation

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Tkinter**: Tkinter is included with most Python installations. If it's not installed, you can install it using:

```bash
  sudo apt-get install python3-tk
```

### Clone the Repository

```bash
git clone https://github.com/ablazejuk/crypto-trades-simulator.git
cd crypto-trades-simulator
```

### Install Required Packages

```bash
pip install requests
```

## Configuration

### Configure pre-push git hook to check types

```bash
pre-commit install --hook-type pre-push
```

## Usage

1. **Run the Application**:

   Navigate to the project directory and run:

   ```bash
   python app.py
   ```

2. **Simulate Trades**:

   - **Fetch Prices**: Click the "Fetch Prices" button to get the latest cryptocurrency prices.
   - **Buy Cryptocurrency**: Enter the amount in BRL you want to spend and click the respective "Buy" button next to the cryptocurrency you want to buy.
   - **View Holdings**: The table shows your purchased quantities and their current value in BRL.

3. **Persist Data**:

   Your balance and cryptocurrency holdings are automatically saved when you close the application. When you reopen it, your data will be restored.

## Project Structure

crypto-trades-simulator/

- `gui.py`           # Main GUI application file

- `crypto_data.json` # File for persisting balance and purchases

- `README.md`        # Project documentation

## Troubleshooting

- **API Request Errors**: If the application fails to fetch cryptocurrency prices, ensure you have an active internet connection. The app will log errors in the console for debugging.
- **Insufficient Balance**: Ensure you have enough simulated balance to buy the desired amount of cryptocurrency.

## Future Improvements

- **Portfolio Analysis**: Provide more detailed analytics on the user's portfolio.
- **Support for More Cryptocurrencies**: Extend the list of supported cryptocurrencies.

## Check types

```bash
   mypy .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **CoinGecko API**: For providing real-time cryptocurrency prices.
- **Tkinter**: For the simple and effective GUI toolkit.
