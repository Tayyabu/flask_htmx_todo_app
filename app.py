from todos import app
from todos.db import db
from todos.routes import *
import os

if __name__ == "__main__":
    
    app.run(port=4000, debug=True)
