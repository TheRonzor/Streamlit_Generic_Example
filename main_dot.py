import matplotlib.pyplot as plt
import streamlit as st

class MoveTheDot:
    INC = 0.05 # How much the dot moves
    def __init__(self):
        if 'data' not in st.session_state:
            self.data = [0.5,0.5]
            st.session_state['data'] = self.data
        else:
            self.data = st.session_state['data']

        if 'figure' not in st.session_state:
            self.fig, self.ax = plt.subplots(figsize=(4,4))
            self.scat = self.ax.scatter(self.data[0], self.data[1], ec='k')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_xlim([0,1])
            self.ax.set_ylim([0,1])
            st.session_state['figure'] = [self.fig, self.ax, self.scat]
        else:
            self.fig, self.ax, self.scat = st.session_state['figure']

        self.build_page()
        return
    
    def update_figure(self):
        self.scat.set_offsets(self.data)
        return
    def move_up(self):
        self.data[1]+=self.INC
        self.data[1]%=1
        self.update_figure()
        return
    def move_down(self):
        self.data[1]-=self.INC
        self.data[1]%=1
        self.update_figure()
        return
    def move_left(self):
        self.data[0]-=self.INC
        self.data[0]%=1
        self.update_figure()
        return
    def move_right(self):
        self.data[0]+=self.INC
        self.data[0]%=1
        self.update_figure()
        return
    
    def build_page(self):
        st.write("# Move the dot!")

        # Create empty columns to reduce plot size
        plot_cols = st.columns([1,5,1])
        plot_cols[1].pyplot(self.fig)

        
        # There is no grid layout in streamlit,
        # and no built-in way to center things
        # below is a hack!

        button_area = plot_cols[1]

        button_row1 = button_area.container()
        button_row2 = button_area.container()
        button_row3 = button_area.container()

        # Experiment until it looks roughly centered
        n = 9
        offset = 3

        button_cols1 = button_row1.columns(n)
        button_cols1[offset+0].write(' ')
        button_cols1[offset+1].button('^', on_click=self.move_up)
        button_cols1[offset+2].write(' ')

        button_cols2 = button_row2.columns(n)
        button_cols2[offset+0].button('<', on_click=self.move_left)
        button_cols2[offset+1].write(' ')
        button_cols2[offset+2].button('\>', on_click=self.move_right)

        button_cols3 = button_row3.columns(n)
        button_cols3[offset+0].write(' ')
        button_cols3[offset+1].button('v', on_click=self.move_down)
        button_cols3[offset+2].write(' ')

        self.streamlit_defaults()
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
    
if __name__ == '__main__':
    MoveTheDot()