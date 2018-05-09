import os.path
import string
import sqlite3
from nltk import word_tokenize
from nltk.corpus import stopwords

# create table in db
conn = sqlite3.connect('jobs.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Keywords')
cur.execute('CREATE TABLE Keywords (word TEXT, occurences INTEGER)')

while True:
    # load data
    filename = input('Enter the file name: ')
    try:
        file = open(os.path.join('descriptions',filename), 'r')
    except:
        print('File cannot be opened: ', filename)
        break
    text = file.read()
    file.close()
    # split into words
    tokens = word_tokenize(text)
    # convert  to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove all tokens that are not alphabetic
    words = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # count words
    counts = dict()
    for word in words:
        if word not in counts:
            counts[word] = 1
        else:
            counts[word] += 1
    print(counts)
    # continue?
    end = input("Do you have another file (Y/N): ")
    if end == "N":
        break
