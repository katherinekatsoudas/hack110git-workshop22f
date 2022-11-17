from flask import Flask, render_template, request,  jsonify
from helpers import todo

# a python library to fetch APIs -- different from request in the flask library
import requests

todo_list: list[todo] = []
todo_count: int = 0

app: Flask = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/create-todo', methods=["GET", "POST"])
def create_todo():
    if request.method == "POST":
        global todo_list
        global todo_count

        title: str = request.form['title']
        description: str = request.form['description']
        color: str = request.form['color']

        if title == '':
            return render_template("create-todo.html")

        new_todo: todo = todo(todo_count, title, description, color)
        todo_list.append(new_todo)

        todo_count += 1

        return render_template("success.html", title=title, description=description, color=color)
    return render_template("create-todo.html")


@app.route('/view-todo-list', methods=["GET", "POST"])
def view_todo_list():
    if request.method == "POST" and len(todo_list) > 0:
        idx: int = int(request.form['check-button'])
        todo_list[idx].checked = not todo_list[idx].checked
    return render_template('view-list.html', todo_list=todo_list)


@app.route('/edit-todo<todo_number>', methods=["GET", "POST"])
def edit_todo(todo_number: str):
    if request.method == "POST":
        global todo_list

        title: str = request.form['title']
        description: str = request.form['description']
        color: str = request.form['color']

        if title == '':
            return render_template("edit-todo.html")

        todo_list[int(todo_number)].title = title
        todo_list[int(todo_number)].description = description
        todo_list[int(todo_number)].color = color

        return render_template("edit-success.html")
    return render_template('edit-todo.html', todo=todo_list[int(todo_number)])


@app.route("/api/joke")
def get_a_joke() -> dict[str, str]:

    # Joke API endpoint URLs
    jokes_api_url: str = "https://official-joke-api.appspot.com/random_joke"

    # using the requests library's get function to call the API, store data as a variable
    # don't worry about the type, Python will take care of this
    data = requests.get(jokes_api_url)

    # Parse JSON to a dict[str, str]
    # be careful of json structure -- sometimes it can be formatted within a list!
    response = data.json()
    return response


@app.route("/jokes")
def my_jokes():
    a_joke: dict[str, str] = get_a_joke()
    return render_template('jokes.html', setup=a_joke["setup"], punchline=a_joke["punchline"])


def get_a_def() -> dict[str, str]:
    # Below lines of code are all from the API documentation: https://developer.oxforddictionaries.com/documentation/getting_started
    # Follow along with the documentation and create an account to generate a unique app id and key 
    app_id = "Replace with your id"
    app_key = "<Replace with your key>"

    language = "en-gb" # sets language to English

    word_id = "example" # change this variable to see different word definitions

    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    data = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    response = data.json()
    return response


@app.route("/definitions")
def my_definitions():
    # Right now, we are just returning the plain dictionary
    # Look at the jokes example we did earlier if you want to experiment with reformatting the data!
    # Read the Oxford Dictionary API documentation for more information on how to use the API!
    a_definition: dict[str, str] = get_a_def()
    return a_definition



if __name__ == '__main__':
    app.run(debug=True)
