from typing import Literal


from . import login_manager, app
from .db import User, Todo, db
from flask_login import login_user, logout_user, current_user
from flask import abort, render_template, request
from .forms import RegisterForm, LoginForm, TodoForm
from sqlalchemy import select, update


@login_manager.user_loader
def load_user(user_id) -> User | None:
    return db.session.query(User).get(int(user_id))  # type: ignore


@app.route("/")
def index() -> str:
    todos = (
        db.session.query(Todo).filter_by(user_id=int(current_user.id)).all()
        if current_user.is_authenticated
        else None
    )
    return render_template("index.html", todos=todos)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        duplicate_user = (
            db.session.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        )
        if duplicate_user:
            return render_template(
                "partials/alert.html", message="User Already Exists!", error=True
            )

        if password != confirm_password:
            return render_template(
                "partials/alert.html", message="Passwords are not Matching!", error=True
            )
        user = User(username=username, email=email, password=password)  # type: ignore

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return render_template(
            "partials/alert.html",
            message="You are Registered successfully",
            error=False,
        )

    return render_template("register.html", form=form)


@app.route("/add-todo", methods=["GET", "POST"])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        title = request.form.get("title")
        content = request.form.get("content")

        todo = Todo(title=title, content=content, user_id=int(current_user.id))  # type: ignore
        db.session.add(todo)
        db.session.commit()
        todos = db.session.query(Todo).filter_by(user_id=int(current_user.id)).all()
        return render_template("partials/todos.html", todos=todos)

    return render_template("todo-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(User).filter((User.email == email)).first()
        if user is None:
            return render_template(
                "partials/alert.html", message="Please Enter correct Email!", error=True
            )
        if not user.is_valid_password(password):
            return render_template(
                "partials/alert.html",
                message="Please Enter correct password!",
                error=True,
            )
        login_user(user)

        return render_template(
            "partials/alert.html",
            message="You are Logged in successfully",
            error=False,
        )

    return render_template("login.html", form=form)


@app.get("/logout")
def logout():
    logout_user()
    return "You are Logged out"


@app.delete("/delet-todo/<int:id>")
def delete_todo(id):
    todo = (Todo).query.get_or_404(id)
    if todo.user_id != current_user.id:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    todos = db.session.query(Todo).filter_by(user_id=int(current_user.id)).all()
    return render_template("partials/todos.html", todos=todos)


@app.route("/edit-todo/<int:id>", methods=["GET", "POST"])
def edit_todo(id):
    # 1. Fetch the existing todo (use get_or_404 for better safety)
    todo = db.session.query(Todo).get_or_404(id)  # type: ignore
    # 2. Initialize form with existing object data
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        # 3. Populate the existing object with validated form data

        if todo.user_id != current_user.id:
         abort(403)
        db.session.commit()

        # 4. Fetch fresh list for the partial
        todos = db.session.query(Todo).filter_by(user_id=current_user.id).all()

        # Ensure your frontend target is the PARENT container of the list
        return render_template("partials/todos.html", todos=todos)

    return render_template("todo-form.html", form=form, todo=todo)


@app.get("/search-todos")
def search_todos():
    # Use request.args for GET requests
    search_pattern = request.args.get("search_term", "").lower()

    # Get todos for current user
    todos = db.session.query(Todo).filter_by(user_id=int(current_user.id)).all()

    # Filter in Python
    filtered_todos = [
        t
        for t in todos
        if search_pattern in t.title.lower() or search_pattern in t.content.lower()
    ]

    return render_template("partials/todos.html", todos=filtered_todos)


@app.patch("/toggle-todo/<int:id>")
def toggle_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    if todo.user_id != current_user.id:
        abort(403)
    db.session.commit()
    return render_template("partials/todo.html", todo=todo)


@app.get("/rerender-navbar")
def rerender_navbar():
    return render_template("partials/navbar.html")
