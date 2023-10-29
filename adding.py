import requests
from owlready2 import *#https://pypi.org/project/owlready2/
import shutil
import sys
from bs4 import BeautifulSoup
from tools import window
from definition import run_bioportal

def get_annotation(api_key,term,task,onto_ontologies):
    choosing_def=[]
    choosing_iri=[]
    #bioportal
    url=f"https://data.bioontology.org/annotator?apikey={api_key}&text={term.replace('_','%20')}"
    datas = requests.get(url).json()
    #bioportal
    
    #obo
    url_obo=f"https://ontobee.org/search?ontology=&keywords={term.replace('_','+')}&submit=Search+terms"
    print(url_obo)
    datas_obo = requests.get(url_obo).text
    soup_obo = BeautifulSoup(datas_obo,"html.parser")
    result_obo = soup_obo.find_all(class_="search-list")
    #obo

    #bioportal
    choosing_def,choosing_iri,choosing_ontology = run_bioportal(datas,api_key,term,False,task)

    #obo
    for pick in result_obo:
        bar_length = 20
        current = int(round((result_obo.index(pick)/len(result_obo)),2)*bar_length)
        left = bar_length - current
        print(f"loading: [{'*'*current}{' '*left}]",end="\r")
        b = pick.find_all("ul")[0].find_all("li")
        for i in b:
            result_term = i.text.strip().replace("  ","__").split("__")[0].lower() 
            if term.lower() == result_term:
                iri = [a['href'] for a in pick.find_all('a')][0]
                opened_iri = requests.get(iri).text
                opened_iri_soup = BeautifulSoup(opened_iri,'xml').text.split("\n")

                while("" in opened_iri_soup):
                    opened_iri_soup.remove("")

                try:
                    definition = [item for item in opened_iri_soup if item.endswith('.')][0].replace("<p>","").replace("</p>"),""
                    if definition in choosing_def:
                        continue
                    else:          
                        choosing_def.append(definition)
                        choosing_iri.append(iri)
                except Exception:
                    continue

    #result
    if choosing_def ==[]:
        print()
        print()
        print(f'There is no definition of "{term}" in the database')
        print()
        return 0
    #skiparei afta me ton ena orismo
    #elif len(choosing_def)==1:#exei mono ena definition
    #    print()
    #    print(f'There is a single definition: "{a}"')
    #    print()
    #    a = f"{choosing_def[0]} ({choosing_iri[0]})"
    #    return a
    else:
        used_ontologies_index = []
        for i in range(len(choosing_ontology)):
            if choosing_ontology in onto_ontologies:
                used_ontologies_index.append(i)
        pos,definition = window(choosing_def,(f'''"{term}" isn't in your ontology'''),used_ontologies_index,add_button=True)
        if definition:
            if pos <= len(choosing_def)-1:
                return f"{definition} ({choosing_iri[pos]})"
            else:
                return definition
        else:
            return f"{choosing_def[pos]} ({choosing_iri[pos]})"
