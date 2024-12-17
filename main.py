# Import
from flask import Flask, render_template,request, redirect
# Importowanie biblioteki bazy danych
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Podłączanie SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating a DB
db = SQLAlchemy(app )

#Zadanie nr 1. Utwórz tabelę DB
class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    subtitle = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f'<Card {self.id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)



@app.route('/', methods = ['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        users_db = User.query.all()
        for user in users_db:
            if form_login == user.login and form_password == user.password:
                return redirect('/index')
        error = 'Niepoprawne dane logowania'
    return render_template('login.html', error=error)

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('registration.html')




# Uruchamianie strony z treścią
@app.route('/index')
def index():
    # Wyświetlanie obiektów Bazy
    # Assignment #2. Display the objects from the DB in index.html
    cards = Card.query.order_by(Card.id).all()

    return render_template('index.html',
                           cards = cards

                           )

# Uruchomienie strony z kartą
@app.route('/card/<int:id>')
def card(id):
    #Zadanie #2. Wyświetl właściwą kartę według jej identyfikatora
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Uruchomienie strony i utworzenie karty
@app.route('/create')
def create():
    return render_template('create_card.html')

# Formularz karty
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Zadanie #2. Stwórz sposób przechowywania danych w bazie danych
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()




        return redirect('/index')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
