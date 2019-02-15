# dupquest
IDENTIFYING DUPLICATE QUESTIONS

## Problem
<p>Question-answering and knowledge-sharing platforms like Quora and Stack-Exchange require mechanisms to group questions in their database based on similar intent. According to Quora about 100 million users visit their website every month, and a lot of the questions end up being duplicates (duplicate questions could be differently worded but they have the same intent)
For example, the questions ‘What is the best way to travel from Houston to Atlanta ?’ and  ‘Should I drive, fly or take a bus from Houston to Atlanta ?’, are duplicates. 
User experience is greatly improved if Quora is able to identify duplicate questions as this enables them to find questions that have already been answered and also avoids the need to answer the same question multiple times.</p>

## Data
Source : Kaggle (Quora Question Pairs)<br>
Description : The dataset contains a human-labeled training set and a test set. Each record in the training set represents a pair of questions with the text of both questions and a binary label which indicates whether the question-pair represents a duplicate or not.

## Preprocessing
The dataset was processed by [this ipython file](src/tfidf_word2vec.ipynb)

## Modeling

### Machine Learning Methods
<ul>
  <li><a href='src/tfidf_word2vec.ipynb'>Logistic Regression</a></li>
  <li><a href='src/tfidf_word2vec.ipynb'>XGBoost</a></li>
</ul>

### Deep Learning Methods
<ul>
  <li><a href='src/DL_encode_attend.ipynb'>Attention based methods</a></li>
  <li><a href='src/DL_LSTMN.ipynb'>LSTMN (experimental)</a></li>
</ul>
