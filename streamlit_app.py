# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
import requests

#st.text(smoothiefroot_response.json())

session = cnx.session()
helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on smoothie')
st.write('The name of your smoothier will be',name_on_order)



#option = st.selectbox(
    #"What is your favorite fruits ?",
    #("Banana", "Strawberries", "Peaches")
#)

#st.write("You favorite fruit is:", option)



#ajouter les 25 fruits a ma liste à partir de la BD
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
      
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        #sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        #st.write(ingredients_string)
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop
    cnx = st.connection("snowflake")
    session = cnx.session()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        cnx = st.connection("snowflake")
        session = cnx.session()
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
