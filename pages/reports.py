import streamlit as st
import pandas as pd
import pyodbc
import numpy as np
import json
from deepdiff import DeepDiff

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
        

def format_df(df):
    
    def format_diff(json_str1, json_str2):
        if json_str1 is None:
            return ['Data Added']
        if json_str2 is None:
            return ['Data Deleted']

        json_obj1 = json.loads(json_str1)
        json_obj2 = json.loads(json_str2)
        diff = DeepDiff(json_obj1, json_obj2, ignore_order=True)
        formatted_diffs = []

        def clean_path(path):
            # Remove the 'root' prefix and the surrounding brackets
            return path.replace("root", "").strip('[]')

        for change_type, changes in diff.items():
            if change_type == 'values_changed':
                for path, change in changes.items():
                    old_value = change['old_value']
                    new_value = change['new_value']
                    cleaned_path = clean_path(path)
                    formatted_diffs.append(f"{cleaned_path}: {old_value} -> {new_value}")
            elif change_type == 'iterable_item_added':
                for path, new_value in changes.items():
                    cleaned_path = clean_path(path)
                    formatted_diffs.append(f"{cleaned_path}: None -> {new_value}")
            elif change_type == 'iterable_item_removed':
                for path, old_value in changes.items():
                    cleaned_path = clean_path(path)
                    formatted_diffs.append(f"{cleaned_path}: {old_value} -> None")

        return formatted_diffs
    
    df['NewData'] = df['NewData'].apply(lambda x : x[1:-1] if type(x) == str else None)
    df['OriginalData'] = df['OriginalData'].apply(lambda x : x[1:-1] if type(x) == str else None)   
    df['Changes'] = df.apply(lambda x : format_diff(x['OriginalData'],x['NewData']),axis=1)
    # reorder the columns
    df = df[['LogID','ChangeTime', 'TableName', 'ChangeType', 'OriginalData', 'NewData' , 'Changes']]
    return df

db = Database()

st.markdown("<h2 style='color: green;'>Reports</h2>", unsafe_allow_html=True)


set = '''
SELECT DISTINCT CONVERT(DATE, ChangeLog.ChangeTime) AS unique_date
FROM dbo.ChangeLog
ORDER BY unique_date;
'''
df = db.query(set)

list = df['unique_date'].tolist()

Date = st.selectbox("Date", list)


if st.button("Show"):
    df_temp = db.query(f"SELECT ChangeTime ,TableName, NewData, OriginalData, ChangeType, LogID FROM dbo.ChangeLog WHERE CONVERT(DATE, ChangeTime) = '{Date}'")
    st.write(format_df(df_temp))

st.markdown("---")


List_of_table = ['Menu','Customer','Employee','Order','Table']

Name = st.selectbox("Which Part?", List_of_table)


if st.button("Show_res"):
    df_temp2 = db.query(f"SELECT ChangeTime ,TableName, NewData, OriginalData, ChangeType, LogID FROM  dbo.ChangeLog WHERE TableName = '{Name}'")
    st.write(format_df(df_temp2))
    

st.markdown("---")


List_of_action = ['Insert', 'Delete', 'Update']

Action = st.selectbox("Which Action?", List_of_action)


if st.button("Show_res2"):
    df_temp3 = db.query(f"SELECT ChangeTime, TableName, NewData, OriginalData, ChangeType, LogID FROM  dbo.ChangeLog WHERE ChangeType = '{Action}'")
    st.write(format_df(df_temp3))




