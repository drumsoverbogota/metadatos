from mongoengine import *
from corpus.models import *
from archivos.models import *
import csv

db = connect('gestion')
db.drop_database('test')

nombre = 'ALEC'


def createSubtags(tags,tag):
    
    print(tags)
    for b in tags:
        with open('../'+b[2:]+'.csv', encoding='utf16') as s_csvfile:
            s_spamreader = csv.reader(s_csvfile, delimiter='\t', quotechar='|')
            i = 0
            s_headers = []
            s_tags = []
            s_a_tags = []
            n_tag = None
            for s_row in s_spamreader:
                if i == 0:
                    i=+1
                    s_headers = s_row
                    for col in s_row:
                        if col.startswith('Id') and not col=='Id':
                            s_a_tags.append(col)
                        else:
                            s_tags.append(col)
                    n_tag = Subtag(nombre=b[2:],main_tag=s_headers[0],tags=s_tags,ptag=tag)
                    n_tag.save()
                    if len(s_a_tags) > 0:
                        createSubtags(s_a_tags,n_tag)
                else:


                    d = {}
                    anidados = Anidados(corpus=mod,ref=n_tag)
                    for f, b in zip(s_headers, s_row):
                        if not f.startswith('Id') or f=='Id':
                            d[f] = b
                        else:
                            nombre = f[2:]
                            dest = Subtag.objects(nombre=nombre)[0].id
                            for a in Anidados.objects(ref=dest):
                                if a.tags["Id"] == b:
                                    if nombre not in anidados.refa.keys():
                                        anidados.refa[nombre] = []
                                    anidados.refa[nombre].append(a.id)
                            anidados.tags = d
                            anidados.save()
            #print(s_tags)



with open('../Fragmentos.csv', encoding='utf16') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    i = 0
    headers = []
    tags = []
    a_tags = []
    mod = None
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
            mod = ModeloCorpus(nombre=nombre,tags=tags)
            mod.save()
            for a in a_tags:
                #print(a)
                with open('../'+a[2:]+'.csv', encoding='utf16') as s_csvfile:
                    s_spamreader = csv.reader(s_csvfile, delimiter='\t', quotechar='|')
                    j = 0
                    s_headers = []
                    s_tags = []
                    s_a_tags = []
                    for s_row in s_spamreader:
                        if j == 0:
                            j=+1
                            s_headers = s_row
                            for col in s_row:
                                if col.startswith('Id') and not col=='Id':
                                    s_a_tags.append(col)
                                else:
                                    s_tags.append(col)
                            tag = Tag(nombre=a[2:],main_tag=s_headers[0],tags=s_tags,corpus=mod)
                            tag.save()
                            if len(s_a_tags) > 0:
                                createSubtags(s_a_tags,tag)
                            
                        else:
                            d = {}
                            anidados = Anidados(corpus=mod,ref=tag)
                            for f, b in zip(s_headers, s_row):
                                if not f.startswith('Id') or f=='Id':
                                    d[f] = b
                                else:
                                    nombre = f[2:]
                                    dest = Subtag.objects(nombre=nombre)[0].id
                                    for a in Anidados.objects(ref=dest):
                                        if a.tags["Id"] == b:
                                            if nombre not in anidados.refa.keys():
                                                anidados.refa[nombre] = []
                                            anidados.refa[nombre].append(a.id)
                            anidados.tags = d
                            anidados.save()
    

        else:
            t = {}
            sesion = Sesiones(corpus=mod)
            for f, b in zip(headers, row):
                if not f.startswith('Id') or f=='Id':
                    t[f] = b
                else:
                    nombre = f[2:]
                    dest = Tag.objects(nombre=nombre)[0].id
                    for a in Anidados.objects(ref=dest):
                        if a.tags["Id"] == b:
                            if nombre not in sesion.refa.keys():
                                sesion.refa[nombre] = []
                            sesion.refa[nombre].append(a.id)
            sesion.tags = t
            sesion.save()
#else:
