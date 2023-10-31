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
        st.write('''Random data will be generated each time the page is reloaded. 
                 The true pattern will always be a line with a slope of 2, an intercept of 0, and some Gaussian noise with
                 $\\sigma=0.2$ will be added to $y$.
                 Here you can explore the effects of Ridge regularization in removing/reducing
                 the higher order terms in a polynomial mdoel that initially overfits the data.
                 ''')

        # Controls
        cols = st.columns(5)
        st.session_state['da'] = cols[1].selectbox(label='Step size', 
                                                   options = [0.0001,
                                                              0.001, 
                                                              0.01, 
                                                              0.1, 
                                                              1, 
                                                              10,
                                                              100],
                                                   index=0
                                                   )
        cols[1].write('$\\alpha=' + str(self.get_alpha()) + '$')

        cols[0].button('Decrease $\\alpha$', on_click=self.decrease_alpha)
        cols[0].button('Increase $\\alpha$', on_click=self.increase_alpha)
        
        degree_options = list(range(1,11))
        st.session_state['degree'] = cols[2].selectbox(label = 'Polynomial degree', 
                                                       options = degree_options,
                                                       index = len(degree_options)-1)
        
        # Update the regression with current settings
        self.model.p = st.session_state['degree']
        self.model.a = st.session_state['alpha']
        self.model.fit_model()

        # Show equation
        st.write('When coefficients round to 0 within 2 decimals, they will no longer be displayed:')
        st.write(self.model.get_equation())

        # Create the figure
        self.model.make_plot_data()
        self.plotter = RegressionPlot(self.model)

        # Create some columns (figure is too big)
        plot_cols = st.columns([1,5,1])
        plot_cols[1].pyplot(self.plotter.fig, use_container_width=True)
        return

class RegressionPlot:
    def __init__(self,
                 data: SomeRegression
                 ):
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        
        self.ax.scatter(self.data.X_data, self.data.y, color='r', label='data')
        self.ax.plot(self.data.x_model, self.data.y_model, color='k', label='model')

        #self.ax.set_xlabel('$x$')
        #self.ax.set_ylabel('$y$')

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        padding = 0.1
        self.ax.set_xlim([self.data.xmin-padding, 
                          self.data.xmax+padding])
        self.ax.set_ylim([min(self.data.y)-padding, 
                          max(self.data.y)+padding])

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
        y = 1 + 2*x + np.random.normal(scale=0.2, size=self.n)
        self.x = x
        self.y = y
        return

    def fit_model(self):
        self.pf = PF(degree=self.p)
        self.ss = SS()
        X = self.pf.fit_transform(self.x.reshape(-1,1))
        X = self.ss.fit_transform(X)
        self.X = X
        model = Ridge(alpha=self.a)
        model.fit(self.X,self.y)
        self.model = model
        return

    def make_plot_data(self, res=500):
        self.X_data = self.X[:,1]
        self.xmin = min(self.X_data)
        self.xmax = max(self.X_data)
        self.xmodel = np.linspace(self.xmin, self.xmax, res)
        X = self.pf.transform(self.xmodel.reshape(-1,1))
        X = self.ss.transform(X)

        self.y_model = self.model.predict(X)
        self.x_model = X[:,1]
        return
    
    def get_equation(self, fmt='.2f'):
        eq = '$y \\approx' + format(self.model.intercept_, fmt)
        for p,c in enumerate(self.model.coef_[1:]):
            if round(abs(c),2) > 0:
                if p == 0:
                    eq += '+' + format(c, fmt) + 'x'
                else:
                    eq += '+' + format(c, fmt) + 'x^{' + str(p+1) + '}'
        eq += '$'
        eq = eq.replace('+-', '-')
        return eq

if __name__ == '__main__':
    RegressionApp()