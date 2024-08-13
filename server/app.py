#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# class All_Restaurants(Resource):
#     def get(self):
#         ar = Restaurant.query.all()
#         return[rest.to_dict(rules=('-restaurantpizzas')) for rest in ar]

class All_Restaurants(Resource):
    def get(self):
        sc = Restaurant.query.all()
        return [rants.to_dict(rules = ('-restaurant_pizzas',)) for rants in sc],200
api.add_resource(All_Restaurants,'/restaurants')
#add rules so that it shows up the same way 
class T_Restaurants(Resource):
    def get(self,id):
        one_rest = Restaurant.query.filter(Restaurant.id == id).first()
        if one_rest:
            return one_rest.to_dict(),200
        else:
            return{
                "error": "Restaurant not found"
            },404
    def delete(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id==id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {},204
        else:
            return {
                    "error": "Restaurant not found"
                    }, 404

        # restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        # if restaurant:
        #     db.session.delete(restaurant)
        #     db.session.commit()
        #     return {},204
        # else:
        #     return{
        #         "error": "Restaurant not found"
        #     },404
api.add_resource(T_Restaurants,'/restaurants/<int:id>')

# class All_Pizza(Resource):
#     def get(self):
#         ap = Pizza.query.all()
#         return[piza.to_dict for piza in ap],200
class All_Pizza(Resource):
    def get(self):
        ap = Pizza.query.all()
        p_l = []
        for piza in ap:
            p_l.append(piza.to_dict(rules= ('-restaurant_pizzas',)))
        return p_l,200

api.add_resource(All_Pizza,'/pizzas')
class Rest_Pizza(Resource):
    def post(self):
        try:
            data = request.get_json()
            rp = RestaurantPizza(
                price = data['price'],
                pizza_id = data['pizza_id'], 
                restaurant_id = data['restaurant_id']
            )
            db.session.add(rp)
            db.session.commit()
            return rp.to_dict(),201
        except Exception as e:
            return{
                "errors": ["validation errors"]
            },400
api.add_resource(Rest_Pizza,'/restaurant_pizzas')
if __name__ == "__main__":
    app.run(port=5555, debug=True)
