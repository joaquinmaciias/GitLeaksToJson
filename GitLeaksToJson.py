#!user/bin/python3

# git init
# Module GitPython: python -m pip install gitpython
# Module entorno virtual: python -m venv env
# Create a virtual enviroment: env/Scrips >> .\activate
# Data extraction: git clone https://github.com/skalenetwork/skale-manager
# Create: .gitignore

from git import Repo

import re, signal, sys, os, json

# Finish the process with  Ctrl + C
def handler_signal(signal, frame):
    print('\n\n [!] Out ....... \n')
    sys.exit(1)

signal.signal(signal.SIGINT, handler_signal)

# Extraction

def extract(path):
    repo = Repo(path)
    return repo.iter_commits()

# Tranformation

def transform(commits, length):

    print('FIND GIT LEAKS\n')

    compile_key = input('Write a word that you want to find: ')

    list_all_matches = []

    pattern = re.compile(r'.*'+compile_key+'.*', re.IGNORECASE)

    print('Finding matches...\t')

    for commit in commits:
        matches = pattern.finditer(commit.message)
        if matches: list_all_matches.append(matches)
    
    print('Finished\n')

    listJsonData = []
    dictJsonData = {}

    counter = 1

    for matches in list_all_matches:
        for match in matches:

            dicts = {}
            
            string = 'Match ' + str(counter)
            dicts[string] = str(match)

            listJsonData.append(dicts)

            counter += 1

    dictJsonData['Matches'] = listJsonData

    return dictJsonData

# Load data on the screen

def load(dictJsonData):

    print('The matches are and the ata of the Json dictionaty: \n')

    print('{\n')

    for content in dictJsonData['Matches']:
        for key in content:

            print(str(key) , ': ' + str(content[key]) + ',\n')

    print('}\n')

if __name__ == '__main__':

    REPO_DIR = './skale-manager'

    commits = extract(REPO_DIR)

    length = len(list(commits))

    dictJsonData = transform(extract(REPO_DIR), length)

    load(dictJsonData)

    # Export matches to a Json

    input('Press ENTER to export the leaks to the Json File.')


    dataPythonYoJson = json.dumps(dictJsonData, indent=4)

    with open('jsonDataGitLeaks.json','w') as jsonFile:
        jsonFile.write(dataPythonYoJson)

    jsonFile.close()