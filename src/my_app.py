from src.my_db import MyDB
from src.my_plots import SimpleLinePlot, SimpleBarChart
import streamlit as st
 
class MyApp:
    def __init__(self):
        self.db = MyDB()
        self.build_page()
        return

    # main build_page method
    def build_page(self):
        st.write('# My Awesome Store.com\n---')
        
        st.write('## Executive Dashboard')

        self.build_sales_plot()

        self.custom_columns = st.columns([1,0.1,1])
        self.build_customer_tracker(self.custom_columns[0])
        self.build_product_tracker(self.custom_columns[2])

        self.streamlit_defaults()
        return
    
    # Builders
#region
    def build_sales_plot(self):
        # Initialize a line plot
        self.plot_sales = SimpleLinePlot()

        # Example of a dropdown box to select things
        styles = {'Black line with x marks'         : '-kx',
                  'Blue dotted line with circles'   : ':ob'
                  }
        # Create the dropdown
        self.style_selector = st.selectbox('Select plot style',
                                           styles,
                                           index=0
                                           )
        # Capture the current value of the dropdown
        current_style = styles[self.style_selector]
        
        # Update the plot with the current data
        self.update_sales_plot(current_style)
        
        # Draw the plot
        st.pyplot(self.plot_sales.fig)
        return
    
    def build_customer_tracker(self, 
                               container
                               ):
        # Initialize a bar chart
        self.plot_cust = SimpleBarChart()

        # Get customer info
        cust_info = self.db.get_customers()


        # Customer selector will be formatted as either:
        #       cust_id: Name
        # or    Name: cust_id
        cust_selector_options = {'ID first': 0, 'Name first': 1}
        cust_selector_order = container.radio('How to select customers?',
                                               cust_selector_options,
                                               horizontal=True)

        # Depending on the option selected, build a
        # dictionary of options
        if cust_selector_options[cust_selector_order] == 0:
            
            cust_dict = {str(cust_info['cust_id'][i]) + \
                        ': ' + cust_info['first'][i] + \
                        ' ' + cust_info['last'][i] 
                        : cust_info['cust_id'][i]
                        for i in range(len(cust_info))
                        }
        else:
            
            cust_dict = {cust_info['first'][i] + \
                        ' ' + cust_info['last'][i] + \
                        ': ' + str(cust_info['cust_id'][i])
                        : cust_info['cust_id'][i]
                        for i in range(len(cust_info))
                        }
            
        # Create the dropdown menu for selecting a customer, based on above options
        cust_selector = container.selectbox('Select customer',
                                            cust_dict,
                                            index=0)
        
        # Store the currently selected option
        cust_selected = cust_dict[cust_selector]

        # Get the data
        data = self.db.get_customer_sales(cust_selected)
        
        # Plot it
        self.plot_cust.update_plot(data['year'], data['Sales'])
        container.pyplot(self.plot_cust.fig)
        return
    
    def build_product_tracker(self, 
                              container
                              ):
        # Initialize a bar chart
        self.plot_prod = SimpleBarChart()

        # Get product info
        prod_info = self.db.get_products()

        prod_selector_options = {'ID first': 0, 'Name first': 1}
        prod_selector_order = container.radio('How to select products?',
                                               prod_selector_options,
                                               horizontal=True)

        if prod_selector_options[prod_selector_order] == 0:
            
            prod_dict = {str(prod_info['prod_id'][i]) + \
                        ': ' + prod_info['prod_desc'][i] \
                        : prod_info['prod_id'][i]
                        for i in range(len(prod_info))
                        }
        else:
            
            prod_dict = {prod_info['prod_desc'][i] + \
                        ': ' + str(prod_info['prod_id'][i])
                        : prod_info['prod_id'][i]
                        for i in range(len(prod_info))
                        }
            
        # Create the dropdown menu for selecting a customer, based on above options
        prod_selector = container.selectbox('Select product',
                                            prod_dict,
                                            index=0)
        
        # Store the currently selected option
        prod_selected = prod_dict[prod_selector]

        # Get the data
        data = self.db.get_product_sales(prod_selected)

        # Plot the data
        self.plot_prod.ax.bar(data['year'], data['Sales'])
        container.pyplot(self.plot_prod.fig)
        return
    

#endregion

    # Updaters
#region
    def update_sales_plot(self, 
                          style:str
                          ):
        data = self.db.get_monthly_sales()
        
        xticks = range(len(data))
        months = data['month']
        
        self.plot_sales.update_plot(xticks, 
                                    data['Sales']/1000,
                                    x_label = None,
                                    y_label = "Sales ('000s)",
                                    x_ticklabels = months,
                                    style = style
                                    )
        
        # Unclutter the month markers
        self.plot_sales.ax.set_xticklabels(self.plot_sales.ax.get_xticklabels(), 
                                           rotation=45)
        self.plot_sales.ax.set_xticks(self.plot_sales.ax.get_xticks()[::3])
        return
#endregion

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