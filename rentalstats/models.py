import mongoengine as db

connect(os.environ.get('MONGOHQ_DB', 'default'), os.environ.get('MONGOHQ_URL', 'localhost'))

class Listing(db.Document):
    url = db.URLField()
    title = db.StringField()
    price = db.IntField()
    time = db.DateTimeField(default=datetime.datetime.now)
    neighborhood = db.StringField()
    bedrooms = db.IntField()
