from mongoengine import *

class Corpus(Document):
    nombre = StringField(max_length=120, required=True)

class Tag(Document):
    tag = StringField()
    descripcion = StringField()
    corpus = ReferenceField(Corpus)

