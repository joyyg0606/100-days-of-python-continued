from flask import Flask, render_template_string
import random

app = Flask(__name__)

random_number = random.randint(0, 9)
print(f"Random Number: {random_number}")

# HTML Templates
home_page = """
<h1>Guess a number between 0 and 9</h1>
<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"/>
"""

high_page = """
<h1 style="color: purple">Too high, try again!</h1>
<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>
"""

low_page = """
<h1 style="color: red">Too low, try again!</h1>
<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>
"""

found_page = """
<h1 style="color: green">You found me!</h1>
<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>
"""

@app.route('/')
def home():
    return render_template_string(home_page)


@app.route("/<guess>")
def guess_number(guess):
    try:
        guess = int(guess)
    except ValueError:
        return "<h1 style='color: orange'>Invalid input! Please enter a number.</h1>"

    if guess > random_number:
        return render_template_string(high_page)
    elif guess < random_number:
        return render_template_string(low_page)
    else:
        global random_number
        random_number = random.randint(0, 9)  # Reset the number after a win
        print(f"New Random Number: {random_number}")
        return render_template_string(found_page)


if __name__ == "__main__":
    app.run(debug=True)