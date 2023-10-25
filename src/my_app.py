from src.my_db import MyDB
from src.my_plots import SimpleLinePlot, SimpleBarChart
import streamlit as st
import io

class MyApp:
    def __init__(self):
        self.db = MyDB()
        self.build_page()
        return

    # main build_page method
    def build_page(self):
        st.write('# My Awesome Store.com')
        
        st.write('\n---\n## Executive Dashboard')
        self.build_sales_plot()

        st.write('\n---\n### Customer Tracker')
        self.build_customer_tracker()
        
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
    
    @st.cache_data
    def get_customers(_self):
        return _self.db.get_customers()
    
    @st.cache_data
    def get_customer_sales(_self, cust_id):
        return _self.db.get_customer_sales(cust_id)
    
    @st.cache_data
    def get_customer_order_history(_self, cust_id):
        return _self.db.get_customer_order_history(cust_id)
    
    def build_customer_tracker(self):
        cols = st.columns([1,0.1,1])
        self.show_customer_sales_totals(cols[0])
        self.show_customer_order_history(cols[2])
        self.create_download_buttons(cols[2])
        return
    
    def show_customer_sales_totals(self, container):
        # Initialize a bar chart
        self.plot_cust = SimpleBarChart()

        # Get customer info
        cust_info = self.get_customers()

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
        # First check if a customer was previously selected
        if 'cust_index' in st.session_state:
            index = st.session_state['cust_index']
        else:
            index = 0
        
        cust_selector = container.selectbox('Select customer',
                                            cust_dict,
                                            index=int(index))
        
        # Store the currently selected cust_id
        cust_selected = cust_dict[cust_selector]

        # Store selection info in the session state
        st.session_state['cust_id'] = cust_selected
        # Index of the currently selected customer in the dropdown
        #  (Don't assume it's the same number as cust_id)
        cust_index = list(cust_dict.values()).index(cust_selected)
        st.session_state['cust_index'] = cust_index
        # Save the customer name to the session state for other processes to access
        st.session_state['cust_name'] = cust_info['first'][cust_index] + ' ' +  cust_info['last'][cust_index]
        
        # Get the sales data
        data = self.get_customer_sales(cust_selected)
        
        # Plot it
        self.plot_cust.update_plot(data['year'], data['Sales'])
        container.pyplot(self.plot_cust.fig)
        return
    
    def show_customer_order_history(self,
                                    container
                                    ):
        container.write('Order History')

        data = self.db.get_customer_order_history(st.session_state['cust_id'])
        container.write(data)
        return
    
    def create_download_buttons(self, 
                                container):
        cols = container.columns(2)
        # Download the figure
        img = io.BytesIO()
        self.plot_cust.fig.savefig(img, format='svg')
        filename = st.session_state['cust_name']
        cols[0].download_button(label='Download Plot',
                                data = img,
                                file_name = filename + '.svg',
                                mime='image/svg')
        
        data = self.get_customer_sales(st.session_state['cust_id'])
        cols[1].download_button(label='Download Data',
                                data = data.to_csv(),
                                file_name = filename + '.csv',
                                mime='text/csv')
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