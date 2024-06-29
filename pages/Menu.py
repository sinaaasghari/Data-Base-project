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

    def modify_food(self,operation: Literal['add', 'remove','update'],
                    name:str,
                    Type:Optional[Literal['Main','Drink','Dessert']] = None,
                    remaining:Optional[int]=None,price:Optional[int]=None) -> None:
        
        if operation not in ['add','remove','update']:
            print('operation should be either add or remove or update')
            return
        #check if the name is already in the database, if the name exists, don't add it again
        if operation == 'add':
            check_query = f"SELECT * FROM Menu WHERE name = '{name}'"
            if self.query(check_query).shape[0] > 0:
                print('food already exists')
                return
            
            if None in (Type,remaining,price):
                print('missing values')
                return
            
            try :
                query = f"INSERT INTO Menu (name,type,remaining,price) VALUES ('{name}','{Type}',{remaining},{price})"
                self.execute(query)
                print('food added successfully')

            except Exception as e:
                print(f'Error inserting food \n error : {e}')
                return
                
        elif operation == 'remove':
            try:
                query = f"DELETE FROM Menu WHERE name = '{name}'"
                self.execute(query)
                
                if self.cursor.rowcount == 0: # check if food exists    
                    print('food not found')
                else:
                    print('food removed successfully')
                    
            except Exception as e :
                print(f"Error deleting food \n error : {e}")
            
        elif operation == 'update':
            try:
                update_query = "UPDATE Menu SET"
                update_values = []
                if Type is not None:
                    update_values.append(f" type = '{Type}'")
                if remaining is not None:
                    update_values.append(f" remaining = {remaining}")
                if price is not None:
                    update_values.append(f" price = {price}")
                update_query += " , ".join(update_values)
                update_query += f" WHERE name = '{name}'"
                
                self.execute(update_query)
                
                if self.cursor.rowcount == 0:
                    print('food not found')
                else:
                    print('food updated successfully')
                    
            except Exception as e:
                print(f'Error updating food \n error : {e}')
        
    def modify_customer(self,operation: Literal['add', 'remove','update'],
                        phone:str , 
                        second_phone:Optional[str]=None,
                        name:Optional[str]=None) -> None:
        
        if operation not in ['add','remove','update']:
            print('operation should be either add or remove')
            return
        
        if operation == 'add':
            check_query = f"SELECT * FROM Customer WHERE phone = '{str(phone)}'"
            if self.query(check_query).shape[0] > 0:
                print('Customer already exists')
                return
            
            if None in (name,phone):
                print('missing values')
                return
            
            try:
                query = f"INSERT INTO Customer (name,phone) VALUES ('{name}','{phone}')"
                # print(query)
                self.execute(query)
                print('customer added successfully')

            except Exception as e:
                print(f'Error inserting customer \n error : {e}')
                return
            
        elif operation == 'remove':
            try:
                query = f"DELETE FROM Customer WHERE phone = '{phone}'"
                self.execute(query) 
                
                if self.cursor.rowcount == 0 : 
                    print('customer not found')
                else:
                    print('customer removed successfully')
                    
            except Exception as e:
                print(f'Error deleting customer \n error : {e}')


        elif operation == 'update':
            try:
                update_query = "UPDATE Customer SET"
                update_values = []
                if name is not None:
                    update_values.append(f" name = '{name}'")
                if second_phone is not None:
                    update_values.append(f" phone = '{second_phone}'")
                  
                update_query += " , ".join(update_values)
                update_query += f" WHERE phone = '{phone}'"
                
                self.execute(update_query)
                
                if self.cursor.rowcount == 0:
                    print('Customer not found')
                else:
                    print('Customer updated successfully')
                    
            except Exception as e:
                print(f'Error updating customer \n error : {e}')


    def modify_Employee(self,operation: Literal['add', 'remove','update'],
                        ssn:str,
                        name:Optional[str]=None,
                        role:Optional[Literal['Chef','Waiter','Seller','Manager']]=None,
                        date:Optional[str]=None) -> None:
        if operation not in ['add','remove','update']:
            print('operation should be either add or remove or update')
            return        
        if operation == 'add':
            check_query = f"SELECT * FROM Employee WHERE ssn = '{ssn}'"
            if self.query(check_query).shape[0] > 0:
                print('Employee already exists')
                return
            
            if None in (name,ssn,role,date):
                print('missing values')
                return
            
            try:
                query = f"INSERT INTO Employee (ssn,name,role,date) VALUES ('{ssn}','{name}','{role}','{date}')"
                self.execute(query)
                print('Employee added successfully)')
            except Exception as e : 
                print(f'Error adding employee \n error : {e}')
                
        if operation == 'remove':
            try:
                query = f"DELETE FROM Employee WHERE ssn = '{ssn}'"
                self.execute(query)
                
                if self.cursor.rowcount == 0:
                    print('Employee not found')
                else:
                    print('Employee removed successfully')
                    
            except Exception as e:
                print(f'Error deleting employee \n error : {e}')

        if operation == 'update':
            try:
                update_query = "UPDATE Employee SET"
                update_values = []
                if name is not None:
                    update_values.append(f" name = '{name}'")
                if role is not None:
                    update_values.append(f" role = '{role}'")
                if date is not None:
                    update_values.append(f" date = '{date}'")
                update_query += " , ".join(update_values)
                update_query += f" WHERE ssn = '{ssn}'"
                
                self.execute(update_query)
                
                if self.cursor.rowcount == 0:
                    print('Employee not found')
                else:
                    print('Employee updated successfully')
                    
            except Exception as e:
                print(f'Error updating employee \n error : {e}')
    
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
                query = f"INSERT INTO [Table] (id,capacity) VALUES ({id},{capacity},'{status}')"
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

st.markdown("<h2 style='color: green;'>Menu management</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    Name = st.text_input("Name")

with col2:
    type = st.selectbox("type", ['Main','Drink','Dessert'])

with col3:
    remaining = st.number_input("remaining", value=None, step=1, format='%d')

with col4:
    price = st.number_input("price", value=None, step=1, format='%d')

if st.button("add"):
    db.modify_food('add', Name, type , remaining , price)

st.markdown("---")

col5, col6, col7, col8 = st.columns(4)
with col5:
    Name = st.text_input("Food's Name")

if st.button("remove"):
    db.modify_food('remove', Name)

st.markdown("---")

col9, col10, col11, col12 = st.columns(4)

with col9:
    Name = st.text_input("Food Name")

with col10:
    type = st.selectbox("updated type", ['Main','Drink','Dessert'])

with col11:
    remaining = st.number_input("updated remaining", value=None, step=1, format='%d')

with col12:
    price = st.number_input("updated price", value=None, step=1, format='%d')

if st.button("update"):
    db.modify_food('update', Name, type , remaining , price)

a = db.show_tables('Menu')


st.markdown("---")

if st.button('Show Menu Table'):
    df = db.query("SELECT * FROM Menu")
    st.write(df)
