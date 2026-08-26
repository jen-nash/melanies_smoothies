# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col  

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)

name_on_order = st.text_input("Name on smoothie:",)
st.write("The name on your smoothie will be:", name_on_order)


# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=6
)

if ingredients_list and name_on_order:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

  #  st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""   

    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

import requests
import streamlit as st

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
if smoothiefroot_response.status_code == 200:
    st.write(smoothiefroot_response.json())
else:
    st.error(f"API returned {smoothiefroot_response.status_code}")
    st.write(smoothiefroot_response.text)
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = true)
