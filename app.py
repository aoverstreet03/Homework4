from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
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
    playerId = IntegerField('Player ID:')
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    player_position = StringField('Player Position:', validators=[DataRequired()])

@app.route('/')
def index():
    all_players = overstreet_dolphinsapp.query.all()
    return render_template('index.html',  players=all_players, pageTitle='Miami Dolphins Players')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        print(search_value)
        search = "%{}%".format(search_value)
        print(search)
        results = overstreet_dolphinsapp.query.filter(overstreet_dolphinsapp.first_name.like(search)).all()
        return render_template('index.html', players=results, pageTitle='Dolphins Players', legend='Search Results')
    else:
        return redirect('/')


@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = DolphinsForm()
    if form.validate_on_submit():
            player = overstreet_dolphinsapp(first_name=form.first_name.data, last_name=form.last_name.data, player_position=form.player_position.data)
            db.session.add(player)
            db.session.commit()
            return redirect('/')

    return render_template('add_player.html', form=form, pageTitle='Add A New Dolphins Player')

@app.route('/delete_player/<int:playerId>', methods=['GET','POST'])
def delete_player(playerId):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        player = overstreet_dolphinsapp.query.get_or_404(playerId)
        db.session.delete(player)
        db.session.commit()
        flash('Player was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect

@app.route('/player/<int:player_id>/update', methods=['GET','POST'])
def update_player(player_id):
    player = overstreet_dolphinsapp.query.get_or_404(player_id)
    form = DolphinsForm()
    if form.validate_on_submit():
        player.player_position = form.player_position.data
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        db.session.commit()
        flash('Your player has been updated.')
        return redirect(url_for('get_player', player_id=player.playerId))
    #elif request.method == 'GET':
    form.playerId.data = player.playerId
    form.player_position.data = player.player_position
    form.first_name.data = player.first_name
    form.last_name.data = player.last_name
    return render_template('update_player.html', form=form, pageTitle='Update Post',
                            legend="Update A Player")


@app.route('/player/<int:player_id>', methods=['GET','POST'])
def get_player(player_id):
    player = overstreet_dolphinsapp.query.get_or_404(player_id)
    return render_template('player.html', form=player, pageTitle= 'Player Details', legend='Details Page')

if __name__ == '__main__':
    app.run(debug=True)
