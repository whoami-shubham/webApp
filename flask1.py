from flask import Flask, render_template, url_for, request, redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db', pool_pre_ping=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)


app = Flask(__name__)

@app.route('/')
def Home():
    return '<h1>hello world</h1>'

@app.route('/restaurants/<int:restaurant_id>/', methods=['GET','POST'])
def HelloWorld(restaurant_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)      
    return render_template('restaurant.html',restaurant=restaurant,item=item)
    

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newDish(restaurant_id):
    if request.method == 'POST':
        session = DBSession()
        n = session.query(MenuItem).filter_by(name=request.form['name']).first()
        if n:
            flash('Dish is Already present !')
            return redirect(url_for('HelloWorld',restaurant_id=restaurant_id))
        newd= MenuItem(name=request.form['name'],description=request.form['des'],price=request.form['pri'],restaurant_id=restaurant_id)
        session.add(newd)
        session.commit()
        flash('New Dish Added !')
        return redirect(url_for('HelloWorld',restaurant_id=restaurant_id))
    else:
        return render_template('new.html',restaurant_id=restaurant_id)


@app.route('/editdish/<int:restaurant_id>/<int:menu_id>/', methods=['GET','POST'])
def editDish(restaurant_id,menu_id):
    session = DBSession()
    i = session.query(MenuItem).filter_by(id=menu_id).first()
    if request.method == 'POST':
        if dish:
            n= request.form['name'] if request.form['name']!='' else dish.name
            p=request.form['pri']  if request.form['pri']!='' else dish.price
            d=request.form['des']  if  request.form['des']!='' else dish.description
            i.name = n
            i.price= p
            i.description=d
            session.add(i)
            session.commit()
            flash('Dish Edited !')
        return redirect(url_for('HelloWorld',restaurant_id=restaurant_id,menu_id=menu_id))
    return render_template('edit.html',restaurant_id=restaurant_id,menu_id=menu_id,i=i)
    
@app.route('/deletedish/<int:restaurant_id>/<int:menu_id>/', methods=['GET','POST'])
def deleteDish(restaurant_id,menu_id):
    session = DBSession()
    dish = session.query(MenuItem).filter_by(id=menu_id).first()
    if request.method == 'POST':
        if dish and request.form.get('y',None):
            session.delete(dish)
            session.commit()
            flash(' Dish Deleted !')
            return redirect(url_for('HelloWorld',restaurant_id=restaurant_id,menu_id=menu_id))
        flash(' No Dish  Deleted !')
        return redirect(url_for('HelloWorld',restaurant_id=restaurant_id,menu_id=menu_id))
    return render_template('delete.html',restaurant_id=restaurant_id,menu_id=menu_id,dish=dish)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.secret_key ='password'
    app.run(host='0.0.0.0', port=5000) 
