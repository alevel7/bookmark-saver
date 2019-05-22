from flask_bootstrap import Bootstrap
from flask import Flask
from  flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
app = Flask(__name__)

#configure database
app.config['SECRET_KEY'] = '\x902\xcd\xb1w\xf6+\xa0f\\1J\xab\xc1\xcd?S\xb5B\xa91\t\x1e\x85'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Oluranti08056965@localhost:3306/test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Bootstrap(app)
db =SQLAlchemy(app)
#for displaying timestamp
moment = Moment(app)
import models