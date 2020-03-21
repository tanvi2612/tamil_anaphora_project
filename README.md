main.py
________

Enter
```
python3 main.py filename
```  
to see output of code

The sentences fed must be POS tagged in the format

word1/POS_tag word2/POS_tag........

This program detects the pronoun to be resolved in a window on 3 sentences and in said window traverses through previous sentences to find the possible antecedent

From testing with different databases, program yielded an average of 72% accuracy
Handling of reflexive pronouns remains a bit troublesome
