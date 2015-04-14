from mongoengine import *

class Corpus(Document):
    nombre = StringField(max_length=120, required=True)
    descripcion = StringField(max_length=300)

class Tag(Document):
    tag = StringField()
    descripcion = StringField()
    corpus = ReferenceField(Corpus)

class Subtag(Document):
    subtag = StringField()
    descripcion = StringField()
    tag = ReferenceField(Tag)