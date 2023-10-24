from src.my_db import MyDB
from src.my_plots import SimpleLinePlot
import streamlit as st
 
class MyApp:
    def __init__(self):
        self.db = MyDB()
        self.sales_plot = SimpleLinePlot()

        self.build_page()
        return

    def update_sales_plot(self, 
                          style:str
                          ):
        data = self.db.get_monthly_sales()
        
        xticks = range(len(data))
        months = data['month']
        
        self.sales_plot.update_plot(xticks, 
                                    data['Sales']/1000,
                                    x_label=None,
                                    y_label = "Sales ('000s)",
                                    x_ticklabels=months,
                                    style = style)
        
        # Unclutter the month markers
        self.sales_plot.ax.set_xticklabels(self.sales_plot.ax.get_xticklabels(), 
                                           rotation=45)
        self.sales_plot.ax.set_xticks(self.sales_plot.ax.get_xticks()[::3])
        return

    def build_page(self):
        st.header('My Awesome Store.com')
        
        self.build_sales_chart()

        self.build_customer_tracker()

        self.streamlit_defaults()
        return
    
    def build_sales_chart(self):
        # Example of a dropdown box to select things
        styles = {'Black line with x marks'         : '-kx',
                  'Blue dotted line with circles'   : ':ob'
                  }
        self.style_selector = st.selectbox('Select plot style',
                                      styles,
                                      index=0
                                      )
        current_style = styles[self.style_selector]
        
        # Sales chart
        self.update_sales_plot(current_style)
        st.pyplot(self.sales_plot.fig)
        return
    
    def build_customer_tracker(self):

        # Put it inside a container (pass container in?)

        # Dropdown to select a customer
        cust_info = self.db.get_customers()

        cust_dict = {str(cust_info['cust_id'][i]) + \
                     ': ' + cust_info['first'][i] + \
                     ' ' + cust_info['last'][i] : cust_info['cust_id'][i]
                     for i in range(len(cust_info))
                     }
        cust_selector = st.selectbox('Select customer',
                                     cust_dict,
                                     placeholder="Select a customer")
        return
    
    def streamlit_defaults(self):
        '''
        Remove some auto-generated stuff by streamlit
        '''
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
        return