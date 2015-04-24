from mongoengine import *
from corpus.models import *


class Sesiones(Document):
    id = StringField(max_length=120, required=True)
    tags = DictField()
    corpus = ReferenceField(Corpus)