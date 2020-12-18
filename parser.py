import wikitextparser as wtp
import os
import re
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from requests.utils import requote_uri

ARTICLES_PATH = 'Articles/'

class Personaje():
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        rep = "{}: {}".format(self.nombre, self.familia)
        return rep

    def __iter__(self):
        list = []
        for i in self.nombre_real:
            list.append(('nombre_real', i))
        for i in self.apodos:
            list.append(('apodo', i))
        for i in self.especie:
            list.append(('especie', i))
        for i in self.amigos:
            list.append(('amigo', i))
        return iter(list)
    
    def to_graph(self, graph):
        nodename = requote_uri(self.nombre)
        for k,v in self:
            graph.add((URIRef(nodename),
                       URIRef(k),
                       Literal(v, datatype=XSD.string)))
        
def get_arg(template, arg):
    if template.has_arg(arg):
        value = template.get_arg(arg).value.replace("<nowiki>","").replace("</nowiki>","").strip()
        value = re.split('<br/>|<br>', value)
        if value != "": return value
    return []

def serialize_pj(nombre, template):
    pj = Personaje(nombre)
    pj.nombre_real = get_arg(template, 'nombre_real')
    pj.apodos = get_arg(template, 'apodos')
    pj.integrantes = get_arg(template, 'integrantes')
    pj.especie = get_arg(template, 'especie')
    pj.edad = get_arg(template, 'edad')
    pj.nacimiento = get_arg(template, 'nacimiento')
    pj.nacionalidad = get_arg(template, 'nacionalidad')
    pj.ocupacion = get_arg(template, 'ocupacion')
    pj.especialidad = get_arg(template, 'especialidad')
    pj.afiliaciones = get_arg(template, 'afiliaciones')
    pj.residencia = get_arg(template, 'Residencia')
    pj.aficiones = get_arg(template, 'aficiones')
    pj.logros = get_arg(template, 'logros')

    # Relaciones
    pj.amigos = get_arg(template, 'amigos')
    pj.enemigos = get_arg(template, 'enemigos')
    pj.familia = get_arg(template, 'familia')
    pj.pareja = get_arg(template, 'pareja')
    pj.mascotas = get_arg(template, 'mascotas')
    pj.lider = get_arg(template, 'líder')
    pj.guiaespiritual = get_arg(template, 'guíaespiritual')
    pj.discipulos = get_arg(template, 'discípulos')
    
    # Información musical
    pj.cancion = get_arg(template, 'cancion')
    pj.album = get_arg(template, 'album')
    pj.top = get_arg(template, 'top') #Episodio donde es #1
    
    # Producción
    pj.voces = get_arg(template, 'voces')
    # Apariciones
    pj.primera_aparicion = get_arg(template, 'primera_aparición')
    pj.ultima_aparición = get_arg(template, 'última_aparición')
    pj.primera_vacaciones = get_arg(template, 'primera_vacaciones')
    pj.ultima_vacaciones = get_arg(template, 'última_vacaciones')
                
    return pj            
    

g = Graph()

##borre las carpetas para no tener problemas
fileList = os.listdir(ARTICLES_PATH)
for file in fileList:
    with open(ARTICLES_PATH+file, "r") as file:
        parsed = wtp.parse(file.read())
        templates = parsed.templates
        for template in templates:
            if(template.name == 'Fichapersonaje'):
                nombre = file.name.replace(".txt","").replace(ARTICLES_PATH,"")
                pj = serialize_pj(nombre, template)
                pj.to_graph(g)
                

g.serialize(destination='graph.ttl', format='turtle')


