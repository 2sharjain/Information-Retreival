# Plagiarism checker

### Getting Started

* Python (**preferably version 3.7**)
* Git

## Installation

* Clone the repo using this command in your preferred directory
```git 
git clone https://github.com/2sharjain/Information-Retreival.git
```

* Install nltk using pip
  
```bash
    pip3 install nltk
```

* Then, download required data for nltk

```python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> exit()
```

* Configuration

- Create a copy of config.template.json and rename it to config.json
- In this file enter the corpus dir and the name of the pickle file to which the index must be written.
- For fields other than CORPUS_DIR it is not mandatory for the file to already exist. Just give a name in the entry appending with a .pkl


* Running

- If the index files are not found or if you are running it for the first time, the index for the given
  CORPUS_DIR will be built.

- Run the main.py file in the following way
  
```bash
    python3 main.py --file_name={path_to_file}
```
- For info on other options run the file with --help option
```bash
    python3 main.py --help
```

- To rebuild the index with a different corpus, edit the config.json and run the comman

```bash
    python3 main.py --build
```

- By default, the results are obtained using LSH. To use TF-IDF for obtaining results run
```bash
    python3 main.py --file_name={path_to_file} --use_idf
```


## TEAM:
* Naman Arora
* Toshit Jain
* Lovedeep Singh Sidhu
