from mongoengine import *
from corpus.models import *


class Sesiones(Document):
    tags = DictField()
    refa = DictField()
    corpus = ReferenceField(ModeloCorpus)

class Anidados(Document):
    tags = DictField()
    corpus = ReferenceField(ModeloCorpus)
    ref = ReferenceField(Tag)