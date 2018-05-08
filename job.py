# load data
filename = input('Enter the file name: ')
file = open(filename)
text = file.read()
file.close()
# split into words
from nltk import word_tokenize
tokens = word_tokenize(text)
# convert  to lower case
tokens = [w.lower() for w in tokens]
# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
# remove all tokens that are not alphabetic
words = [word for word in tokens if word.isalpha()]
# filter out stop words
from nltk.corpus import stopwords
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
