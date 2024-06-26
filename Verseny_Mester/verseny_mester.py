from flask import Flask, render_template, request, redirect, url_for, session
import data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
@app.route('/home')
def home():
    session.pop('chosen_sport', None)
    session.pop('formats', None)
    session.pop('chosen_format', None)
    session.pop('tournament_name', None)
    session.pop('names', None)
    
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
    return redirect(url_for('enter_tournament_name'))

@app.route('/enter_tournament_name', methods=['GET', 'POST'])
def enter_tournament_name():
    if request.method == 'POST':
        tournament_name = request.form.get('tournament_name')
        session['tournament_name'] = tournament_name
        return redirect(url_for('enter_name'))
    return render_template('enter_tournament_name.html', title='Verseny név megadása')

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
    tournament_name = session.get('tournament_name', '')
    names = session.get('names', [])
    return render_template('review.html', title='Áttekintés', chosen_sport=chosen_sport, chosen_format=chosen_format, tournament_name=tournament_name, names=names)

@app.route('/enter_results', methods=['GET', 'POST'])
def enter_results():
    if request.method == 'POST':
        return redirect(url_for('home'))
    
    names = session.get('names', [])
    chosen_sport = session.get('chosen_sport', '')
    tournament_name = session.get('tournament_name', '')
    return render_template('enter_results.html', title='Eredmények felvétele', names=names, chosen_sport=chosen_sport, tournament_name=tournament_name)




# Eddig


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Elérhetőség')

if __name__ == '__main__':
    app.run(debug=True)

