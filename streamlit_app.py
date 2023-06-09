

import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

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

#A function to manage repeated API request
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #this onl writes data to the screen
    #streamlit.text(fruityvice_response.json())
    #This converts the json to a tabular format
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#Try except block to capture errors
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()


def get_fruit_load_list():
    #This will be used to query the database
    with my_cnx.cursor() as my_cur:
        #Running some sql on the db
        my_cur.execute("SELECT * from fruit_load_list")
        #Getting the first row
        #my_data_row = my_cur.fetchone()
        #Getting all the rows from the query
        my_data_row = my_cur.fetchall()
        return my_data_row
streamlit.header("The fruit load list contains:")
#If the streamlit button is pressed then execute the following:
if streamlit.button('Get Fruit Load List'):
    #Creating a connection to snowflake
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#A function to add a fruit to the snowflake table
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        #By enclosing new_fruit in '+' we can dynamically add a variable
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
        return('Thanks for adding ' + new_fruit)
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    #Creating a connection to snowflake
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = insert_row_snowflake(add_my_fruit)
    #Clsoing the connection, for best practice
    my_cnx.close()
    streamlit.text(my_data_rows)


#Not running any code apst this
streamlit.stop()