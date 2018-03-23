from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
#        return item.json()

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        # The lines below will be replaced with SQLAlchemy shorter lines;
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Item deleted"}


class StoreList(Resource):
    #    TABLE_NAME = 'items'

    def get(self):
        # You can use list comprehension
        #        return {'items in database': [item.json() for item in ItemModel.query.all()]}
        # OR you can also use lamda function
        return {'stores in database': list(map(lambda x: x.json(), StoreModel.query.all()))}
