from flask import Flask, render_template, request,  jsonify
from helpers import todo
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


@app.route("/api")
def get_api():
    # 'Open Notify' API endpoint URLs
    jokes_api_url: str = "https://official-joke-api.appspot.com/random_joke"

    # using the requests library's get function to call the API, store data as a variable
    # don't worry about the type, Python will take care of this
    data = requests.get(jokes_api_url)
    response = data.json()
    return response  # converts to a format that Python can use


@app.route("/jokes")
def my_jokes():
    a_joke: dict[str, str] = get_api()
    return render_template('jokes.html', setup=a_joke["setup"], punchline=a_joke["punchline"])


if __name__ == '__main__':
    app.run(debug=True)
