# ontopito
##prerequirements
1. Run "pip install -r requirements.txt" to install the required libraries in python
2. Run "sudo apt-get install python3-tk" to install tkinter in your system
3. Download the reference BFO ontology from https://github.com/BFO-ontology/BFO/blob/master/bfo_classes_only.owl and move it in the current directory
4. Acquire your own Bioportal api-key from https://bioportal.bioontology.org/account by creating your own account

How to run:
You can run this program by using this command in the terminal:
```ruby
./main.py -i INP [-o [OUT]] [-n [NCPU]] -a API -t [TERMS ...]
```

- \-i: is for the input ontology in owl format
- \-o: is for the name of the output ontology (default:'output.owl')
- \-n: is for the number of cpu threads that you would like to use for this program (default:1)
- \-a: is for your own personal api-key in Bioportal
- \-t: is for apposing the desired terms. The terms should be comma seperated and in quatation marks if they are more than one (e.g. "Father,Student")

example:
```ruby
/main.py -i bfo_classes_only.owl -n 6 -a 1b1cc837-edf0-4d4b-89e6-f19449b03abf -t Human
```
