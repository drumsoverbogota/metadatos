from mongoengine import *

class ModeloCorpus(Document):
    nombre = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())

class Tag(Document):
    nombre = StringField()
    main_tag = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())
    corpus = ReferenceField(ModeloCorpus)
    meta = {'allow_inheritance': True}

class Subtag(Tag):
    ptag = ReferenceField(Tag)