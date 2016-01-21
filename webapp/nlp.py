import nltk
import re
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from pprint import pprint

class Entity(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.id = 0
        self.sensitivity = "Medium"

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
    for subtree in  sentt.subtrees(filter=lambda t: t.label() != None):
        if subtree.label() == "PERSON":
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 0:
                for part in person:
                    name += part + ' '
                #if name[:-1] not in person_list:
                entities.append(Entity(name[:-1], "Person"))
                person_list.append(name[:-1])
                name = ''
        person = []
        if subtree.label() == "ORGANIZATION":
            for leaf in subtree.leaves():
                organization.append(leaf[0])
            if len(organization) > 0:
                for part in organization:
                    name += part + ' '
                #if name[:-1] not in organization_list:
                entities.append(Entity(name[:-1], "Organization"))
                organization_list.append(name[:-1])
                name = ''
        organization = []
        if subtree.label() == "GPE":
            for leaf in subtree.leaves():
                gpe.append(leaf[0])
            if len(gpe) > 0:
                for part in gpe:
                    name += part + ' '
                #if name[:-1] not in gpe_list:
                entities.append(Entity(name[:-1], "Geo Entity"))
                gpe_list.append(name[:-1])
                name = ''
        gpe = []

    dates = []
    dates = re.findall(r'(\d{2}[/.-]\d{2}[/.-]\d{4})', text)
    for date in dates:
        entities.append(Entity(date, "Date"))
    dates = []
    dates = re.findall(r'(\d{4}[/.-]\d{2}[/.-]\d{2})', text)
    for date in dates:
        entities.append(Entity(date, "Date"))
    dates = []
    dates = re.findall(r'\d\d\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z]{0,6}\s\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z]{0,6}\s\d{2,4}', text, re.IGNORECASE)
    for date in dates:
        entities.append(Entity(date, "Date"))
    times = []
    times = re.findall(r'([0-2][0-9]:[0-5]\d)', text)
    for time in times:
        entities.append(Entity(time, "Time"))
    phones = []
    phones = re.findall(r'([0-9]{3}-[0-9]{3}-[0-9]{4})', text)
    for phone in phones:
        entities.append(Entity(phone, "Phone"))
    emails = []
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]', text)
    for email in emails:
        entities.append(Entity(email, "Email Id"))

    for entity in entities:
        offset = text.find(entity.name)
        text = text.replace(entity.name, "*"*len(entity.name), 1)
        entity.id = offset

    entities.sort(key=lambda x: x.id)

    return entities
