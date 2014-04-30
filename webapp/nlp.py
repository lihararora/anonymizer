import nltk
import re
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from pprint import pprint

class Entity(object):
    def __init__(self, name, type, id, sensitivity):
        self.name = name
        self.type = type
        self.id = id
        self.sensitivity = sensitivity

def get_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    entities = []
    person_list = []
    person = []
    organization_list = []
    organization = []
    gpe_list = []
    gpe = []
    name = ""
    id = 0
    for subtree in  sentt.subtrees(filter=lambda t: t.node != None):
        print id
        print subtree
        if subtree.node == "PERSON":
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 0:
                for part in person:
                    name += part + ' '
                #if name[:-1] not in person_list:
                id = id + 1
                entities.append(Entity(name[:-1], "Person", id, 0))
                person_list.append(name[:-1])
                name = ''
        person = []
        if subtree.node == "ORGANIZATION":
            for leaf in subtree.leaves():
                organization.append(leaf[0])
            if len(organization) > 0:
                for part in organization:
                    name += part + ' '
                #if name[:-1] not in organization_list:
                id = id + 1
                entities.append(Entity(name[:-1], "Organization", id, 0))
                organization_list.append(name[:-1])
                name = ''
        organization = []
        if subtree.node == "GPE":
            for leaf in subtree.leaves():
                gpe.append(leaf[0])
            if len(gpe) > 0:
                for part in gpe:
                    name += part + ' '
                #if name[:-1] not in gpe_list:
                id = id + 1
                entities.append(Entity(name[:-1], "Geo Entity", id, 0))
                gpe_list.append(name[:-1])
                name = ''
        gpe = []
        
    dates = []
    dates = re.findall(r'(\d{2}[/.-]\d{2}[/.-]\d{4})', text)
    for date in dates:
        id = id + 1
        entities.append(Entity(date, "Date", id, 0))
    dates = []
    dates = re.findall(r'(\d{4}[/.-]\d{2}[/.-]\d{2})', text)
    for date in dates:
        id = id + 1
        entities.append(Entity(date, "Date",id , 0))    
    return entities