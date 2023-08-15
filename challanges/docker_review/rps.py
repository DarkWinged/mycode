#!/usr/bin/env python3
"""
To use, try:
    curl localhost:5000/paper
    curl localhost:5000/rock
    curl localhost:5000/scissors
"""

import random
from flask import Flask
app = Flask(__name__)

choices = ["paper", "rock", "scissors"]

# if user sends HTTP GET to /paper
@app.route("/paper")
def paper():
    user_choice = "paper"
    computer_choice = random.choice(choices)
    result = determine_winner(user_choice, computer_choice)
    return f"Computer chose: {computer_choice}\n{result}"

# if user sends HTTP GET to /rock
@app.route("/rock")
def rock():
    user_choice = "rock"
    computer_choice = random.choice(choices)
    result = determine_winner(user_choice, computer_choice)
    return f"Computer chose: {computer_choice}\n{result}"

# if user sends HTTP GET to /scissors
@app.route("/scissors")
def scissors():
    user_choice = "scissors"
    computer_choice = random.choice(choices)
    result = determine_winner(user_choice, computer_choice)
    return f"Computer chose: {computer_choice}\n{result}"

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (
        (user_choice == "paper" and computer_choice == "rock") or
        (user_choice == "rock" and computer_choice == "scissors") or
        (user_choice == "scissors" and computer_choice == "paper")
    ):
        return "You win!"
    else:
        return "Computer wins!"

# bind to all IP addresses port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
