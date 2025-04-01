from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import random
import uvicorn

class SimulationRequest(BaseModel):
    p: float = Field(..., gt=0, le=1, description="Probability of winning each bet")
    q: float = Field(..., ge=1, description="Payout multiplier")
    bet: float = Field(..., gt=0, description="Initial bet size")
    starting_money: float = Field(..., gt=0, description="Initial amount of money")
    goal: float = Field(..., gt=0, description="Money goal to reach")
    k: Optional[float] = Field(0, ge=0, description="Line of credit amount")
    max_bet: Optional[float] = Field(None, gt=0, description="Maximum table bet")
    num_simulations: Optional[int] = Field(10000, ge=100, description="Number of simulations to run")

class SimulationResponse(BaseModel):
    win_probability: float
    loss_probability: float

app = FastAPI(
    title="Gambler's Ruin Simulator",
    description="API for simulating gambling scenarios with various parameters",
    version="1.0.0"
)

def generalized_gambler_sim(p, q, bet, starting_money, goal, k=0, max_bet=None, num_simulations=10000):
    win_count = 0
    loss_count = 0

    for _ in range(num_simulations):
        money = starting_money
        credit_remaining = k
        losing_streak = 0

        while 0 < money < goal:
            current_bet = bet * (1 / p) ** losing_streak

            if max_bet is not None:
                current_bet = min(current_bet, max_bet)

            if current_bet > money:
                needed = current_bet - money
                loan = min(needed, credit_remaining)
                credit_remaining -= loan
                money += loan

            if current_bet > money:
                break

            if random.random() < p:
                winnings = current_bet * (q - 1)
                money += winnings
                losing_streak = 0
            else:
                money -= current_bet
                losing_streak += 1

        if money >= goal:
            win_count += 1
        else:
            loss_count += 1

    win_prob = win_count / num_simulations
    loss_prob = loss_count / num_simulations

    return win_prob, loss_prob

@app.post("/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    win_prob, loss_prob = generalized_gambler_sim(
        p=request.p,
        q=request.q,
        bet=request.bet,
        starting_money=request.starting_money,
        goal=request.goal,
        k=request.k,
        max_bet=request.max_bet,
        num_simulations=request.num_simulations
    )
    
    return SimulationResponse(
        win_probability=win_prob,
        loss_probability=loss_prob
    ) 

if __name__ == "__main__":
    
    # Run the FastAPI application with uvicorn server
    # Host 0.0.0.0 makes it accessible from external machines
    # Port 8000 is the default for FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)

