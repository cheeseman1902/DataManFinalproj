import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

st.header("Group 8 Final Project")
conn = sqlite3.connect("Cleaned_Mental_Health_data.db")