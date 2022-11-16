from flask import Flask, render_template, request
from helpers import todo

# a python library to fetch APIs -- different from request in the flask library
import requests

todo_list: list[todo] = []
todo_count: int = 0

app: Flask = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/jokes")
def my_jokes():
    a_joke: dict[str, str] = get_a_joke()
    return render_template('jokes.html', setup=a_joke["setup"], punchline=a_joke["punchline"])


@app.route("/many-jokes")
def many_jokes():
    ten_jokes: list[dict[str, str]] = get_10_jokes()
    return render_template('many-jokes.html', jokes=ten_jokes)


# API CALLS

@app.route("/api/joke")
def get_a_joke() -> dict[str, str]:

    # Joke API endpoint URLs
    jokes_api_url: str = "https://official-joke-api.appspot.com/random_joke"

    # using the requests library's get function to call the API, store data as a variable
    # don't worry about the type, Python will take care of this
    data = requests.get(jokes_api_url)

    # Parse JSON to a dict[str, str]
    # be careful of json structure -- sometimes it can be formatted within a list!
    response: dict[str, str] = data.json()
    return response


@app.route("/api/ten_jokes")
def get_10_jokes() -> list[dict[str, str]]:

    # Joke API endpoint URLs
    jokes_api_url: str = "https://official-joke-api.appspot.com/random_ten"

    # using the requests library's get function to call the API, store data as a variable
    # don't worry about the type, Python will take care of this
    data = requests.get(jokes_api_url)

    # Parse JSON to a dict[str, str]
    # The response JSON is now a LIST of dictionaries! It's important to know the structure of response JSON!
    response: list[dict[str, str]] = data.json()
    return response


if __name__ == '__main__':
    app.run(debug=True)
