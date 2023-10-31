# ontopito

## prerequirements

1. Run "pip install -r requirements.txt" to install the required libraries in python
2. Run "sudo apt-get install python3-tk" to install tkinter in your system
3. Download the reference BFO ontology from https://github.com/BFO-ontology/BFO/blob/master/bfo_classes_only.owl and move it in the current directory
4. Acquire your own Bioportal api-key from https://bioportal.bioontology.org/account by creating your own account

How to run this program:
```ruby
python3 main.py -i INP -o OUT -n NCPU -a API -t "TERMS"
```

- \-i: is for the input ontology in owl format
- \-o: is for the name of the output ontology (default:'output.owl')
- \-n: is for the number of cpu threads that you would like to use for this program (default:1)
- \-a: is for your own personal api-key in Bioportal
- \-t: is for apposing the desired terms. The terms should be comma seperated and in quatation marks if they are more than one (e.g. "Father,Student")

example:
```ruby
python3 main.py -i input_ontology.owl -o output_ontology.owl -n 6 -a (use here your own api-key) -t Human
```
or with multiple terms:

```ruby
python3 main.py -i input_ontology.owl -o output_ontology.owl -n 6 -a (use here your own api-key) -t "Father,Student"
```
