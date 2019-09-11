from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    addr = db.Column(db.String(128))

# set FLASK_APP = sample_migration.py

# In Power shell
# $env:FLASK_APP = "sample_migration.py"
# flask db init

# New change execute the below command
# flask db migrate
# flask db upgrade