from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration — use /tmp so Vercel's read-only filesystem doesn't block writes
db_path = '/tmp/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Item Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }

# Initialize Database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    
    new_item = Item(name=name, description=description, price=price)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    item.name = request.form.get('name')
    item.description = request.form.get('description')
    item.price = float(request.form.get('price'))
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
