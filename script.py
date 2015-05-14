from mongoengine import *
from corpus.models import *
from archivos.models import *
import csv

connect('gestion')

nombre = 'test'


with open('sesiones.csv', encoding='utf16') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    i = 0
    headers = []
    tags = []
    a_tags = []
    for row in spamreader:
        if i == 0:
            i+=1
            headers = row
            for col in row:
                if col.startswith('Id') and not col=='Id':
                    a_tags.append(col)
                else:
                    tags.append(col)

            print('Documentos')
            print(tags)
            print(a_tags)
            mod = ModeloCorpus(nombre=nombre,tags=tags)
            mod.save()
            for a in a_tags:
                print(a)
                with open(a[2:]+'.csv', encoding='utf16') as s_csvfile:
                    s_spamreader = csv.reader(s_csvfile, delimiter='\t', quotechar='|')
                    i = 0
                    s_headers = []
                    s_tags = []
                    for s_row in s_spamreader:
                        if i == 0:
                            i=+1
                            s_headers = s_row
                            for col in s_row:
                                s_tags.append(col)
                    print(s_tags)
                    tag = Tag(nombre=a[2:],main_tag=s_row[0],tags=s_tags,corpus=mod)
                    tag.save()
        #else:





