import streamlit
import requests
import pandas as pd
import snowflake.connector

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

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#this onl writes data to the screen
#streamlit.text(fruityvice_response.json())

#This converts the json to a tabular format
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

#Creating a connection to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#This will be used to query the database
my_cur = my_cnx.cursor()
#Running some sql on the db
my_cur.execute("SELECT * from fruit_load_list")
#Getting the first row
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)

