import wikitextparser as wtp
import os
import re
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from requests.utils import requote_uri

ARTICLES_PATH = 'Articles/'

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ").replace('"', " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

def is_link(v):
    linkregex = r'\[\[.*\]\]'
    return re.match(linkregex, v) is not None

def get_link(v):
    a=v
    clean = re.match(r'(\[\[((?!\[).)*\]\])(.*)', v).group(1)
    wl = wtp.WikiLink(clean)
    return wl.title

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
        for i in self.integrantes:
            list.append(('integrante', i))
        for i in self.especie:
            list.append(('especie', i))
        for i in self.edad:
            list.append(('edad', i))
        for i in self.nacimiento:
            list.append(('nacimiento', i))
        for i in self.nacionalidad:
            list.append(('nacionalidad', i))
        for i in self.ocupacion:
            list.append(('ocupacion', i))
        for i in self.especialidad:
            list.append(('especialidad', i))
        for i in self.afiliaciones:
            list.append(('afiliacion', i))
        for i in self.residencia:
            list.append(('residencia', i))
        for i in self.aficiones:
            list.append(('aficion', i))
        for i in self.logros:
            list.append(('logro', i))
        
        for i in self.amigos:
            list.append(('amigo', i))
        for i in self.enemigos:
            list.append(('enemigo', i))
        for i in self.familia:
            list.append(('familia', i))
        for i in self.pareja:
            list.append(('pareja', i))
        for i in self.mascotas:
            list.append(('mascota', i))
        for i in self.lider:
            list.append(('lider', i))
        for i in self.guiaespiritual:
            list.append(('guiaEspiritual', i))
        for i in self.discipulos:
            list.append(('discipulo', i))
        
        for i in self.cancion:
            list.append(('cancion', i))
        for i in self.album:
            list.append(('album', i))
        for i in self.top:
            list.append(('top', i))
        
        for i in self.voces:
            list.append(('voz', i))
        
        for i in self.primera_aparicion:
            list.append(('primera_aparicion', i))
        for i in self.ultima_aparicion:
            list.append(('ultima_aparicion', i))
        for i in self.primera_vacaciones:
            list.append(('primera_vacaciones', i))
        for i in self.ultima_vacaciones:
            list.append(('ultima_vacaciones', i))
        return iter(list)
    
    def to_graph(self, graph):
        nodename = to_camel_case(self.nombre)
        print("to_graph: {}".format(nodename))
        for k,v in self:
            if(is_link(v)):
                o = URIRef(to_camel_case(get_link(v)))
                print("\tFound a link: {}".format(o))
            else:
                o = Literal(v, datatype=XSD.string)
            
            
            graph.add((URIRef(nodename),
                       URIRef(k),
                       o))
        
def get_arg(template, arg):
    if template.has_arg(arg):
        value = template.get_arg(arg).value.replace("<nowiki>","").replace("</nowiki>","").strip()
        value = re.split('<br/>|<br>|\n', value)
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
    pj.ultima_aparicion = get_arg(template, 'última_aparición')
    pj.primera_vacaciones = get_arg(template, 'primera_vacaciones')
    pj.ultima_vacaciones = get_arg(template, 'última_vacaciones')
                
    return pj            
    



def create_pj_graph():
    g = Graph()

    ##borre las carpetas para no tener problemas
    fileList = os.listdir(ARTICLES_PATH)
    for filename in fileList:
        with open(ARTICLES_PATH+filename, "r") as f:
            parsed = wtp.parse(f.read())
            templates = parsed.templates
            for template in templates:
                if(template.name.strip() == 'Fichapersonaje'):
                    nombre = f.name.replace(".txt","").replace(ARTICLES_PATH,"")
                    pj = serialize_pj(nombre, template)
                    pj.to_graph(g)
                
                

    g.serialize(destination='graph.ttl', format='turtle')

if __name__ == '__main__':
    create_pj_graph()
