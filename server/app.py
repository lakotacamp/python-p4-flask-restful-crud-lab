#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# - Making a PATCH request to this route with an object in the body should update one
#   plant, and return the updated plant in the response
# - Making a DELETE request to this route should delete one plant from the database.
#   You should return a response of an empty string with the status code 204 (No Content)
#   to indicate a successful deletion.
class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

    def patch(self,id):
        record = Plant.query.filter_by(id=id).first()
        data = request.get_json()
        for attr in data:
            setattr(record, attr, data[attr])
        db.session.add(record)
        db.session.commit()
        return make_response(record.to_dict(),200)
    
    def delete(self,id):
        record = Plant.query.filter_by(id=id).first()
        db.session.add(record)
        db.session.commit()
        response_dict = {"message":"plant deleted"}
        return make_response(response_dict, 204)

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
