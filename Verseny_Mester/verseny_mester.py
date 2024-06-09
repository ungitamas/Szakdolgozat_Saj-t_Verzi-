from flask import Flask, render_template, request, redirect, url_for, session
import data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
@app.route('/home')
def home():
    return render_template('choose_sport.html', title='Sportágak', sports=data.sports)

@app.route('/choosing_sport', methods=['POST'])
def choosing_sport():
    chosen_sport = request.form.get('sport')
    session['chosen_sport'] = chosen_sport
    
    if chosen_sport in ['Röplabda', 'Kézilabda', 'Kosárlabda', 'Labdarúgás']:
        session['formats'] = data.formats_team
    elif chosen_sport in ['Úszás', 'Atlétika']:
        session['formats'] = data.formats_individual
    
    return redirect(url_for('choose_format'))

@app.route('/choose_format')
def choose_format():
    formats = session.get('formats', [])
    chosen_sport = session.get('chosen_sport', '')
    return render_template('choose_format.html', title='Formátumok', formats=formats, chosen_sport=chosen_sport)

@app.route('/choosing_format', methods=['POST'])
def choosing_format():
    chosen_format = request.form.get('format')
    session['chosen_format'] = chosen_format
    session['names'] = []
    return redirect(url_for('enter_name'))

@app.route('/enter_name', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form.get('name')
        if 'names' not in session:
            session['names'] = []
        names = session['names']
        names.append(name)
        session['names'] = names

    chosen_sport = session.get('chosen_sport', '')
    names = session.get('names', [])
    return render_template('enter_name.html', title='Név megadása', chosen_sport=chosen_sport, names=names)

@app.route('/review')
def review():
    chosen_sport = session.get('chosen_sport', '')
    chosen_format = session.get('chosen_format', '')
    names = session.get('names', [])
    return render_template('review.html', title='Áttekintés', chosen_sport=chosen_sport, chosen_format=chosen_format, names=names)



@app.route('/contact')
def contact():
    return render_template('contact.html', title='Elérhetőség')

if __name__ == '__main__':
    app.run(debug=True)

