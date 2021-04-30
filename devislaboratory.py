from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


devislaboratory = Flask(__name__)
devislaboratory.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devislab.db'
devislaboratory.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(devislaboratory)



class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    effect = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    adress = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    tshirt = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return  '<Orders %r>' % self.id


@devislaboratory.route('/')
def index():
    return render_template('index.html')


@devislaboratory.route('/video')
def video():
    return render_template('video.html')


@devislaboratory.route('/order', methods=['POST', 'GET'])
def order():
    if request.method == 'POST':
        effect = request.form['Effect']
        email = request.form['Email']
        name = request.form['Name']
        state = request.form['State']
        city = request.form['City']
        surname = request.form['Surname']
        adress = request.form['Adress']
        postcode = request.form['Postcode']
        tshirt = request.form['TShirt']
        price = request.form['Price']

        order = Orders(effect=effect, email=email, name=name,
                       state=state, city=city, surname=surname,
                       adress=adress, postcode=postcode,
                       tshirt=tshirt, price=price)

        try:
            db.session.add(order)
            db.session.commit()
            return redirect('/completeOrder')
        except:
            return 'Error'

    else:
        return render_template('order.html')

@devislaboratory.route('/completeOrder')
def completeOrder():
    completeOrder = Orders.query.order_by(Orders.date.desc()).all()
    return render_template("completeOrder.html", completeOrder=completeOrder)


@devislaboratory.route('/completeOrder/<int:id>/del')
def orderDelete(id):
    completeOrder = Orders.query.get_or_404(id)

    try:
        db.session.delete(completeOrder)
        db.session.commit()
        return redirect('/completeOrder')
    except:
        return 'Error'


@devislaboratory.route('/effects')
def effects():
    return render_template('effects.html')


@devislaboratory.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    devislaboratory.run(debug=True)
