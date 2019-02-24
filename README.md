# dupquest
## IDENTIFYING DUPLICATE QUESTIONS
<p>(for a more detailed description refer to the <a href='Capstone 2 - Final Report.pdf'>project report</a>)</p>

## Problem
<p>Question-answering and knowledge-sharing platforms like Quora and Stack-Exchange require mechanisms to group questions in their database based on similar intent. According to Quora about 100 million users visit their website every month, and a lot of the questions end up being duplicates (duplicate questions could be differently worded but they have the same intent)
For example, the questions ‘What is the best way to travel from Houston to Atlanta ?’ and  ‘Should I drive, fly or take a bus from Houston to Atlanta ?’, are duplicates. 
User experience is greatly improved if Quora is able to identify duplicate questions as this enables them to find questions that have already been answered and also avoids the need to answer the same question multiple times.</p>

## Data
Source : Kaggle (Quora Question Pairs)<br>
Description : The dataset contains a human-labeled training set and a test set. Each record in the training set represents a pair of questions with the text of both questions and a binary label which indicates whether the question-pair represents a duplicate or not.

## Data Processing
The dataset was processed by [this ipython file](src/tfidf_word2vec.ipynb)

### Preprocessing
<p>Following preprocessing was performed on the text data using the <a href='https://radimrehurek.com/gensim/parsing/preprocessing.html'>gensim API</a>:
<ul>
  <li>Tag Removal</li>
  <li>Repeating Whitespace Removal - Removed repeating whitespace characters (spaces, tabs, line breaks) and turned tabs & line breaks into spaces</li>
  <li>Stopwords Removal - Removed stopwords. (the default stopwords list from gensim was used)</li>
  <li>Case conversion and Stemming - Transformed text to lowercase and performed porter stemming.</li>
</ul>
</p>

### Word2Vec Embedding
The text data was embedded in 300 dimensional space using two methods:
<ul>
  <li>Word2Vec - <a href='https://fasttext.cc/docs/en/crawl-vectors.html'>Fasttext pretrained model for English</a> (trained on Common Crawl and Wikipedia) was transfer-trained with the questions in training data using the gensim method intersect_word2vec_format. This method allows one to initialize a word2vec model with a vocabulary same as that of the training data, then intersects this vocabulary with the pretrained model. No words are added to the existing vocabulary, but intersecting words adopt the weights of the pretrained model, while non-intersecting words are left alone.</li>
  <li>GloVe - <a href='https://spacy.io/models/en#en_vectors_web_lg'>Spacy pretrained model for English</a> (trained on Common Crawl using GloVe). Provision was made for Out Of Vocabulary (OOV) words by randomly mapping each OOV word to one of 50 randomly generated vectors.</li>
</ul>

## Modeling

### Machine Learning Methods
<ul>
  <li><a href='src/tfidf_word2vec.ipynb'>Logistic Regression</a></li>
  <li><a href='src/tfidf_word2vec.ipynb'>XGBoost</a></li>
</ul>

### Deep Learning Methods
<ul>
  <li><a href='src/DL_encode_attend.ipynb'>Attention based methods</a></li>
  <li><a href='src/DL_LSTMN.ipynb'>LSTMN (experimental and WIP)</a></li>
</ul>
