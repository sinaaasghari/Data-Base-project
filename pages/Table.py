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

            
        
    def modify_table(self, operation: Literal['add', 'remove','update'],
                     id: int,
                     capacity: Optional[int] = None , 
                     status: Optional[Literal['empty','taken']] = None):
        
        if operation not in ['add', 'remove','update']:
            print('operation should be either add or remove or update')
            return
        
        if operation == 'add':
            check_query = f"SELECT * FROM [Table] WHERE id = '{id}'"
            if self.query(check_query).shape[0] > 0:
                print('Table already exists')
                return
            
            if None in (id,capacity):
                print('missing values')
                return
            
            try:
                query = f"INSERT INTO [Table] (id,capacity,status) VALUES ({id},{capacity},'{status}')"
                self.execute(query)
                print('Table added successfully')
            except Exception as e:
                print(f'Error adding table \n error : {e}')
                
        if operation == 'remove':
            try:
                query = f"DELETE FROM [Table] WHERE id = '{id}'"
                self.execute(query)
                
                if self.cursor.rowcount == 0:
                    print('Table not found')
                else:
                    print('Table removed successfully')
                    
            except Exception as e:
                print(f'Error deleting table \n error : {e}')
        
        
        
        if operation == 'update':
            try:
                update_query = "UPDATE [Table] SET"
                update_values = []
                if capacity is not None:
                    update_values.append(f" capacity = {capacity}")
                if status is not None:
                    update_values.append(f" status = '{status}'")
                update_query += " , ".join(update_values)
                update_query += f" WHERE id = {id}"
                
                self.execute(update_query)
                
                if self.cursor.rowcount == 0:
                    print('Table not found')
                else:
                    print('Table updated successfully')
                    
            except Exception as e:
                print(f'Error updating table \n error : {e}')
        
    def __del__(self):
        self.conn.close()

db = Database()


st.markdown("<h2 style='color: green;'>Tables management</h2>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    number = st.text_input("Number")

with col2:
    capacity = st.number_input("Capacity", value=0, step=1, format='%d')
with col3:
    status = st.selectbox("Status", ['empty','taken'])



if st.button("add"):
    db.modify_table('add', number, capacity , status)

st.markdown("---")

col4, col5, col6 = st.columns(3)

with col4:
    number = st.text_input(" Table Number ")
if st.button("remove"):
    db.modify_table('remove',number)

st.markdown("---")


col7, col8, col9 = st.columns(3)

with col7:
    number = st.text_input("Table Number")

with col8:
    capacity = st.number_input("new Capacity", value=0, step=1, format='%d')
    
with col9:
    status = st.selectbox("new Status", ['empty', 'taken'])



if st.button("update"):
    db.modify_table('update',number, capacity,  status)


a = db.show_tables('Table')


st.markdown("---")

if st.button('Show Tables'):
    df = db.query("SELECT * FROM [Table]")
    st.write(df)