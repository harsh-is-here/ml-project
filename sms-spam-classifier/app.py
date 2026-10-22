import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
tfdf = pickle.load(open('vectorize.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title('Email Spam Classifier')

sms = st.text_area('Enter your email text below:')
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y=[]

    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)

if st.button('Predict'):
    #1 preprocess the input text
    transformed_sms = transform_text(sms)
    #2 vectorize the input text
    vectorized_sms = tfdf.transform([transformed_sms])
    #3 make prediction using the model
    prediction = model.predict(vectorized_sms)
    #4 Display the prediction result
    if prediction[0] == 1:
        st.header('Spam')
    else:
        st.header('Not Spam')