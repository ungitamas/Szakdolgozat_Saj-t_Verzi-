from flask import Flask, render_template, request
from data import add_name, get_names
import random

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('competitions.html', title='Versenyek')

@app.route('/competitions')
def competitions():
    return render_template('competitions.html', competitions=competitions, title='Versenyek')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Elérhetőség')

@app.route('/create_names/new', methods=['GET', 'POST'])
def create_names():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            add_name(name)
    return render_template('create_names.html', title='Nevek', names=get_names())

@app.route('/straight_elimination')
def straight_elimination():
    names = get_names()
    random.shuffle(names)
    return render_template('straight_elimination.html', title='Egyenes kiesés', names=names)

if __name__ == '__main__':
    app.run(debug=True)

