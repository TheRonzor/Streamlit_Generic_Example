import os
import sqlite3
import pandas as pd

class MyDB:
    def __init__(self):
        self.path_data = os.path.join(os.path.dirname(__file__), 'data')
        self.path_db = os.path.join(self.path_data, 'store.db')
        return
    
    def connect(self):
        self.conn = sqlite3.connect(self.path_db)
        self.curs = self.conn.cursor()
        return
    
    def close(self):
        self.conn.close()
        return
    
    def run_query(self, 
                  sql: str, 
                  params: tuple|dict=None
                  ) -> pd.DataFrame:
        self.connect()
        results = pd.read_sql(sql, self.conn, params=params)
        self.close()
        return results
    
    def get_monthly_sales(self) -> pd.DataFrame:
        sql = """
            SELECT substr(date,1,7) as month, 
                sum(qty*unit_price) as Sales
            FROM tOrder
            JOIN tOrderDetail USING(order_id)
            JOIN tProd USING (prod_id)
            GROUP BY month
            ORDER BY month ASC
            ;"""
        return self.run_query(sql)
    
    def get_customers(self) -> pd.DataFrame:
        sql = """
            SELECT cust_id, first, last
            FROM tCust
            ;"""
        return self.run_query(sql)
    
    def get_customer_sales(self, 
                           cust_id:int,
                           ) -> pd.DataFrame:
        sql = """
            SELECT substr(date,1,4) as year,
                   sum(qty*unit_price) as Sales
            FROM tOrder
            JOIN tOrderDetail USING(order_id)
            JOIN tProd USING(prod_id)
            WHERE cust_id = :cust_id
            GROUP BY year
            ORDER BY year ASC
            ;"""
        return  self.run_query(sql, {'cust_id': cust_id})
    
    