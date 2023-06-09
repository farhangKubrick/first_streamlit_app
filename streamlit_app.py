import streamlit
import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#Setting the index of our list to the fruit name in the table
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
#The list is based on the index of myfruitlist, which we have set to the 'fruit' column of the csv
# If we add a list in our third parameter it will autopopulate with those 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#Creating a subset by filtering our table only for the chosen fruits, which is dynamic based on our multiselect
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Displaying the filtered table
streamlit.dataframe(fruits_to_show)
streamlit.title('My parents new healthy diner')
streamlit.header('Header 1')
streamlit.text('text 1')
streamlit.text('text 2')
streamlit.text('from Vs code')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
