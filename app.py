from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY']= 'aJasldihfaEJKF105urwrfhsJAJF'

class DolphinsForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    player_position = StringField('Player Position:', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', pageTitle='Miami Dolphins Players')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = DolphinsForm()
    if form.validate_on_submit():
                return "<h2> The Dolphins player's name is {0} {1} and their position is {2}.".format(form.first_name.data, form.last_name.data, form.player_position.data)

    return render_template('add_player.html', form=form, pageTitle='Add A New Dolphins Player')


if __name__ == '__main__':
    app.run(debug=True)
