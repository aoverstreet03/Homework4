from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)


app = Flask(__name__)
app.config['SECRET_KEY']= 'aJasldihfaEJKF105urwrfhsJAJF'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class overstreet_dolphinsapp(db.Model):
    playerId= db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    player_position = db.Column(db.String(255))

def __repr__(self):
        return "playerId: {0} | first name: {1} | last name: {2} | player position: {3}".format(self.id, self.first_name, self.last_name, self.player_position)

class DolphinsForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    player_position = StringField('Player Position:', validators=[DataRequired()])

@app.route('/')
def index():
    all_players = overstreet_dolphinsapp.query.all()
    return render_template('index.html',  players=all_players, pageTitle='Miami Dolphins Players')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = DolphinsForm()
    if form.validate_on_submit():
            player = overstreet_dolphinsapp(first_name=form.first_name.data, last_name=form.last_name.data, player_position=form.player_position.data)
            db.session.add(player)
            db.session.commit()
            return "<h2> The Dolphins player's name is {0} {1} and their position is {2}.".format(form.first_name.data, form.last_name.data, form.player_position.data)

    return render_template('add_player.html', form=form, pageTitle='Add A New Dolphins Player')


if __name__ == '__main__':
    app.run(debug=True)
