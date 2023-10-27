from __future__ import annotations

# Libraries used for SomeRegression
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler as SS
from sklearn.preprocessing import PolynomialFeatures as PF

# Libraries used for RegressionPlot
import matplotlib.pyplot as plt

# Libararies used for app
import streamlit as st


# ToDo:

#  Need to create data once and save it (make a button for new data)
#  

class RegressionApp:
    DEFAULTS = {'alpha'  : 0,
                'da'     : 1,
                'degree' : 6
                }

    def __init__(self):

        if 'model' not in st.session_state:
            self.model = SomeRegression()
            self.model.make_data()
            st.session_state['model'] = self.model
        else:
            self.model = st.session_state['model']

        self.state_manager()
        self.build_page()
        return
    
    def state_manager(self):
        '''
        Ensure relevant variables/objects exist in the session_state
        If they do not, then create and set to default values
        '''
        for key, value in self.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value
        return
    
    def get_alpha(self):
        return float(st.session_state['alpha'])
    
    def set_alpha(self, 
                  alpha
                  ):
        st.session_state['alpha'] = round(alpha, 5)    
        return
    
    def get_da(self):
        return float(st.session_state['da'])

    def increase_alpha(self):
        self.set_alpha(self.get_alpha() + self.get_da())
        return
    
    def decrease_alpha(self):
        new_alpha = self.get_alpha() - self.get_da()
        new_alpha = max(new_alpha, 0)
        self.set_alpha(new_alpha)
        return
        
    def build_page(self):
        st.write('# Ridge Regression')

        # Controls
        cols = st.columns(5)
        st.session_state['da'] = cols[1].selectbox(label='Step size', 
                                                   options = [0.001, 
                                                              0.01, 
                                                              0.1, 
                                                              1, 
                                                              10],
                                                   index=2
                                                   )
        cols[1].write('$\\alpha=' + str(self.get_alpha()) + '$')

        cols[0].button('Decrease $\\alpha$', on_click=self.decrease_alpha)
        cols[0].button('Increase $\\alpha$', on_click=self.increase_alpha)
        
        st.session_state['degree'] = cols[2].selectbox(label = 'Polynomial degree', 
                                                       options = list(range(1,11))
                                                       )
        
        # Update the regression with current settings
        self.model.p = st.session_state['degree']
        self.model.a = st.session_state['alpha']
        self.model.fit_model()

        # Create the figure
        self.model.make_curve()
        self.plotter = RegressionPlot(self.model)

        # placeholder
        fig, ax = plt.subplots(figsize=(4,4))
        st.pyplot(self.plotter.fig)
        return

class RegressionPlot:
    def __init__(self,
                 data: SomeRegression
                 ):
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        
        self.ax.scatter(self.data.x, self.data.y, color='r', label='data')
        self.ax.plot(self.data.x_model, self.data.y_model, color='k', label='model')

        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y$')
        self.ax.legend(loc='center left', bbox_to_anchor = [1,0.5])
        return

class SomeRegression:
    def __init__(self,
                 n_points = 10,
                 poly_degree = 6,
                 alpha = 1
                 ):
        self.n = n_points
        self.p = poly_degree
        self.a = alpha
        return

    def make_data(self):
        x = np.random.random(size=self.n)
        y = 2*x + np.random.normal(scale=0.2, size=self.n)
        self.x = x
        self.y = y
        return

    def fit_model(self):
        self.pf = PF(degree=self.p)
        X = self.pf.fit_transform(self.x.reshape(-1,1))
        ss = SS()
        X = ss.fit_transform(X)
        self.X = X
        self.ss = ss
        model = Ridge(alpha=self.a)
        model.fit(self.X,self.y)
        self.model = model
        return

    def make_curve(self, res=100):
        x_model = np.linspace(min(self.x.ravel()), max(self.x.ravel()), res)
        X_model = self.pf.transform(x_model.reshape(-1,1))
        X_model = self.ss.transform(X_model)
        self.x_model = x_model
        self.y_model = self.model.predict(X_model)
        return

if __name__ == '__main__':
    RegressionApp()