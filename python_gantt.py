#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 22:20:36 2022

"""

import plotly.express as px
import pandas as pd
import numpy as np



df = pd.DataFrame([
    dict(Task="Task 1", Start='2023-01-01', Finish='2023-01-31'),
    dict(Task="Task 2", Start='2023-02-01', Finish='2023-02-28')


    #dict(task = "asdf", Start = 'YYYY-M-D', Finsih = 'YYYY-MM-DD')
    
    # prints out locally
    # auto-timescales


])

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

fig.show()
