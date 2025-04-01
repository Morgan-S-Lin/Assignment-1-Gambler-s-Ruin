# Gambler's Ruin Simulation

This project implements a simulation of the Gambler's Ruin problem with additional features like credit lines and maximum bet limits. The simulation is built using Python and Streamlit, providing an interactive web interface for exploring different gambling scenarios.

## Features

- Interactive web interface using Streamlit
- Configurable parameters:
  - Probability of winning (p)
  - Payout multiplier (q)
  - Initial bet amount
  - Starting money
  - Goal amount
  - Number of simulations
- Optional credit line feature
- Optional maximum bet limit
- Real-time probability calculations
- Visual results display

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run gamblers_ruin.py
   ```

## Usage

1. Adjust the simulation parameters using the sliders and input fields
2. Enable/disable credit line and maximum bet features as needed
3. Click "Run Simulation" to see the results
4. The simulation will show:
   - Probability of reaching the goal amount
   - Probability of going broke
   - Number of iterations performed

## Mathematical Background

The Gambler's Ruin problem is a classic probability problem that examines the likelihood of a gambler reaching a certain goal amount or going broke, given:
- Initial capital
- Probability of winning each bet
- Payout ratio
- Goal amount

This implementation extends the classic problem by incorporating:
- Credit lines (k)
- Maximum bet limits
- Variable bet sizing based on losing streaks 