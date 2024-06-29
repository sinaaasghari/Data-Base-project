import streamlit as st
import pandas as pd
import pyodbc
import numpy as np

server = 'SHAD\SQLEXPRESS'
database = 'resturant'
username = ''  # Only if using SQL Server Authentication
password = ''  # Only if using SQL Server Authentication

from typing import Literal , Optional

class Database:

    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.conn.cursor()

    def query(self, query:str):
        """
        Read SQL query or database table into a DataFrame.

        """
        return pd.read_sql(query, self.conn)

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def show_tables(self,table:Literal['Menu','Customer','Employee','Order','Table']):
        """
        Show the content of a table in the database
        
        Parameters
        ----------
        table : str
            The name of the table to show {Menu, Customer, Employee, Order, Table}
            
        Returns
        -------
        DataFrame
            The content of the table
        """
        query = f"SELECT * FROM [{table}]"
        df = self.query(query)
        df
        return df

   
    
    def add_order(self,
                     customer_id:Optional[int]=None,
                     menu_id:Optional[int]=None,
                     staus:Optional[Literal['Pending','Done']]=None,
                     type:Optional[Literal['TakeAway','DineIn']]=None,
                     table_id:Optional[int]=None,
                     employee_id:Optional[str]=None , 
                     date:Optional[str]=None) -> None:
            
            try:
                query = f"INSERT INTO [Order] (customer_id,menu_id,status,type,table_id,employee_id,date) VALUES ({customer_id},{menu_id},'{staus}','{type}','{table_id}','{employee_id}','{date}')"
                # print(query)
                self.execute(query)
                print('Order added successfully')
            except Exception as e:
                print(f'Error adding order \n error : {e}')
                     
    def remove_order(self,id:int):
        try:
            query = f"DELETE FROM [Order] WHERE id = '{id}'"
            self.execute(query)
            
            if self.cursor.rowcount == 0:
                print('Order not found')
            else:
                print('Order removed successfully')
                
        except Exception as e:
            print(f'Error deleting order \n error : {e}')

    def update_order(self,id:int,
                     customer_id:Optional[int]=None,
                     menu_id:Optional[int]=None,
                     staus:Optional[Literal['Pending','Done']]=None,
                     type:Optional[Literal['TakeAway','DineIn']]=None,
                     table_id:Optional[int]=None,
                     employee_id:Optional[str]=None , 
                     date:Optional[str]=None) -> None:
        
        try:
            update_query = "UPDATE [Order] SET"
            update_values = []
            if customer_id is not None:
                update_values.append(f" customer_id = {customer_id}")
            if menu_id is not None:
                update_values.append(f" menu_id = {menu_id}")
            if staus is not None:
                update_values.append(f" status = '{staus}'")
            if type is not None:
                update_values.append(f" type = '{type}'")
            if table_id is not None:
                update_values.append(f" table_id = {table_id}")
            if employee_id is not None:
                update_values.append(f" employee_id = '{employee_id}'")
            if date is not None:
                update_values.append(f" date = '{date}'")
            update_query += " , ".join(update_values)
            update_query += f" WHERE id = {id}"
            
            self.execute(update_query)
            
            if self.cursor.rowcount == 0:
                print('Order not found')
            else:
                print('Order updated successfully')
                
        except Exception as e:
            print(f'Error updating order \n error : {e}')
            
        
   
        
    def __del__(self):
        self.conn.close()

db = Database()

st.markdown("<h2 style='color: green;'>Orders management</h2>", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    customer_id = st.text_input("customer_id")

with col2:
    menu_id = st.text_input("menu_id")

with col3:
    status = st.selectbox("Status", ['Pending', 'Done'])

with col4:
    order_type = st.selectbox("Type", ['TakeAway', 'DineIn'])

with col5:
    table_id = st.number_input("Table", value=None, step=1, format='%d')

with col6:
    employee_id = st.number_input("Employee",  value=None, step=1, format='%d')

with col7:
    date = st.date_input("Date")


if st.button("add"):
    if customer_id and menu_id:
        db.add_order(customer_id[0], menu_id[0], status, order_type, table_id, employee_id, date)
    else:
        st.error("Customer ID or Menu ID not found.")

st.markdown("---")
col8, col9, col10, col11, col12, col13, col14= st.columns(7)
with col8:
    id = st.text_input("Id")
if st.button("remove"):
    db.remove_order(id)

st.markdown("---")

col15, col16, col17, col18, col19, col20, col21, col22 = st.columns(8)
with col15:
    id = st.text_input("order Id")
with col16:
    customer_id = st.text_input("new C_id")

with col17:
    menu_id = st.text_input("new M_id")

with col18:
    status = st.selectbox("new Status", ['Pending', 'Done'])

with col19:
    order_type = st.selectbox("new Type", ['TakeAway', 'DineIn'] )

with col20:
    table_id = st.number_input("new Table", value=None, step=1, format='%d')

with col21:
    employee_id = st.number_input("New Emp", value=None, step=1, format='%d')

with col22:
    date = st.date_input("new Date")



if st.button("update"):
    if customer_id and menu_id:
        db.update_order(id, customer_id[0], menu_id[0], status, order_type, table_id, employee_id, date)
    else:
        st.error("Customer ID or Menu ID not found.")

a = db.show_tables('Order')


st.markdown("---")

if st.button('Show Order Table'):
    df = db.query("SELECT * FROM [Order]")
    st.write(df)