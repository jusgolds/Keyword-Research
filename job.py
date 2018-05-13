import os.path
import sys
import string
import sqlite3
import time
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import ClauseElement
from nltk import word_tokenize
from nltk.corpus import stopwords

Base = declarative_base()
class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    count = Column(Integer, default=0, nullable=False)

now = time.strftime("%Y%m%d-%H%M%S")
db_path = os.path.join('dbs', 'job-{}.db'.format(now))
engine = create_engine('sqlite:///{}'.format(db_path))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

descriptions_dir = 'descriptions'

directory = os.fsencode(descriptions_dir)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        with open('{}/{}'.format(descriptions_dir, filename)) as f:
            text = f.read()
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
        for word in counts:
            db_word = get_or_create(session, Word, name=word)
            db_word.count += counts[word]
            session.add(db_word)
            session.commit()
        print("Finished {}".format(filename))

print("Finished all files")
