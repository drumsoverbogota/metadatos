from mongoengine import *

class Corpus(Document):
    nombre = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())

class Tag(Document):
    nombre = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())
    corpus = ReferenceField(Corpus)
    meta = {'allow_inheritance': True}

class Subtag(Tag):
    ptag = ReferenceField(Tag)