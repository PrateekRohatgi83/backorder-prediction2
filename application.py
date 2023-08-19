# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 18:08:21 2023

@author: Administrator
"""

import numpy as np
import pandas as pd
import pickle
import streamlit as st
import os,sys

loaded_model = pickle.load(open('E:/Project INEURON/backorder prediction/backorder-prediction2/trained_model.sav', 'rb'))
# print(type(loaded_model))
# sys.exit(0)
def predict_backorder(input_data):

    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    input_data = pd.DataFrame(input_data)
    prediction = list(loaded_model.predict(input_data_reshaped))
    
    # print(prediction)
    
    if (prediction[0] == 0):
        return 'No backorder'
    else:
        return 'Backorder'

        
def main():
  st.title("Backorder Prediction")
  
  national_inv = float(st.text_input("National Inventory",value = 1))
  in_transit_qty = float(st.text_input("in_transit_qty",value = 1))
  forecast_3_month = float(st.text_input("forecast_3_month",value=1))
  forecast_6_month = float(st.text_input("forecast_6_month",value = 1))
  forecast_9_month = float(st.text_input("forecast_9_month",value = 1))
  sales_1_month = float(st.text_input("sales_1_month",value = 1))
  sales_3_month = float(st.text_input("sales_3_month",value = 1))
  sales_6_month = float(st.text_input("sales_6_month",value = 1))
  sales_9_month = float(st.text_input("sales_9_month",value = 1))
  min_bank = float(st.text_input("min_bank",value = 1))
  potential_issue = float(st.text_input("potential_issue",value = 1))
  pieces_past_due = float(st.text_input("pieces_past_due",value = 1))
  perf_6_month_avg = float(st.text_input("perf_6_month_avg",value = 1))
  perf_12_month_avg = float(st.text_input("perf_12_month_avg",value = 1))
  local_bo_qty = float(st.text_input("local_bo_qty",value = 1))
  deck_risk = float(st.text_input("deck_risk",value = 1))
  oe_constraint = float(st.text_input("oe_constraint",value = 1))
  ppap_risk = float(st.text_input("ppap_risk",value = 1))
  stop_auto_buy = float(st.text_input("stop_auto_buy",value = 1))
  rev_stop = float(st.text_input("rev_stop",value = 1))
  
  result = ""
  if st.button("Predict"):
    result = predict_backorder([national_inv,in_transit_qty,forecast_3_month,forecast_6_month,forecast_9_month,sales_1_month,sales_3_month,sales_6_month,sales_9_month,min_bank,potential_issue,pieces_past_due,perf_6_month_avg,perf_12_month_avg,local_bo_qty,deck_risk,oe_constraint,ppap_risk,stop_auto_buy,rev_stop])
  st.success(result)
  
  if st.button("About"):
    st.text("Made by prateek")
    

if __name__ == '__main__':
    main()