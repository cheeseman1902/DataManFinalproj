import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

st.header("Group 8 Final Project")
conn = sqlite3.connect("Mental_Health_data.db")

st.subheader('Tabbed Questions by person')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Julia", "Mac", "David", "Koise", "Chris"])

with tab1:
    st.header("Julia's Questions")

with tab2:
    st.header("Mac's Questions")

with tab3:
    st.header("David's Questions")

with tab1:
    st.header("Koise's Questions")

with tab1:
    st.header("Chris's Questions")