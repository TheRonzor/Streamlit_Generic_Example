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
    DFLT_ALPHA = 0
    def __init__(self):
        self.alpha = 0
        self.build_page()
        return
    
    def set_alpha(self, alpha):
        st.session_state['alpha'] = round(alpha, 5)    
        return
    
    def get_alpha(self):
        if 'alpha' in st.session_state:
            return st.session_state['alpha']
        else:
            self.set_alpha(self.DFLT_ALPHA)
            return self.get_alpha()
    
    def get_da(self):
        print(self.da)
        return float(self.da)
    
    def increase_alpha(self):
        new_alpha = self.get_alpha() + self.get_da()
        print(new_alpha)
        self.set_alpha(new_alpha)
        return
    
    def decrease_alpha(self):
        new_alpha = self.get_alpha() - self.get_da()
        print(new_alpha)
        self.set_alpha(new_alpha)
        return
        
    def build_page(self):
        st.write('# Ridge Regression')

        # Alpha controls
        alpha_cols = st.columns(6)
        alpha_cols[0].write('   $\\alpha=$' + str(self.get_alpha()))
        self.da = alpha_cols[0].text_input(label='Step size', value=1)
        alpha_cols[1].write(' ')
        alpha_cols[1].button('Decrease $\\alpha$', on_click=self.decrease_alpha)
        alpha_cols[1].button('Increase $\\alpha$', on_click=self.increase_alpha) 
        
        # placeholder
        fig, ax = plt.subplots(figsize=(4,4))
        st.pyplot(fig)
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

        self.make_data()
        self.fit_model()
        self.make_curve()
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