import streamlit as st
import random

def generalized_gambler_sim(p, q, bet, starting_money, goal, k=0, max_bet=None, num_simulations=10000):
    win_count = 0
    loss_count = 0

    for _ in range(num_simulations):
        money = starting_money
        credit_remaining = k
        losing_streak = 0

        while 0 < money < goal:
            # Adjust bet based on losing streak
            current_bet = bet * (1 / p) ** losing_streak

            # Cap bet if above table max
            if max_bet is not None:
                current_bet = min(current_bet, max_bet)

            # If bet is more than money, use remaining credit
            if current_bet > money:
                needed = current_bet - money
                loan = min(needed, credit_remaining)
                credit_remaining -= loan
                money += loan

            # If still can't place the bet, break
            if current_bet > money:
                break

            if random.random() < p:
                # Win
                winnings = current_bet * (q - 1)
                money += winnings
                losing_streak = 0
            else:
                # Loss
                money -= current_bet
                losing_streak += 1

        if money >= goal:
            win_count += 1
        else:
            loss_count += 1

    win_prob = win_count / num_simulations
    loss_prob = loss_count / num_simulations

    return win_prob, loss_prob

# Set up the Streamlit UI
st.title("Gambler's Ruin Simulation")
st.write("Adjust the parameters below to simulate different gambling scenarios")

# Create input controls
col1, col2 = st.columns(2)

with col1:
    p = st.slider("Probability of Winning (p)", 0.0, 1.0, 0.5, 0.01)
    q = st.number_input("Payout Multiplier (q)", min_value=1.0, value=2.0, step=0.1)
    bet = st.number_input("Initial Bet", min_value=1, value=1)
    starting_money = st.number_input("Starting Money", min_value=1, value=10)

with col2:
    goal = st.number_input("Goal Amount", min_value=1, value=20)
    num_simulations = st.number_input("Number of Simulations", min_value=100, value=10000, step=100)
    
    # Add checkbox for enabling credit line
    enable_credit = st.checkbox("Enable Credit Line")
    k = st.number_input("Credit Line Amount (k)", min_value=0, value=5, disabled=not enable_credit)
    
    # Add checkbox for enabling maximum bet
    enable_max_bet = st.checkbox("Enable Maximum Bet")
    max_bet = st.number_input("Maximum Bet Amount", min_value=1, value=8, disabled=not enable_max_bet)

# Run simulation button
if st.button("Run Simulation"):
    # Set k and max_bet to None if not enabled
    k_value = k if enable_credit else 0
    max_bet_value = max_bet if enable_max_bet else None
    
    # Run simulation
    win_prob, loss_prob = generalized_gambler_sim(
        p, q, bet, starting_money, goal, 
        k=k_value, 
        max_bet=max_bet_value,
        num_simulations=num_simulations
    )
    
    # Display results
    st.header("Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Probability of Winning", f"{win_prob:.4f}")
    with col2:
        st.metric("Probability of Going Broke", f"{loss_prob:.4f}")
    
    # Add a note about the simulation
    st.info(f"Simulation completed with {num_simulations:,} iterations")
