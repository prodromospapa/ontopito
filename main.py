#!/usr/bin/python3

import argparse
from definition import run_bioportal
from ancestry import run
from owlready2 import *
from tools import window
import shutil
import requests

parser=argparse.ArgumentParser(description="Get the initial owl file with the BFO terms from: https://github.com/BFO-ontology/BFO/blob/master/bfo_classes_only.owl")
parser.add_argument("-i","--inp",type=str, nargs=1,required=True,help="Input file")
parser.add_argument("-o","--out",type=str,nargs="?",required=False,default="output.owl",help="Output file (default:'output.owl')")
parser.add_argument("-t","--terms",type=str,nargs="*",required=True,help='Your terms. The terms should be comma seperated and in quatation marks if they are more than one (e.g. "Father,Student")')
parser.add_argument("-n","--ncpu",type=int,nargs="?",required=False,default=1,help="Set number of threads to be used (default:1)")
parser.add_argument("-a","--api", type=str,nargs=1,required=True,help="Your api in bioportal (get it from: https://bioportal.bioontology.org/account)")

args=parser.parse_args()

task = args.ncpu#number of processors

terms = args.terms[0].split(",")
terms = [i.strip() for i in terms]
api_key = args.api[0]
#api_key = open("ontopipis/api.txt").read().strip()
new_added=[]
if args.inp[0] != args.out:#ama exei orous me idia parental prepei na ksanafortwsei thn ontologia sto ancestry
    shutil.copyfile(args.inp[0], args.out)

for term in terms:
    onto=get_ontology(args.out).load() #prepei na fortwnei kathe fora thn ananewmena terms
    onto_terms_list = list(onto.classes())
    onto_terms = []
    onto_ontologies = []
    for i in onto_terms_list:
        onto_terms.append(str(i.label[0]))
        try:
            onto_ontologies.append(i.comment[0])
        except:
            continue
    if term.lower() not in [i.lower() for i in onto_terms]:
        try:
            #definitions
            url_bio=f"https://data.bioontology.org/annotator?apikey={api_key}&text={term.replace(' ','%20')}"     
            datas = requests.get(url_bio).json()
            choosing_def,choosing_iri,choosing_ancestors,choosing_ontology = run_bioportal(datas,api_key,term,True,task,onto_terms)
            
            #find ontology that I have used
            used_ontologies_index = []
            for i in range(len(choosing_ontology)):
                if choosing_ontology[i] in onto_ontologies:
                    used_ontologies_index.append(i)
            can_add = 0
            new_added.append(term)
            if choosing_def == []:
                print(f'''can't find your term "{term}"''')
                new_added.pop(-1)
                break            
            #definition pick
            pos,definition = window(choosing_def,(f'Definition for "{term}"'),used_ontologies_index,add_button=False)
            if definition:
                picked = [definition]
            else:
                picked = [choosing_def[pos]]

            picked += [choosing_iri[pos],choosing_ancestors[pos],choosing_ontology[pos]]

            definition = picked[0] + f"({picked[1]})"
            ancestors = picked[2]
            ontology_name = picked[3]

            del choosing_def[pos]
            del choosing_iri[pos]
            del choosing_ancestors[pos]
            del choosing_ontology[pos]

            #tree build
            can_add = run(term,ancestors,api_key,definition,onto_terms,args.out,task,ontology_name,onto_ontologies)
        except Exception as e:
            print(e)
            new_added.pop(-1)
            print(f'''Can't add "{term}"'''+" "*20)
            continue
    else:
        print(f'"{term}" already exists'+" "*20)
print(f"{new_added} have been added" + " "*7)


