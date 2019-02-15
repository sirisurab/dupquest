# dupquest
IDENTIFYING DUPLICATE QUESTIONS

## Problem
Question-answering and knowledge-sharing platforms like Quora and Stack-Exchange require mechanisms to group questions in their database based on similar intent. According to Quora about 100 million users visit their website every month, and a lot of the questions end up being duplicates (duplicate questions could be differently worded but they have the same intent)
For example, the questions ‘What is the best way to travel from Houston to Atlanta ?’ and  ‘Should I drive, fly or take a bus from Houston to Atlanta ?’, are duplicates. 
User experience is greatly improved if Quora is able to identify duplicate questions as this enables them to find questions that have already been answered and also avoids the need to answer the same question multiple times.

## Data
Source : Kaggle (Quora Question Pairs)
Description : The dataset contains a human-labeled training set and a test set. Each record in the training set represents a pair of questions with the text of both questions and a binary label which indicates whether the question-pair represents a duplicate or not.

## Preprocessing
The dataset was processed by [this ipython file](src/tfidf_word2vec.ipynb)

## Modeling

### [Logistic Regression and XGBoost](src/tfidf_word2vec.ipynb)

### Deep Learning Methods
  [Attention based methods](src/DL_encode_attend.ipynb)
  [LSTMN (experimental)](src/DL_LSTMN.ipynb)
