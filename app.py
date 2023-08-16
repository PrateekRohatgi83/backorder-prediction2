# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GiO40NoYL3fXk4kC62HJmSwkPbS03Pty
"""

import numpy as np
import pickle
import pandas as pd
import streamlit as st

pickle_in = open("model.pkl","rb")
model = pickle.load(pickle_in)

def welcome():
    return "Welcome all"

def predict_backorder(national_inv, in_transit_qty, forecast_3_month, forecast_6_month, forecast_9_month, sales_1_month, sales_3_month, sales_6_month, sales_9_month, min_bank, potential_issue, pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop, went_on_backorder):
  prediction = model.predict([[national_inv, in_transit_qty, forecast_3_month, forecast_6_month, forecast_9_month, sales_1_month, sales_3_month, sales_6_month, sales_9_month, min_bank, potential_issue, pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop, went_on_backorder]])
  print(prediction)
  return prediction

def main():
  st.title("Backorder Prediction")
  html_temp = """
  <div style = "background-color:tomato;padding:10px">
  <h2 style = "color:white;text-align:center;"> Prateek Backorder Prediction </h2>
 """
  st.markdown(html_temp, unsafe_allow_html = True)
  national_inv = st.text_input("National Inventory","Type Here")
  in_transit_qty = st.text_input("in_transit_qty","Type Here")
  forecast_3_month = st.text_input("forecast_3_month","Type Here")
  forecast_6_month = st.text_input("forecast_6_month","Type Here")
  forecast_9_month = st.text_input("forecast_9_month","Type Here")
  sales_1_month = st.text_input("sales_1_month","Type Here")
  sales_3_month = st.text_input("sales_3_month","Type Here")
  sales_6_month = st.text_input("sales_6_month","Type Here")
  sales_9_month = st.text_input("sales_9_month","Type Here")
  min_bank = st.text_input("min_bank","Type Here")
  potential_issue = st.text_input("potential_issue","Type Here")
  pieces_past_due = st.text_input("pieces_past_due","Type Here")
  perf_6_month_avg = st.text_input("perf_6_month_avg","Type Here")
  perf_12_month_avg = st.text_input("perf_12_month_avg","Type Here")
  local_bo_qty = st.text_input("local_bo_qty","Type Here")
  deck_risk = st.text_input("deck_risk","Type Here")
  oe_constraint = st.text_input("oe_constraint","Type Here")
  ppap_risk = st.text_input("ppap_risk","Type Here")
  stop_auto_buy = st.text_input("stop_auto_buy","Type Here")
  rev_stop = st.text_input("rev_stop","Type Here")
  result = ""
  if st.button("Predict"):
    result = predict_backorder(national_inv, in_transit_qty, forecast_3_month, forecast_6_month, forecast_9_month, sales_1_month, sales_3_month, sales_6_month, sales_9_month, min_bank, potential_issue, pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop, went_on_backorder)
  st.success("The output is {}".format(result))
  if st.button("About"):
    st.text("Made by prateek")

if __name__=='__main__':
  main()