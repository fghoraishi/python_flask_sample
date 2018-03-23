from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

        #        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):

        # All lines below can be replaced with SQLAlcheym line below
        return cls.query.filter_by(name=name).first()
#        connection = sqlite3.connect('data.db')
#        cursor = connection.cursor()
    #    query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
#        query = "SELECT * FROM items WHERE name=?"
#        result = cursor.execute(query, (name,))
#        row = result.fetchone()
#        connection.close()
#        if row:
        #            return cls(row[0], row[1])
        # Simpler line from above line is this:
#            return cls(*row)

#    def insert(self):
        # All lines below can be replaced with SQLAlcheym line below
    def save_to_db(self):  # SQLAlchemy replaces both insert and update....
        db.session.add(self)
        db.session.commit()
#       connection = sqlite3.connect('data.db')
#        cursor = connection.cursor()

#        query = "INSERT INTO items VALUES(?, ?)"
#        cursor.execute(query, (self.name, self.price))

#        connection.commit()
#        connection.close()

#    def update(self):   # With SQLAlchemy we reuse update to Delete sinc update is taken care above
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
#        connection = sqlite3.connect('data.db')
#        cursor = connection.cursor()

#        query = "UPDATE items SET price=? WHERE name=?"
#        cursor.execute(query, (self.price, self.name))

#        connection.commit()
#        connection.close()
