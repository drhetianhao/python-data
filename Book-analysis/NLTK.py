import matplotlib.pyplot as mpLib
from wordcloud import WordCloud, STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import nltk

nltk.download("punkt")

corpus = PlaintextCorpusReader(r"", "TJ1.txt")
print(corpus.raw())

# extract words from the corpos
print("Words in the corpus:", corpus.words())

freq = nltk.FreqDist(corpus.words())
# common words
print("Common Words:", freq.most_common(10))

# Read the base file into a raw text variable
base_file = open(
    r"C:\Users\hetia\Desktop\Book" + "/TJ.txt", "rt", encoding="utf8", errors="ignore"
)
raw_text = base_file.read()
base_file.close()

# Extract tokens
token_list = nltk.word_tokenize(raw_text)
print("Token List : ", token_list[:20])
print("\n Total Tokens : ", len(token_list))


# Use the Punkt library to extract tokens
token_list2 = list(
    filter(lambda token: nltk.tokenize.punkt.PunktToken(token).is_non_punct, token_list)
)
print("Token List after removing punctuation : ", token_list2[:20])
print("\nTotal tokens after removing punctuation : ", len(token_list2))


token_list3 = [word.lower() for word in token_list2]
print("Token list after converting to lower case : ", token_list3[:20])
print("\nTotal tokens after converting to lower case : ", len(token_list3))


# Download the standard stopword list
nltk.download("stopwords")

# Remove stopwords
token_list4 = list(
    filter(lambda token: token not in stopwords.words("english"), token_list3)
)
print("Token list after removing stop words : ", token_list4[:20])
print("\nTotal tokens after removing stop words : ", len(token_list4))


# Use the wordnet library to map words to their lemmatized form
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
token_list6 = [lemmatizer.lemmatize(word) for word in token_list4]
print("Token list after Lemmatization : ", token_list6[:20])
print("\nTotal tokens after Lemmatization : ", len(token_list6))


# to install wordcloud - execute "pip install wordcloud" from Anaconda prompt
# read the course descriptions
with open("TJ.txt", "r", encoding="utf8", errors="ignore") as fh:
    filedata = fh.read()

# check contents
print("File data sample : ", filedata[:200])

# Create stopword list:
stopwords = set(STOPWORDS)

# Generate wordcloud data
wordcloud = WordCloud(
    stopwords=stopwords, max_words=25, background_color="white"
).generate(filedata)

mpLib.imshow(wordcloud)
mpLib.axis("off")
mpLib.show()
