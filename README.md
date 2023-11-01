# Streamlit: Some Generic Examples

This repository contains several [Streamlit](https://streamlit.io/) applications meant to help get you started.

**Important**: You do not run these like you usually run python scripts. Instead, the syntax you'll use from the command line is like:

```streamlit run my_app.py```

In order of increasing code complexity:

- main_dot.py
  - A scatter plot with a dot, and some buttons you can use to move the dot around
- main_reg.py
  - An interactive Ridge regression. The data is randomly generated each time you refresh the page. You can select the degree of a polynomial regression model which is intended to initially overfit the data, and then see how increasing the strength of the regularization reduces the complexity of the model.
- main_store.py
  - A sample dashboard linked to a sqlite database. The rest of the code and data for this app is found in the ```src/``` directory
    - That code is split into three files:
      - my_plots.py: Code to create visualizations
      - my_db.py: Code to work with the database
      - my_app.py: Code to create the streamlit app
