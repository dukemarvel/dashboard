from mongoengine import Document, IntField, FloatField, StringField

class EquityData(Document):
    account_id = IntField(required=True)
    equity = FloatField(required=True)
    balance = FloatField(required=True)
    timestamp = StringField(required=True)
