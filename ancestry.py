import requests
import types
from owlready2 import *
from adding import get_annotation
from tkinter.simpledialog import askstring
import tkinter as tk

def create_ancestry(term,ancestry_url,api_key,definition,onto_terms,output,task,ontology_name,onto_ontologies):
    onto=get_ontology(output).load()
    ancestry=ancestry_url   
    ancestry=requests.get(ancestry+f"?apikey={api_key}").json() #removes parent term
    ancestor_details={anc['prefLabel']:[anc['definition'],anc['@id']] for anc in ancestry}
    terms=list(ancestor_details.keys())
    terms=[i.replace("_"," ") for i in terms]
    childs = [term]
    parent=""

    for i in terms:
        if i.lower() in onto_terms:
            parent = i
            break
        else:
            childs.append(i)
    childs = childs[::-1]
    for checking_format in [parent.title(),parent.lower(),parent.upper()]:
        onto_parent = onto.search(label = checking_format)
        if onto_parent:
            parent = checking_format

    if parent=="":
        return 0

    for child in childs[:-1]:
        child_def = ancestor_details[child][0]
        if child_def==[]:
            child_def = get_annotation(api_key,child,task,onto_ontologies)
            if child_def == 0:
                child_def = askstring("Set definition", f'''Can't find definition for "{child}"''')               
        else:
            child_def = child_def[0]+ f"({ancestor_details[child][1]})"
        child = child.replace("_"," ")
        create_class(child,parent,child_def,onto,ontology_name)#vazei tous parental orous
        parent = child
        onto.save(output,format="rdfxml")    
    create_class(term,parent,definition,onto,ontology_name)#vazei ton oro mou
    onto.save(output,format="rdfxml")   
    return 1


def create_class(label,parent,definition,onto,ontology_name):
    with onto:
        Class=types.new_class(label,(onto.search_one(label=parent),)) #,namespace=onto
        Class.label = label
        Class.isDefinedBy=definition
        Class.comment=ontology_name
        sync_reasoner(onto)


def run(term,ancestry_url,api_key,definition,onto_terms,output,task,ontology_name,onto_ontologies):       
    if len(term):
        onto_terms = [i.lower() for i in onto_terms]
        checking = create_ancestry(term,ancestry_url,api_key,definition,onto_terms,output,task,ontology_name,onto_ontologies)
        return checking