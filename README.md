# Third-Year-Project

Source Code For 'Mapping Adverse Drug Reaction entity to Ontology term'

# Introduction
This project aims to build the model which can extract ADR enitity from text, and then using ontology mapping tool 'EBI-ZOOMA' to map entity into ontology term.

main file: ```AdverseDrugReactionNER.ipynb```

This code can run properly on ```Colab```, all the tools that needs to download are listed at the top of the file ```AdverseDrugReactionNER.ipynb```. Please download additional packages as needed.

# Training
Our model is a pretrained BART (Bidirectional and Auto-Regressive Transformers）model.

The input is a csv file which contains 2 columns: The first columne is the free text, while the second columns is the template. The template should be either a positive (ADR) template or a negative template 

Example:  
pos: ``` Use of corticosteroids may result in posterior subcapsular cataract formation. | posterior subcapsular cataract is an adverse reaction entity.```  
neg: ``` Use of corticosteroids may result in posterior subcapsular cataract formation. | result in is not a named entity``` 

To fit the BART model sequence length, the length of free text should be within 1000. 

# Inference

In the inference part, Each word of the candidate text will be used to generate 1 to n grams. Then, those word will concatenate positive template amd negative template respectively to generate two candidate templates: ```[MASK] is an adverse reaction enitity``` and ```[MASK] is not a named entity```. Those candidates will be scored by the model and then choose the one with highest score as the prediction.

# Mapping
The input text will be input to the trained model to extract the possible ADR enitity, and those enitity will be mapped to ontology terms by calling ```ZOOMA``` API.

You can try the function by changing the variable ```input``` (which is under the 'Mapping to Ontology' markup.

The output is a csv file called ```'Mapping_result.csv'```, it contains: input text, extracted ADR entity, the mapped ontology term, confidence level, ontology id, and ontology source.

If you want to test the model, make sure you run all the functions below the ```Inference``` markup.

# Corpus

All the training and testing data comes from ```conll2003``` (https://bionlp.nlm.nih.gov/tac2017adversereactions/)

```Data_Generation.ipynb``` is used to generate training, validation and testing file for traing the model. All files are in csv format.

# Contact

If you have any question, please feel free to contacr Jiachen Fan.
(<jiachen.fan-2@student.manchester.ac.uk>)

