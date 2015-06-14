from mongoengine import *

class ModeloCorpus(Document):
    nombre = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())

    n_tag = StringField()
    main = StringField()

class BaseTag(Document):
    nombre = StringField()
    main_tag = StringField()
    tags = ListField(StringField())
    tags_f = ListField(StringField())
    meta = {'allow_inheritance': True}

class Tag(BaseTag):
    corpus = ReferenceField(ModeloCorpus)

class Subtag(BaseTag):
    ptag = ReferenceField(BaseTag)
    corpus = ReferenceField(ModeloCorpus)