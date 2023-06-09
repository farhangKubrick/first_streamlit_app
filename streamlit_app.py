import streamlit
import pandas as pd
my_fruits_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruits_list)
streamlit.title('My parents new healthy diner')
streamlit.header('Header 1')
streamlit.text('text 1')
streamlit.text('text 2')
streamlit.text('from Vs code')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
