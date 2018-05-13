import os.path
import sys
import string
import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from nltk import word_tokenize
from nltk.corpus import stopwords

# does db exist?
if not os.path.exists('job.db'):
    # create db
    Base = declarative_base()

    class Word(Base):
        __tablename__ = 'word'
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)

    engine = create_engine('sqlite:///job.db')

    Base.metadata.create_all(engine)


# run script
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
