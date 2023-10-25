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
    def __init__(self):
        self.alpha = 0
        self.build_page()
        return
    
    def build_page(self):
        st.write('# Ridge Regression')

        cols = st.columns([1,1])
        alpha_cols = cols[0].columns(3)
        alpha_cols[0].button('Decrease $\\alpha$')
        alpha_cols[1].write('$\\alpha=' + str(self.alpha) + '$')
        alpha_cols[2].button('Increase $\\alpha$') 

        # placeholder
        fig,ax = plt.subplots(figsize=(4,4))
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