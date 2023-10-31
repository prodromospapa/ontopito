# ontopito

## prerequirements

1. To install the required libraries in python run:
```ruby
pip install -r requirements.txt
```
2. To install tkinter in your system run:
```ruby
sudo apt-get install python3-tk
```
3. Download the reference BFO ontology from https://github.com/BFO-ontology/BFO/blob/master/bfo_classes_only.owl 
4. Acquire your own Bioportal api-key from https://bioportal.bioontology.org/account by creating your own account

How to run this program:
```ruby
python3 main.py -i INP -o OUT -n NCPU -a API -t TERMS
```

- \-i: name of the input ontology
- \-o: name of the output ontology (default:'output.owl')
- \-n: number of cpu threads that you would like to use for this program (default:1)
- \-a: your own personal api-key in Bioportal
- \-t: for apposing the desired terms. The terms should be comma seperated and in quatation marks if they are more than one (e.g. "Father,Student")

examples:

with one term:
```ruby
python3 main.py -i input_ontology.owl -o output_ontology.owl -n 6 -a (your api-key) -t Human
```
with multiple terms:

```ruby
python3 main.py -i input_ontology.owl -o output_ontology.owl -n 6 -a (your api-key) -t "Father,Student"
```
