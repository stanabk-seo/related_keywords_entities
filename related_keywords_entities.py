from bs4 import BeautifulSoup
import requests, lxml
import pandas as pd
import streamlit as st
import csv

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

st.title("""Keyword Research Tool""")
st.subheader('Get the related keywords and entities')
st.write('**Type any keyword in search box or Upload a CSV File with a list of keywords in it**')

with st.form(key='my_form'):
    keyword = st.text_input(label = 'Type any keyword (E.g. Marketing)')
    submit_button = st.form_submit_button(label = 'Fetch Keywords')

input_keyword = keyword.replace(" ", "+")

url = ('https://www.bing.com/search?q='+input_keyword+'&form=QBLH&sp=-1')

response = requests.get(url, headers=headers).text

soup = BeautifulSoup(response, 'lxml')

if input_keyword:

    print('Related Keywords:')
    st.write('**Related Keywords**')

    for related_search in soup.select('.b_rs ul li'):
        searches = related_search.text
        print(searches)
        st.write(searches)

    print('-----------------')
    st.write('----------------')

    print('Entities:')
    st.write('**Entities**')

    for entities in soup.select('.b_factrow a'):
        entities = entities.text
        print(entities)
        st.write(entities)

try:

    file = st.file_uploader('', type='csv')
    keyword_list = file
    if keyword_list:
        st.write('In Progress...')

    searches = []
    entities = []
    search_keywords = []
    search_entities = []

    for i in keyword_list:
        keyword = i.decode('utf-8')
        url = ('https://www.bing.com/search?q='+keyword+'&form=QBLH&sp=-1')
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')

        for related_search in soup.select('.b_rs ul li'):
            searches.append(related_search.text)
            search_keywords.append(keyword)

        for entity in soup.select('.b_factrow a'):     
            entities.append(entity.text)
            search_entities.append(keyword)

    df1 = pd.DataFrame(searches)
    df1.columns = ['related_keywords']
    df2 = pd.DataFrame(entities)
    df2.columns = ['related_entities']
    s1 = pd.Series(search_keywords, name = 'keywords')
    s2 = pd.Series(search_entities, name = 'keywords')

    df1_concat = pd.concat([s1, df1], axis=1)
    df2_concat = pd.concat([s2, df2], axis=1)

    result1 = df1_concat.groupby('keywords')['related_keywords'].apply(list)
    result2 = df2_concat.groupby('keywords')['related_entities'].apply(list)

    print('Related Keywords')
    st.write('**Related Keywords**') 
    st.write(result1)

    print('Related Entities')
    st.write('**Related Entities**') 
    st.write(result2)

    csv1 = result1.to_csv(index=True)
    csv2 = result2.to_csv(index=True)
    st.write('Done!')

    st.download_button('Download Related Keywords', csv1, 'related_keywords.csv', 'text/csv')
    st.download_button('Download Entities', csv2, 'related_keywords.csv', 'text/csv')

except:
    print('Ingore none type error')


st.write("\n")
st.write("\n")
st.write("\n")

st.write("@author: abhishek.shukla")
st.write("Facing issues?")
href2 = f'<a href="https://www.linkedin.com/in/abhishekshukla01/">DM me on Linkedin</a>'
href3 = f'<a href="https://twitter.com/StanAbK">DM me on Twitter</a>'
st.markdown(href2, unsafe_allow_html=True)
st.markdown(href3, unsafe_allow_html=True)


