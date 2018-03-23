from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every store needs an ID"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
#        return item.json()

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # The lines below will be replaced with SQLAlchemy shorter lines;
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}
#        connection = sqlite3.connect('data.db')
#        cursor = connection.cursor()
#        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
#        cursor.execute(query, (name,))

#        connection.commit()
#        connection.close()

#        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
# updated_item = ItemModel(name, data['price']) # remove due to SQLAlchemy
        if item is None:
            # replace due to SQLAlchemy
            #            item = ItemModel(name, data['price'], data['store_id'])
            # above line can be simplified with **data
            item = ItemModel(name, **data)
    #        try:
    #            updated_item.insert()
    #        except:
    #            return {"message": "An error occurred inserting the item."}
        else:
            # REplace due to SQLAlchemy

            item.price = data['price']

        item.save_to_db()
#            try:
#                updated_item.update()
#            except:
#                return {"message": "An error occurred updating the item."}
#        return updated_item.json()
        return item.json()


class ItemList(Resource):
    #    TABLE_NAME = 'items'

    def get(self):
        # all_items = []
        # items = ItemModel.query.all()
        # for item in items:
        #     all_items.append(item.json())
        # return all_items
        # You can use list comprehension
        #        return {'items in database': [item.json() for item in ItemModel.query.all()]}
        # OR you can also use lamda function
        return {'items in database': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # replace bleow by above lines
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[1], 'price': row[2]})
        # connection.close()
        #
        # return {'items': items}
