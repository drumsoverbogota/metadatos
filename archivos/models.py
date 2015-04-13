from mongoengine import *
from corpus.models import *


class Archivo(Document):
    archivo = StringField()
    tags = DictField()
    corpus = ReferenceField(Corpus)