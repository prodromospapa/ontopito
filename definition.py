import requests
from owlready2 import *#https://pypi.org/project/owlready2/
import shutil
import sys
import multiprocessing
import threading

def run_bioportal(datas,api_key,term,term_def,task):
    if not len(datas):
        return [[],[],[]]
    #cpu check 
    n_cpus = os.cpu_count()
    if task > n_cpus:
        task = n_cpus

    if len(datas)<task:
        task = len(datas)
    lista = list(divide(datas,task))
    p = multiprocessing.Pool(task) 
    lista = [[i, term,api_key,term_def] for i in lista]
    res = p.map(export_data,lista)
    choosing_def=[]
    choosing_iri=[]
    choosing_ancestors=[]
    choosing_ontology=[]
    for i in range(len(res)):
        choosing_def+=res[i][0]
        choosing_iri+=(res[i][1])
        choosing_ontology+=(res[i][3])
        if term_def:
            choosing_ancestors+=(res[i][2])
    if term_def:
        return [choosing_def,choosing_iri,choosing_ancestors,choosing_ontology]
    else:
        return [choosing_def,choosing_iri,choosing_ontology]

def divide(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def words(input_string):    
    words = input_string.split()
    filtered_words = []

    for word in words:
        if len(word) <= 25:
            filtered_words.append(word)
    result_string = ' '.join(filtered_words)
    return result_string        

def export_data(a):
    datas = a[0]
    term = a[1]
    api_key = a[2]
    term_def = a[3]
    #general
    choosing_def=[]
    choosing_iri=[]
    choosing_ancestors=[]
    choosing_ontology=[]
    #general
    for data in datas:
        try:#kamia fora pernaei data pou den paizei
            bar_length = 20
            current = int(round((datas.index(data)/len(datas)),2)*bar_length)
            left = bar_length - current
            print(f"loading: [{'*'*current}{' '*left}]",end="\r")
            #print(f"loading Bioportal",end="\r")
            Class = data['annotatedClass']

            #check matching
            Annotations = data['annotations']
            Label=str(Annotations[0]['text'])
            if term.lower()!=Label.lower():#When an annotation doesn't match the text term fully
                continue

            #Find Basic data Information
            IRI=Class["@id"]

            #definition
            self_link = Class['links']['self']
            definition_html=requests.get(self_link+f"?apikey={api_key}").json()
            ontology = self_link.split("/")[4]

            try:#checks if there is definition site
                definition = definition_html["definition"]
                definition=definition[0].replace("<p>","").replace("</p>","")
            except Exception as e:
                continue

            if term_def:
                #ancestors
                ancestors = definition_html['links']["ancestors"]
            else:
                ancestors="pass"


            definition = words(definition)
            if definition=="" or ancestors=="" or (not term_def and definition in choosing_def):
                continue
            else:          
                choosing_def.append(definition)
                choosing_iri.append(str(IRI))
                choosing_ontology.append(ontology)
                if term_def:
                    choosing_ancestors.append(ancestors)
        except Exception:
            continue
    if term_def:
        return [choosing_def,choosing_iri,choosing_ancestors,choosing_ontology]
    else:
        return [choosing_def,choosing_iri,choosing_ontology]