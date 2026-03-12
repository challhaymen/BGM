import datetime
import re

import streamlit as st
import numpy as np
import pandas as pd

if 'warnings_list' not in st.session_state:
   st.session_state['warnings_list'] = []

if 'errors_list' not in st.session_state:
   st.session_state['errors_list'] = []

if 'df_flights' not in st.session_state:
    st.session_state['df_flights'] = None

if 'df_flights_to_edit' not in st.session_state:
    st.session_state['df_flights_to_edit'] = None

if 'df_aircrafts' not in st.session_state:
    st.session_state['df_aircrafts'] = None

if 'threshold_low' not in st.session_state:
    st.session_state['threshold_low'] = None

if 'threshold_med' not in st.session_state:
    st.session_state['threshold_med'] = None

if 'color_low' not in st.session_state:
    st.session_state['color_low'] = None

if 'color_med' not in st.session_state:
    st.session_state['color_med'] = None

if 'color_high' not in st.session_state:
    st.session_state['color_high'] = None

if 'df_final' not in st.session_state:
    st.session_state['df_final'] = None

if 'cross_matrix' not in st.session_state:
   st.session_state['cross_matrix'] = None

if 'df_final_wp' not in st.session_state:
    st.session_state['df_final_wp'] = None

if 'df_final_wp_to_edit' not in st.session_state:
    st.session_state['df_final_wp_to_edit'] = None

if 'cross_matrix_wp' not in st.session_state:
   st.session_state['cross_matrix_wp'] = None

def get_departure_airport_list():
    if st.session_state['df_aircrafts'] is None:
        return []
    else:
       return list(st.session_state['df_aircrafts']['departure_airport'].unique())
    
def get_arrival_airport_list():
    if st.session_state['df_aircrafts'] is None:
        return []
    else:
       return list(st.session_state['df_aircrafts']['arrival_airport'].unique())
    
def get_aircraft_code_list():
   if st.session_state['df_aircrafts'] is None:
      return []
   else:
      return list(st.session_state['df_aircrafts']['aircraft_code'].unique())
   
def get_new_flight_id(df_flights):
   return 'FL' + (6 - len(str(df_flights['flight_id'].str[2:].astype(int).max() + 1))) * '0' + str(df_flights['flight_id'].str[2:].astype(int).max() + 1)

def reset_df_flights():
   st.session_state['df_flights'] = None

def reset_df_aircrafts():
   st.session_state['df_aircrafts'] = None

def handle_df_flights_change():
   
    df_flights_state = st.session_state['df_flights_editor']

    for row_index, updates in df_flights_state['edited_rows'].items():

        flight_code_mask = st.session_state['df_flights_to_edit'].loc[row_index, 'flight_code']
        departure_date_mask = st.session_state['df_flights_to_edit'].loc[row_index, 'departure_date'] 

        st.write(f"Row Index: {row_index}, flight_code: {flight_code_mask}, departure_date: {departure_date_mask}")

        for column_name, new_value in updates.items():
            if column_name == 'departure_airport':
                departure_airport = new_value
                arrival_airport = st.session_state['df_flights_to_edit'].loc[row_index, 'arrival_airport']
                aircraft_code = st.session_state['df_flights_to_edit'].loc[row_index, 'aircraft_code']

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'departure_airport'] = new_value

            if column_name == 'arrival_airport':
                departure_airport = st.session_state['df_flights_to_edit'].loc[row_index, 'departure_airport']
                arrival_airport = new_value
                aircraft_code = st.session_state['df_flights_to_edit'].loc[row_index, 'aircraft_code']

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'arrival_airport'] = new_value

            if column_name == 'aircraft_code':
                departure_airport = st.session_state['df_flights_to_edit'].loc[row_index, 'departure_airport']
                arrival_airport = st.session_state['df_flights_to_edit'].loc[row_index, 'arrival_airport']
                aircraft_code = new_value

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'aircraft_code'] = new_value

            # if column_name == 'departure_date':
                
            if column_name == 'economy_pax_load':
                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_pax_load'] = new_value
                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_pax_count'] = np.floor((new_value / 100 ) * st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_capacity'])
            # elif column_name == 'economy_pax_count':
            #    st.session_state['df_flights'].at[row_index, 'economy_pax']

            if column_name == 'business_pax_load':
               st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_pax_load'] = new_value
               st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_pax_count'] = np.floor((new_value / 100) * st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_capacity'])

            if column_name == 'economy_avg_bag_weight':
               st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_avg_bag_weight'] = new_value

            if column_name == 'business_avg_bag_weight':
               st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_avg_bag_weight'] = new_value

            if column_name == 'flight_status':
                if new_value == 'scheduled':
                    if not st.session_state['df_flights'][(st.session_state['df_flights']['flight_code'] == flight_code_mask) & 
                                                                              (st.session_state['df_flights']['departure_date'] == departure_date_mask) & 
                                                                              (st.session_state['df_flights']['flight_status'] == 'scheduled')].empty:
                        st.session_state['errors_list'].append("Impossible d'avoir plus d'un vol planifié avec meme Code Vol et Date Départ")
                else:
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'flight_status'] = new_value

    # st.session_state['df_final'] = None
    # st.session_state['cross_matrix'] = None

def handle_df_final_wp_change():

    df_final_wp_state = st.session_state['df_final_wp_editor']

    for row_index, updates in df_final_wp_state['edited_rows'].items():

        flight_code_mask = st.session_state['df_final_wp_to_edit'].loc[row_index, 'flight_code']
        departure_date_mask = st.session_state['df_final_wp_to_edit'].loc[row_index, 'departure_date']

        for column_name, new_value in updates.items():
            if column_name == 'departure_airport':
                departure_airport = new_value
                arrival_airport = st.session_state['df_final_wp_to_edit'].loc[row_index, 'arrival_airport']
                aircraft_code = st.session_state['df_final_wp_to_edit'].loc[row_index, 'aircraft_code']

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'departure_airport'] = new_value
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'departure_airport'] = new_value

            if column_name == 'arrival_airport':
                departure_airport = st.session_state['df_final_wp_to_edit'].loc[row_index, 'departure_airport']
                arrival_airport = new_value
                aircraft_code = st.session_state['df_final_wp_to_edit'].loc[row_index, 'aircraft_code']

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'arrival_airport'] = new_value
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'arrival_airport'] = new_value
                
            if column_name == 'aircraft_code':
                departure_airport = st.session_state['df_final_wp_to_edit'].loc[row_index, 'departure_airport']
                arrival_airport = st.session_state['df_final_wp_to_edit'].loc[row_index, 'arrival_airport']
                aircraft_code = new_value

                if st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'aircraft_code'] = new_value
                    st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'aircraft_code'] = new_value
                
            if column_name == 'economy_pax_load':
                
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'economy_pax_load'] = new_value
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'economy_pax_count'] = np.floor((new_value / 100 ) * st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'economy_capacity'])

                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_pax_load'] = new_value
                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_pax_count'] = st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'economy_pax_count']
                
            if column_name == 'business_pax_load':

                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'business_pax_load'] = new_value
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'business_pax_count'] = np.floor((new_value / 100) * st.session_state['df_final_wp'].loc[row_index, 'business_capacity'])

                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_pax_load'] = new_value
                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_pax_count'] = st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'business_pax_count']
                
            if column_name == 'economy_avg_bag_weight':
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'economy_avg_bag_weight'] = new_value

                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'economy_avg_bag_weight'] = new_value
                
            if column_name == 'business_avg_bag_weight':
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'business_avg_bag_weight'] = new_value

                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'business_avg_bag_weight'] = new_value
                
            if column_name == 'flight_status':
                st.session_state['df_final_wp'].loc[(st.session_state['df_final_wp']['flight_code'] == flight_code_mask) & (st.session_state['df_final_wp']['departure_date'] == departure_date_mask), 'flight_status'] = new_value

                st.session_state['df_flights'].loc[(st.session_state['df_flights']['flight_code'] == flight_code_mask) & (st.session_state['df_flights']['departure_date'] == departure_date_mask), 'flight_status'] = new_value
                

def run_algo_without_period(df_flights, df_aircrafts):

    df_flights = df_flights[df_flights['flight_status'] == 'scheduled'].copy()

    df_flights.insert(loc=8, column='departure_datetime', value=pd.to_datetime(df_flights['departure_date'] + ' ' + df_flights['departure_time']))
    df_flights.insert(loc=9, column='arrival_datetime', value=pd.to_datetime(df_flights['arrival_date'] + ' ' + df_flights['arrival_time']))

    df_flights.insert(loc=10, column='week', value=df_flights['departure_datetime'].dt.isocalendar().week)
    df_flights['week'] = 'Semaine ' + df_flights['week'].astype(str)

    df_flights.insert(loc=18, column='total_pax_count', value=np.floor((df_flights['economy_pax_load'] / 100) * df_flights['economy_capacity']) + np.floor((df_flights['business_pax_load'] / 100) * df_flights['business_capacity']))

    df_flights['economy_total_bag_weight'] = np.floor((df_flights['economy_pax_load'] / 100) * df_flights['economy_capacity']) * df_flights['economy_avg_bag_weight']
    df_flights['business_total_bag_weight'] = np.floor((df_flights['business_pax_load'] / 100) * df_flights['business_capacity']) * df_flights['business_avg_bag_weight']

    df_flights['economy_total_bag_weight_backlog_prev_flight'] = 0
    df_flights['economy_total_bag_weight_backlog_prev_flight'] = df_flights['economy_total_bag_weight_backlog_prev_flight'].astype(float)
    df_flights['business_total_bag_weight_backlog_prev_flight'] = 0
    df_flights['business_total_bag_weight_backlog_prev_flight'] = df_flights['business_total_bag_weight_backlog_prev_flight'].astype(float)

    df_flights['economy_total_bag_weight_backlog_prev_flight_added'] = 0
    df_flights['economy_total_bag_weight_backlog_prev_flight_added'] = df_flights['economy_total_bag_weight_backlog_prev_flight_added'].astype(float)
    df_flights['business_total_bag_weight_backlog_prev_flight_added'] = 0
    df_flights['business_total_bag_weight_backlog_prev_flight_added'] = df_flights['business_total_bag_weight_backlog_prev_flight_added'].astype(float)

    df_flights['economy_total_bag_weight_charged'] = 0
    df_flights['economy_total_bag_weight_charged'] = df_flights['economy_total_bag_weight_charged'].astype(float)
    df_flights['business_total_bag_weight_charged'] = 0
    df_flights['business_total_bag_weight_charged'] = df_flights['business_total_bag_weight_charged'].astype(float)

    df_flights['economy_total_bag_weight_backlog'] = 0
    df_flights['economy_total_bag_weight_backlog'] = df_flights['economy_total_bag_weight_backlog'].astype(float)
    df_flights['business_total_bag_weight_backlog'] = 0
    df_flights['business_total_bag_weight_backlog'] = df_flights['business_total_bag_weight_backlog'].astype(float)

    df_joined = df_flights.merge(df_aircrafts, on=['aircraft_code', 'departure_airport', 'arrival_airport'], how='inner')

    df_joined = df_joined[(df_joined['total_pax_count'] >= df_joined['pax_count_lower_bound']) & (df_joined['total_pax_count'] <= df_joined['pax_count_upper_bound'])]

    df_joined.reset_index(inplace=True, drop=True)

    economy_total_bag_weight_backlog = 0

    df_final = pd.DataFrame(columns=df_joined.columns)

    modified_groups = []

    for (departure_airport, arrival_airport, week), group in df_joined.groupby(['departure_airport', 'arrival_airport', 'week']):

        group = group.sort_values(by='departure_datetime')

        group.reset_index(inplace=True, drop=True)

        group.loc[0, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[0, 'economy_total_bag_weight'] + group.loc[0, 'economy_total_bag_weight_backlog_prev_flight']
        group.loc[0, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[0, 'business_total_bag_weight'] + group.loc[0, 'business_total_bag_weight_backlog_prev_flight']

        economy_total_bag_weight_backlog = 0

        for i in range(len(group)):

            if i == len(group) - 1:
                if (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) > group.loc[i, 'max_total_bag_weight']:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'max_total_bag_weight'] - group.loc[i, 'business_total_bag_weight_charged']

                    economy_total_bag_weight_backlog = (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) - group.loc[i, 'max_total_bag_weight']
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                else:
                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added']

                    economy_total_bag_weight_backlog = 0
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

            else:
                if (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) > group.loc[i, 'max_total_bag_weight']:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'max_total_bag_weight'] - group.loc[i, 'business_total_bag_weight_charged']

                    economy_total_bag_weight_backlog = (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) - group.loc[i, 'max_total_bag_weight']
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'economy_total_bag_weight_backlog']
                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'economy_total_bag_weight'] + group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight']

                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'business_total_bag_weight_backlog']
                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'business_total_bag_weight'] + group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight']

                else:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added']

                    economy_total_bag_weight_backlog = 0
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'economy_total_bag_weight_backlog']
                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'economy_total_bag_weight'] + group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight']

                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'business_total_bag_weight_backlog']
                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'business_total_bag_weight'] + group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight']

        modified_groups.append(group)

    df_final = pd.concat(modified_groups, axis=0, ignore_index=True)

    return df_final

def color_backlog(val):
    if pd.isna(val):
        return ''
    if val < st.session_state['threshold_low']:
        return f"background-color: {st.session_state['color_low']}; color: black"
    elif val < st.session_state['threshold_med']:
        return f"background-color: {st.session_state['color_med']}; color: black"
    else:
        return f"background-color: {st.session_state['color_high']}; color: black"

def calculate_cross_matrix(df_final):
   
    df_aggregated = df_final.groupby(['departure_airport', 'arrival_airport', 'week']).agg({'economy_total_bag_weight_backlog': 'sum', 
                                                                                                  'business_total_bag_weight_backlog': 'sum'})

    df_aggregated['total_bag_weight_backlog'] = df_aggregated['economy_total_bag_weight_backlog'] + df_aggregated['business_total_bag_weight_backlog']

    cross_matrix = pd.pivot_table(data=df_aggregated, values=['economy_total_bag_weight_backlog', 'business_total_bag_weight_backlog', 'total_bag_weight_backlog'], index=['departure_airport', 'arrival_airport'], columns=['week'])

    cross_matrix = cross_matrix.sort_index(axis=1, key=lambda idx: idx.map(lambda x: int(x.split(' ')[1]) if 'Semaine' in x else x))

    return cross_matrix

def run_algo_with_period(df_flights, df_aircrafts, period_start_date=None, period_end_date=None):

    if period_start_date is None:
        period_start_date = pd.to_datetime(df_flights['departure_date']).min()
    else:
        period_start_date = pd.to_datetime(period_start_date)

    if period_end_date is None:
        period_end_date = pd.to_datetime(df_flights['departure_date']).max()
    else:
        period_end_date = pd.to_datetime(period_end_date)

    df_flights = df_flights[(pd.to_datetime(df_flights['departure_date']) >= period_start_date) & (pd.to_datetime(df_flights['departure_date']) <= period_end_date)].copy()

    df_flights = df_flights[df_flights['flight_status'] == 'scheduled']

    df_flights.insert(loc=8, column='departure_datetime', value=pd.to_datetime(df_flights['departure_date'] + ' ' + df_flights['departure_time']))
    df_flights.insert(loc=9, column='arrival_datetime', value=pd.to_datetime(df_flights['arrival_date'] + ' ' + df_flights['arrival_time']))

    df_flights.insert(loc=10, column='week', value=df_flights['departure_datetime'].dt.isocalendar().week)
    df_flights['week'] = 'Semaine ' + df_flights['week'].astype(str)

    df_flights.insert(loc=18, column='total_pax_count', value=np.floor((df_flights['economy_pax_load'] / 100) * df_flights['economy_capacity']) + np.floor((df_flights['business_pax_load'] / 100) * df_flights['business_capacity']))

    df_flights['economy_total_bag_weight'] = np.floor((df_flights['economy_pax_load'] / 100) * df_flights['economy_capacity']) * df_flights['economy_avg_bag_weight']
    df_flights['business_total_bag_weight'] = np.floor((df_flights['business_pax_load'] / 100) * df_flights['business_capacity']) * df_flights['business_avg_bag_weight']

    df_flights['economy_total_bag_weight_backlog_prev_flight'] = 0
    df_flights['economy_total_bag_weight_backlog_prev_flight'] = df_flights['economy_total_bag_weight_backlog_prev_flight'].astype(float)
    df_flights['business_total_bag_weight_backlog_prev_flight'] = 0
    df_flights['business_total_bag_weight_backlog_prev_flight'] = df_flights['business_total_bag_weight_backlog_prev_flight'].astype(float)

    df_flights['economy_total_bag_weight_backlog_prev_flight_added'] = 0
    df_flights['economy_total_bag_weight_backlog_prev_flight_added'] = df_flights['economy_total_bag_weight_backlog_prev_flight_added'].astype(float)
    df_flights['business_total_bag_weight_backlog_prev_flight_added'] = 0
    df_flights['business_total_bag_weight_backlog_prev_flight_added'] = df_flights['business_total_bag_weight_backlog_prev_flight_added'].astype(float)

    df_flights['economy_total_bag_weight_charged'] = 0
    df_flights['economy_total_bag_weight_charged'] = df_flights['economy_total_bag_weight_charged'].astype(float)
    df_flights['business_total_bag_weight_charged'] = 0
    df_flights['business_total_bag_weight_charged'] = df_flights['business_total_bag_weight_charged'].astype(float)

    df_flights['economy_total_bag_weight_backlog'] = 0
    df_flights['economy_total_bag_weight_backlog'] = df_flights['economy_total_bag_weight_backlog'].astype(float)
    df_flights['business_total_bag_weight_backlog'] = 0
    df_flights['business_total_bag_weight_backlog'] = df_flights['business_total_bag_weight_backlog'].astype(float)

    df_joined = df_flights.merge(df_aircrafts, on=['aircraft_code', 'departure_airport', 'arrival_airport'], how='inner')

    df_joined = df_joined[(df_joined['total_pax_count'] >= df_joined['pax_count_lower_bound']) & (df_joined['total_pax_count'] <= df_joined['pax_count_upper_bound'])]

    df_joined.reset_index(inplace=True, drop=True)

    economy_total_bag_weight_backlog = 0

    df_final = pd.DataFrame(columns=df_joined.columns)

    modified_groups = []

    for (departure_airport, arrival_airport), group in df_joined.groupby(['departure_airport', 'arrival_airport']):

        group = group.sort_values(by='departure_datetime')

        group.reset_index(inplace=True, drop=True)

        group.loc[0, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[0, 'economy_total_bag_weight'] + group.loc[0, 'economy_total_bag_weight_backlog_prev_flight']
        group.loc[0, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[0, 'business_total_bag_weight'] + group.loc[0, 'business_total_bag_weight_backlog_prev_flight']

        economy_total_bag_weight_backlog = 0

        for i in range(len(group)):

            if i == len(group) - 1:
                if (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) > group.loc[i, 'max_total_bag_weight']:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'max_total_bag_weight'] - group.loc[i, 'business_total_bag_weight_charged']

                    economy_total_bag_weight_backlog = (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) - group.loc[i, 'max_total_bag_weight']
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                else:
                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added']

                    economy_total_bag_weight_backlog = 0
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

            else:
                if (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) > group.loc[i, 'max_total_bag_weight']:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'max_total_bag_weight'] - group.loc[i, 'business_total_bag_weight_charged']

                    economy_total_bag_weight_backlog = (group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added'] + group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']) - group.loc[i, 'max_total_bag_weight']
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'economy_total_bag_weight_backlog']
                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'economy_total_bag_weight'] + group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight']

                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'business_total_bag_weight_backlog']
                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'business_total_bag_weight'] + group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight']

                else:

                    group.loc[i, 'business_total_bag_weight_charged'] = group.loc[i, 'business_total_bag_weight_backlog_prev_flight_added']
                    group.loc[i, 'economy_total_bag_weight_charged'] = group.loc[i, 'economy_total_bag_weight_backlog_prev_flight_added']

                    economy_total_bag_weight_backlog = 0
                    group.loc[i, 'economy_total_bag_weight_backlog'] = economy_total_bag_weight_backlog

                    group.loc[i, 'business_total_bag_weight_backlog'] = 0

                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'economy_total_bag_weight_backlog']
                    group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'economy_total_bag_weight'] + group.loc[i + 1, 'economy_total_bag_weight_backlog_prev_flight']

                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight'] = group.loc[i, 'business_total_bag_weight_backlog']
                    group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight_added'] = group.loc[i + 1, 'business_total_bag_weight'] + group.loc[i + 1, 'business_total_bag_weight_backlog_prev_flight']

        modified_groups.append(group)

    df_final = pd.concat(modified_groups, axis=0, ignore_index=True)

    return df_final

def calculate_cross_matrix_with_period(df_final):
   
    df_aggregated = df_final.groupby(['departure_airport', 'arrival_airport']).agg({'economy_total_bag_weight_backlog': 'sum', 
                                                                                                  'business_total_bag_weight_backlog': 'sum'})

    df_aggregated['total_bag_weight_backlog'] = df_aggregated['economy_total_bag_weight_backlog'] + df_aggregated['business_total_bag_weight_backlog']

    cross_matrix = pd.pivot_table(data=df_aggregated, values=['economy_total_bag_weight_backlog', 'business_total_bag_weight_backlog', 'total_bag_weight_backlog'], index=['departure_airport', 'arrival_airport'])

    return cross_matrix

def check_form_necessary_fields(fields):
    for field in fields:
        if field is None:
            return True
    return False

st.set_page_config(page_title='Système de Simulation de Bagages', layout='wide')

st.markdown("""
    <style>
            /* Page background */
            .stApp {
                background-color: #f7f7f7;
            }

            /* Sidebar background */
            [data-testid="stSidebar"] {
                background-color: #f3f3f3;
            }

            /* File Uploader */
            [data-testid="stFileUploaderDropzone"] {
                background-color: #f7f7f7;
            }

            /* st.info background */
            [data-testid="stAlert"] {
                background-color: #c0a1b2;
                border-radius: 10px;
            }

            [data-testid="stAlert"] p {
                color: #8d5f7b;
            }

            /*  */
    <\style>
""", unsafe_allow_html=True)

st.title('Système de Simulation de Bagages')
st.markdown("---")

st.sidebar.header("Charger les fichiers des données")
flights_file = st.sidebar.file_uploader("Charger le fichier Flights", type=['csv'], on_change=reset_df_flights)
aircrafts_file = st.sidebar.file_uploader("Charger le fichier Aircrafts", type=['csv'], on_change=reset_df_aircrafts)

st.sidebar.markdown("---")
st.sidebar.header("Couleurs Backlog")
st.session_state['color_low'] = st.sidebar.color_picker("Couleur Bas (en dessous seuil bas)", value='#02B707')
st.session_state['color_med'] = st.sidebar.color_picker("Couleur Moyen (entre seuil bas et moyen)", value='#FB8B0F')
st.session_state['color_high'] = st.sidebar.color_picker("Couleur Haut (en dessus du seuil moyen)", value='#FD0202') # c10130

st.sidebar.markdown("---")
st.sidebar.header("Seuils Backlog")
st.session_state['threshold_low'] = st.sidebar.number_input("Entrer le seuil bas", min_value=0, value=250)
st.session_state['threshold_med'] = st.sidebar.number_input("Entrer le seuil moyen", min_value=0, value=600)
st.sidebar.markdown(
    f'<div style="display: flex; flex-direction: column; gap: 6px; margin-top: 8px;">'
    f'  <div style="display: flex; align-items: center; gap: 10px;">'
    f'    <div style="background-color: {st.session_state["color_low"]}; width: 30px; height: 30px; border-radius: 4px; flex-shrink: 0;"></div>'
    f'    <span>Bas : &lt; {st.session_state["threshold_low"]} kg</span>'
    f'  </div>'
    f'  <div style="display: flex; align-items: center; gap: 10px;">'
    f'    <div style="background-color: {st.session_state["color_med"]}; width: 30px; height: 30px; border-radius: 4px; flex-shrink: 0;"></div>'
    f'    <span>Moyen : {st.session_state["threshold_low"]} – {st.session_state["threshold_med"]} kg</span>'
    f'  </div>'
    f'  <div style="display: flex; align-items: center; gap: 10px;">'
    f'    <div style="background-color: {st.session_state["color_high"]}; width: 30px; height: 30px; border-radius: 4px; flex-shrink: 0;"></div>'
    f'    <span>Haut : ≥ {st.session_state["threshold_med"]} kg</span>'
    f'  </div>'
    f'</div>',
    unsafe_allow_html=True
)

if flights_file is None or aircrafts_file is None:

    st.info("Veuillez charger les deux fichiers pour commencer la simulation.")

    with st.expander("Format attendu"):
        st.markdown("""
        **Flights CSV :** flight_id, flight_code, flight_status, departure_date, departure_time,
        departure_airport, arrival_date, arrival_time, arrival_airport, aircraft_code,
        economy_capacity, economy_pax_load, business_capacity, business_pax_load,
        economy_avg_bag_weight, business_avg_bag_weight

        **Aircrafts CSV :** aircraft_code, departure_airport, arrival_airport,
        max_total_bag_weight, pax_count_lower_bound, pax_count_upper_bound
        """)

    if flights_file is None:
        st.session_state['df_flights'] = None

    if aircrafts_file is None:
        st.session_state['df_aircrafts'] = None

else:

    try:
        if st.session_state['df_flights'] is None:    
            st.session_state['df_flights'] = pd.read_csv(flights_file)
        if st.session_state['df_aircrafts'] is None:
            st.session_state['df_aircrafts'] = pd.read_csv(aircrafts_file)
    except Exception as e:
        st.error(f"Erreur lors du chargement des fichiers: {e}")

    tab1, tab2, tab3 = st.tabs(['Tables', 'Simulation Standard', 'Simulation par Période'])

    with tab1:
        flights_column_config = {
            'flight_id': st.column_config.TextColumn(label='flight_id', disabled=True, required=True),
            'flight_code': st.column_config.TextColumn(label='flight_code', disabled=True, required=True),
            'departure_airport': st.column_config.SelectboxColumn(label='departure_airport', required=True, options=sorted(get_departure_airport_list())), 
            'arrival_airport': st.column_config.SelectboxColumn(label='arrival_airport', required=True, options=sorted(get_arrival_airport_list())), 
            'departure_date': st.column_config.TextColumn(label='departure_date', required=True, disabled=True),
            'arrival_date': st.column_config.TextColumn(label='arrival_date', required=True, disabled=True),  
            # check departure_date < arrival_date
            'departure_time': st.column_config.TextColumn(label='departure_time', required=True, disabled=True), 
            'arrival_time': st.column_config.TextColumn(label='arrival_time', required=True, disabled=True), 
            # check departure_time < arrival_time
            'aircraft_code': st.column_config.SelectboxColumn(label='aircraft_code', required=True, options=get_aircraft_code_list()), 
            'economy_capacity': st.column_config.NumberColumn(label='economy_capacity', required=True, disabled=True), 
            'economy_pax_load': st.column_config.NumberColumn(label='economy_pax_load', min_value=0, max_value=100, required=True), 
            'economy_pax_count': st.column_config.NumberColumn(label='economy_pax_count', required=True, disabled=True), 
            'business_capacity': st.column_config.NumberColumn(label='business_capacity', required=True, disabled=True), 
            'business_pax_load': st.column_config.NumberColumn(label='business_pax_load', min_value=0, max_value=100, required=True),
            'business_pax_count': st.column_config.NumberColumn(label='business_pax_count', required=True, disabled=True), 
            # 'economy_avg_bag_count': st.column_config.NumberColumn(label='economy_avg_bag_count', disabled=True), 
            # 'business_avg_bag_count': st.column_config.NumberColumn(label='business_avg_bag_count', disabled=True), 
            'economy_avg_bag_weight': st.column_config.NumberColumn(label='economy_avg_bag_weight', min_value=0, required=True), 
            'business_avg_bag_weight': st.column_config.NumberColumn(label='business_avg_bag_weight', min_value=0, required=True), 
            'flight_status': st.column_config.SelectboxColumn(label='flight_status', options=['scheduled', 'cancelled'], default='scheduled', required=True)
        }

        st.subheader("Table Aircrafts")
        st.dataframe(st.session_state['df_aircrafts'], hide_index=True)

        st.subheader("Table Flights")

        col1, col2 = st.columns(2)
        
        df_flight_id_filter = col1.multiselect(label='Vol ID', options=st.session_state['df_flights']['flight_id'].unique(), accept_new_options=False, key='df_flight_id_filter')
        df_flight_code_filter = col2.multiselect(label='Code Vol', options=sorted(st.session_state['df_flights']['flight_code'].dropna().unique()), accept_new_options=False, key='df_flight_code_filter')
        df_flight_departure_airport_filter = col1.multiselect(label='Aéroport Départ', options=sorted(list(st.session_state['df_aircrafts']['departure_airport'].unique())), accept_new_options=False, key='df_flight_departure_airport_filter')
        df_flight_arrival_airport_filter = col2.multiselect(label='Aéroport Arrivé', options=sorted(list(st.session_state['df_aircrafts']['arrival_airport'].unique())), accept_new_options=False, key='df_flight_arrival_airport_filter')
        df_flight_use_min_departure_date_filter = col1.checkbox(label='Filtrer par Date Départ Minimale', key='df_flight_use_min_departure_date_filter')
        df_flight_min_departure_date_filter = col1.date_input(label='Date Départ Minimale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_flight_min_departure_date_filter')
        df_flight_use_max_departure_date_filter = col2.checkbox(label='Filtrer par Date Départ Maximale', key='df_flight_use_max_departure_date_filter')
        df_flight_max_departure_date_filter = col2.date_input(label='Date Départ Maximale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_flight_max_departure_date_filter')

        st.session_state['df_flights_to_edit'] = st.session_state['df_flights'].copy()

        if df_flight_id_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][st.session_state['df_flights_to_edit']['flight_id'].isin(df_flight_id_filter)]
        if df_flight_code_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][st.session_state['df_flights_to_edit']['flight_code'].isin(df_flight_code_filter)]
        if df_flight_departure_airport_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][st.session_state['df_flights_to_edit']['departure_airport'].isin(df_flight_departure_airport_filter)]
        if df_flight_arrival_airport_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][st.session_state['df_flights_to_edit']['arrival_airport'].isin(df_flight_arrival_airport_filter)]
        if df_flight_use_min_departure_date_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][pd.to_datetime(st.session_state['df_flights_to_edit']['departure_date']).dt.date >= df_flight_min_departure_date_filter]
        if df_flight_use_max_departure_date_filter:
            st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'][pd.to_datetime(st.session_state['df_flights_to_edit']['departure_date']).dt.date <= df_flight_max_departure_date_filter]

        st.session_state['df_flights_to_edit'] = st.session_state['df_flights_to_edit'].reset_index(drop=True)

        for warning in st.session_state['warnings_list']:
            st.warning(warning)

        for error in st.session_state['errors_list']:
           st.error(error)

        edited_df_flights = st.data_editor(st.session_state['df_flights_to_edit'], column_config=flights_column_config, on_change=handle_df_flights_change, key='df_flights_editor', hide_index=True)

        st.subheader("Ajouter un nouveau vol")

        @st.fragment()
        def add_new_flight():
        
            col1, col2 = st.columns(2)

            flight_code = col1.text_input(label='Code Vol', placeholder='AT###', max_chars=5, key='flight_code_input')
            aircraft_code = col2.selectbox(label='Type Machine', options=list(st.session_state['df_aircrafts']['aircraft_code'].unique()), accept_new_options=False, key='aircraft_code_input')
            departure_airport = col1.selectbox(label='Aéroport Départ', options=sorted(list(st.session_state['df_aircrafts']['departure_airport'].unique())), accept_new_options=False, key='departure_airport')
            arrival_airport = col2.selectbox(label='Aéroport Arrivé', options=sorted(list(st.session_state['df_aircrafts']['arrival_airport'].unique())), accept_new_options=False, key='arrival_airport_input')
            departure_date = col1.date_input(label='Date Départ', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='departure_date_input')
            arrival_date = col2.date_input(label='Date Arrivé', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='arrival_date')
            departure_time = col1.time_input(label='Temps Départ', step=60, key='departure_time_input')
            arrival_time = col2.time_input(label='Temps Arrivé', step=60, key='arrival_time_input')
            economy_capacity = col1.number_input(label='Capacité économique', min_value=0, value=0, key='economy_capacity_input')
            economy_pax_load = col2.number_input(label='Charge pax économique', min_value=0, max_value=100, value=0, key='economy_pax_load_input')
            business_capacity = col1.number_input(label='Capacité business', min_value=0, value=0, key='business_capacity_input')
            business_pax_load = col2.number_input(label='Charge pax business', min_value=0, max_value=100, value=0, key='business_pax_load_input')
            # economy_avg_bag_count = col1.number_input(label='Moyenne du nombre de bagages par passager en classe économique', min_value=0, disabled=True, value=1, key='economy_avg_bag_count_input')
            # business_avg_bag_count = col2.number_input(label='Moyenne du nombre de bagages par passager en classe business', min_value=0, disabled=True, value=1, key='business_avg_bag_count_input')
            economy_avg_bag_weight = col1.number_input(label='Moyenne du poids de bagages par passager en classe économique', min_value=0, value=23, key='economy_avg_bag_weight_input')
            business_avg_bag_weight = col2.number_input(label='Moyenne du poids de bagages par passager en classe business', min_value=0, value=32, key='business_avg_bag_weight_input')

            if st.button('Ajouter', key='add_new_flight_btn'):

                pattern = r"^AT\d{3}$"

                if not re.match(string=flight_code, pattern=pattern):
                    flight_code = None
                
                new_row = {
                    'flight_id': get_new_flight_id(st.session_state['df_flights']),
                    'flight_code': flight_code,
                    'departure_airport': departure_airport,
                    'arrival_airport': arrival_airport,
                    'departure_date': str(departure_date),
                    'arrival_date': str(arrival_date),
                    'departure_time': str(departure_time),
                    'arrival_time': str(arrival_time),
                    'aircraft_code': aircraft_code,
                    'economy_capacity': economy_capacity,
                    'economy_pax_load': economy_pax_load,
                    'economy_pax_count': np.floor((economy_pax_load / 100) * economy_capacity),
                    'business_capacity': business_capacity,
                    'business_pax_load': business_pax_load,
                    'business_pax_count': np.floor((business_pax_load / 100) * business_capacity),
                    # 'economy_avg_bag_count': economy_avg_bag_count,
                    # 'business_avg_bag_count': business_avg_bag_count,
                    'economy_avg_bag_weight': economy_avg_bag_weight,
                    'business_avg_bag_weight': business_avg_bag_weight,
                    'flight_status': 'scheduled'
                }

                if check_form_necessary_fields([flight_code, departure_airport, arrival_airport, departure_date, departure_time, aircraft_code]):

                    st.session_state['errors_list'].append("Champs nécessaires manquants: Code Vol, Aéroport Départ, Aéroport Arrivé, Date Départ, Temps Départ, Code d'Avion.")

                elif not st.session_state['df_flights'][(st.session_state['df_flights']['flight_code'] == flight_code) & 
                                                    (st.session_state['df_flights']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_flights']['flight_status'] == 'scheduled')].empty:
                    
                    st.session_state['errors_list'].append("Impossible d'avoir deux vols planifiés avec meme Code Vol et Date Départ")

                elif st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport) & 
                                                    (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport) & 
                                                    (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code)].empty:
                
                    st.session_state['warnings_list'].append(f"Flight ID: {new_row['flight_id']}: Combinaison de Origine: {departure_airport} ,Destination: {arrival_airport} et Type Machine: {aircraft_code} n'est pas disponible dans la table aircrafts")

                else:
                    st.session_state['df_flights'].loc[len(st.session_state['df_flights'])] = new_row

                st.rerun(scope='app')

        add_new_flight()

        st.subheader("Supprimer un vol")
        
        @st.fragment()
        def remove_flight():
            flight_code = st.selectbox(label='Code Vol', options=sorted(st.session_state['df_flights']['flight_code'].dropna().unique()), accept_new_options=False)
            departure_date = st.date_input(label='Date Départ', min_value=pd.to_datetime(st.session_state['df_flights']['departure_date']).min(), max_value=pd.to_datetime(st.session_state['df_flights']['departure_date']).max())
            flight_status = st.selectbox(label='Status Vol', options=['scheduled', 'cancelled'], accept_new_options=False)

            if st.button('Supprimer'):

                st.session_state['df_flights'] = st.session_state['df_flights'][~((st.session_state['df_flights']['flight_code'] == flight_code) & 
                                                                                (st.session_state['df_flights']['departure_date'] == str(departure_date)) & 
                                                                                (st.session_state['df_flights']['flight_status'] == flight_status))]

                st.rerun(scope='app')

        remove_flight()

    with tab2:
        if st.button("Démarrer la Simulation", type='primary'):

            st.session_state['df_final'] = run_algo_without_period(st.session_state['df_flights'].copy(), st.session_state['df_aircrafts'].copy())
            
            st.session_state['cross_matrix'] = calculate_cross_matrix(st.session_state['df_final'])

        if st.session_state['df_final'] is not None:

            st.subheader("Résultats Simulation")

            col1, col2 = st.columns(2)

            df_final_id_filter = col1.multiselect(label='Vol ID', options=st.session_state['df_flights']['flight_id'].unique(), accept_new_options=False, key='df_final_id_filter')
            df_final_code_filter = col2.multiselect(label='Code Vol', options=sorted(st.session_state['df_flights']['flight_code'].dropna().unique()), accept_new_options=False, key='df_final_code_filter')
            df_final_departure_airport_filter = col1.multiselect(label='Aéroport Départ', options=sorted(list(st.session_state['df_aircrafts']['departure_airport'].unique())), accept_new_options=False, key='df_final_departure_airport_filter')
            df_final_arrival_airport_filter = col2.multiselect(label='Aéroport Arrivé', options=sorted(list(st.session_state['df_aircrafts']['arrival_airport'].unique())), accept_new_options=False, key='df_final_arrival_airport_filter')
            df_final_use_min_departure_date_filter = col1.checkbox(label='Filtrer par Date Départ Minimale', key='df_final_use_min_departure_date_filter')
            df_final_min_departure_date_filter = col1.date_input(label='Date Départ Minimale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_final_min_departure_date_filter')
            df_final_use_max_departure_date_filter = col2.checkbox(label='Filtrer par Date Départ Maximale', key='df_final_use_max_departure_date_filter')
            df_final_max_departure_date_filter = col2.date_input(label='Date Départ Maximale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_final_max_departure_date_filter')

            df_final_copy = st.session_state['df_final'].copy()

            if df_final_id_filter:
                df_final_copy = df_final_copy[df_final_copy['flight_id'].isin(df_final_id_filter)]
            if df_final_code_filter:
                df_final_copy = df_final_copy[df_final_copy['flight_code'].isin(df_final_code_filter)]
            if df_final_departure_airport_filter:
                df_final_copy = df_final_copy[df_final_copy['departure_airport'].isin(df_final_departure_airport_filter)]
            if df_final_arrival_airport_filter:
                df_final_copy = df_final_copy[df_final_copy['arrival_airport'].isin(df_final_arrival_airport_filter)]
            if df_final_use_min_departure_date_filter:
                df_final_copy =df_final_copy[pd.to_datetime(df_final_copy['departure_date']).dt.date >= df_final_min_departure_date_filter]
            if df_final_use_max_departure_date_filter:
                df_final_copy = df_final_copy[pd.to_datetime(df_final_copy['departure_date']).dt.date <= df_final_max_departure_date_filter]

            st.dataframe(df_final_copy, hide_index=True)
        
        if st.session_state['cross_matrix'] is not None:
            st.subheader("Matrice croisé")
            st.dataframe(st.session_state['cross_matrix'].style.applymap(color_backlog).format("{:2f}"), width='stretch', height=600)

            # for col in st.session_state['cross_matrix'].columns:
            #     st.write(col)

    with tab3:

        col1, col2 = st.columns(2)

        period_start_date = col1.date_input(label='Date Début', value=None, min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30))
        period_end_date = col2.date_input(label='Date Fin', value=None, min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30))

        if st.button("Démarrer Simulation avec période", type='primary'):
        
            try:
                st.session_state['df_final_wp'] = run_algo_with_period(st.session_state['df_flights'].copy(), st.session_state['df_aircrafts'].copy(), period_start_date, period_end_date)
            
                st.session_state['cross_matrix_wp'] = calculate_cross_matrix_with_period(st.session_state['df_final_wp'])

            except Exception as e:
                st.warning("Aucun vol ne correspond aux critéres choisies.")
                st.info("Conseil : Vérifiez que les dates choisies couvrent bien les données des vols.")

        final_wp_column_config = {
           'flight_id': st.column_config.TextColumn(label='flight_id', disabled=True, required=True),
           'flight_code': st.column_config.TextColumn(label='flight_code', disabled=True, required=True), 
           'departure_airport': st.column_config.SelectboxColumn(label='departure_airport', options=sorted(get_departure_airport_list()), required=True),
           'arrival_airport': st.column_config.SelectboxColumn(label='arrival_airport', options=sorted(get_arrival_airport_list()), required=True), 
           'departure_date': st.column_config.TextColumn(label='departure_date', disabled=True, required=True), 
           'arrival_date': st.column_config.TextColumn(label='arrival_date', disabled=True, required=True), 
           'departure_time': st.column_config.TextColumn(label='departure_time', disabled=True, required=True), 
           'arrival_time': st.column_config.TextColumn(label='arrival_time', disabled=True, required=True), 
           'departure_datetime': st.column_config.DatetimeColumn(label='departure_datetime', disabled=True, required=True), 
           'arrival_datetime': st.column_config.DatetimeColumn(label='arrival_datetime', disabled=True, required=True), 
           'week': st.column_config.TextColumn(label='week', disabled=True, required=True), 
           'aircraft_code': st.column_config.SelectboxColumn(label='aircraft_code', options=get_aircraft_code_list(), required=True), 
           'economy_capacity': st.column_config.NumberColumn(label='economy_capacity', disabled=True, required=True), 
           'economy_pax_load': st.column_config.NumberColumn(label='economy_pax_load', min_value=0, max_value=100, required=True), 
           'economy_pax_count': st.column_config.NumberColumn(label='economy_pax_count', disabled=True, required=True), 
           'business_capacity': st.column_config.NumberColumn(label='business_capacity', disabled=True, required=True), 
           'business_pax_load': st.column_config.NumberColumn(label='business_pax_load', min_value=0, max_value=100, required=True), 
           'business_pax_count': st.column_config.NumberColumn(label='business_pax_count', disabled=True, required=True), 
           'total_pax_count': st.column_config.NumberColumn(label='total_pax_count', disabled=True, required=True, format='%d'), 
        #    'economy_avg_bag_count': st.column_config.NumberColumn(label='economy_avg_bag_count', disabled=True), 
        #    'business_avg_bag_count': st.column_config.NumberColumn(label='business_avg_bag_count', disabled=True), 
           'economy_avg_bag_weight': st.column_config.NumberColumn(label='economy_avg_bag_weight', min_value=0, required=True), 
           'business_avg_bag_weight': st.column_config.NumberColumn(label='business_avg_bag_weight', min_value=0, required=True), 
           'flight_status': st.column_config.SelectboxColumn(label='flight_status', options=['scheduled', 'cancelled'], default='scheduled', required=True), 
           'economy_total_bag_weight': st.column_config.NumberColumn(label='economy_total_bag_weight', disabled=True, format='%d'), 
           'business_ttal_bag_weight': st.column_config.NumberColumn(label='business_ttal_bag_weight', disabled=True, format='%d'), 
           'economy_total_bag_weight_backlog_prev_flight': st.column_config.NumberColumn(label='economy_total_bag_weight_backlog_prev_flight', disabled=True, format='%d'), 
           'business_total_bag_weight_backlog_prev_flight': st.column_config.NumberColumn(label='business_total_bag_weight_backlog_prev_flight', disabled=True, format='%d'), 
           'economy_total_bag_weight_backlog_prev_flight_added': st.column_config.NumberColumn(label='economy_total_bag_weight_backlog_prev_flight_added', disabled=True, format='%d'),
           'business_total_bag_weight_backlog_prev_flight_added': st.column_config.NumberColumn(label='business_total_bag_weight_backlog_prev_flight_added', disabled=True, format='%d'), 
           'economy_total_bag_weight_charged': st.column_config.NumberColumn(label='economy_total_bag_weight_charged', disabled=True, format='%d'), 
           'business_total_bag_weight_charged': st.column_config.NumberColumn(label='business_total_bag_weight_charged', disabled=True, format='%d'), 
           'economy_total_bag_weight_backlog': st.column_config.NumberColumn(label='economy_total_bag_weight_backlog', disabled=True, format='%d'), 
           'business_total_bag_weight_backlog': st.column_config.NumberColumn(label='business_total_bag_weight_backlog', disabled=True, format='%d'), 
           'pax_count_lower_bound': st.column_config.NumberColumn(label='pax_count_lower_bound', disabled=True, format='%d'), 
           'pax_count_upper_bound': st.column_config.NumberColumn(label='pax_count_upper_bound', disabled=True, format='%d'), 
           'max_total_bag_weight': st.column_config.NumberColumn(label='max_total_bag_weight', disabled=True, format='%d')
        }

        if st.session_state['df_final_wp'] is not None:

            st.subheader("Résultats Simulation avec période")

            col1, col2 = st.columns(2)

            df_final_wp_id_filter = col1.multiselect(label='Vol ID', options=st.session_state['df_flights']['flight_id'].unique(), accept_new_options=False, key='df_final_wp_id_filter')
            df_final_wp_code_filter = col2.multiselect(label='Code Vol', options=sorted(list(st.session_state['df_flights']['flight_code'].dropna().unique())), accept_new_options=False, key='df_final_wp_code_filter')
            df_final_wp_departure_airport_filter = col1.multiselect(label='Aéroport Départ', options=sorted(list(st.session_state['df_aircrafts']['departure_airport'].unique())), accept_new_options=False, key='df_final_wp_departure_airport_filter')
            df_final_wp_arrival_airport_filter = col2.multiselect(label='Aéroport Arrivé', options=sorted(list(st.session_state['df_aircrafts']['arrival_airport'].unique())), accept_new_options=False, key='df_final_wp_arrival_airport_filter')
            df_final_wp_use_min_departure_date_filter = col1.checkbox(label='Filtrer par Date Départ Minimale', key='df_final_wp_use_min_departure_date_filter')
            df_final_wp_min_departure_date_filter = col1.date_input(label='Date Départ Minimale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_final_wp_min_departure_date_filter')
            df_final_wp_use_max_departure_date_filter = col2.checkbox(label='Filtrer par Date Départ Maximale', key='df_final_wp_use_max_departure_date_filter')
            df_final_wp_max_departure_date_filter = col2.date_input(label='Date Départ Maximale', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='df_final_wp_max_departure_date_filter')

            st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp'].copy()

            if df_final_wp_id_filter:
                st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'][st.session_state['df_final_wp_to_edit']['flight_id'].isin(df_final_wp_id_filter)]
            if df_final_wp_code_filter:
                st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'][st.session_state['df_final_wp_to_edit']['flight_code'].isin(df_final_wp_code_filter)]
            if df_final_wp_departure_airport_filter:
                st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'][st.session_state['df_final_wp_to_edit']['departure_airport'].isin(df_final_wp_departure_airport_filter)]
            if df_final_wp_arrival_airport_filter:
                st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'][st.session_state['df_final_wp_to_edit']['arrival_airport'].isin(df_final_wp_arrival_airport_filter)]
            if df_final_wp_use_min_departure_date_filter:
                st.session_state['df_final_wp_to_edit'] =st.session_state['df_final_wp_to_edit'][pd.to_datetime(st.session_state['df_final_wp_to_edit']['departure_date']).dt.date >= df_final_wp_min_departure_date_filter]
            if df_final_wp_use_max_departure_date_filter:
                st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'][pd.to_datetime(st.session_state['df_final_wp_to_edit']['departure_date']).dt.date <= df_final_wp_max_departure_date_filter]

            st.session_state['df_final_wp_to_edit'] = st.session_state['df_final_wp_to_edit'].reset_index(drop=True)

            df_final_wp = st.data_editor(st.session_state['df_final_wp_to_edit'], column_config=final_wp_column_config, on_change=handle_df_final_wp_change, key='df_final_wp_editor', hide_index=True)

            st.subheader("Ajouter un nouveau vol")

            @st.fragment()
            def add_new_flight_wp():
            
                col1, col2 = st.columns(2)

                flight_code_wp = col1.text_input(label='Code Vol', placeholder='AT###', max_chars=5, key='flight_code_wp_input')
                aircraft_code_wp = col2.selectbox(label='Type Machine', options=list(st.session_state['df_aircrafts']['aircraft_code'].unique()), accept_new_options=False, key='aircraft_code_wp_input')
                departure_airport_wp = col1.selectbox(label='Aéroport Départ', options=sorted(list(st.session_state['df_aircrafts']['departure_airport'].unique())), accept_new_options=False, key='departure_airport_wp_input')
                arrival_airport_wp = col2.selectbox(label='Aéroport Arrivé', options=sorted(list(st.session_state['df_aircrafts']['arrival_airport'].unique())), accept_new_options=False, key='arrival_airport_wp_input')
                departure_date_wp = col1.date_input(label='Date Départ', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='departure_date_wp_input')
                arrival_date_wp = col2.date_input(label='Date Arrivé', min_value=datetime.date(2026, 1, 1), max_value=datetime.date(2026, 6, 30), key='arrival_date_wp_input')
                departure_time_wp = col1.time_input(label='Temps Départ', step=60, key='departure_time_wp_input')
                arrival_time_wp = col2.time_input(label='Temps Arrivé', step=60, key='arrival_time_wp_input')
                economy_capacity_wp = col1.number_input(label='Capacité économique', min_value=0, value=0, key='economy_capacity_wp_input')
                economy_pax_load_wp = col2.number_input(label='Charge pax économique', min_value=0, max_value=100, value=0, key='economy_pax_load_wp_input')
                business_capacity_wp = col1.number_input(label='Capacité business', min_value=0, key='business_capacity_wp_input')
                business_pax_load_wp = col2.number_input(label='Charge pax business', min_value=0, max_value=100, value=0, key='business_pax_load_wp_input')
                # economy_avg_bag_count_wp = col1.number_input(label='Moyenne du nombre de bagages par passager en classe économique', min_value=0, disabled=True, value=1, key='economy_avg_bag_count_wp_input')
                # business_avg_bag_count_wp = col2.number_input(label='Moyenne du nombre de bagages par passager en classe business', min_value=0, disabled=True, value=1, key='business_avg_bag_count_wp_input')
                economy_avg_bag_weight_wp = col1.number_input(label='Moyenne du poids de bagages par passager en classe économique', min_value=0, value=23, key='economy_avg_bag_weight_wp_input')
                business_avg_bag_weight_wp = col2.number_input(label='Moyenne du poids de bagages par passager en classe business', min_value=0, value=32, key='business_avg_bag_weight_wp')

                if st.button('Ajouter',key='add_new_flight_wp_btn'):

                    pattern = r"^AT\d{3}$"

                    if not re.match(string=flight_code_wp, pattern=pattern):
                        flight_code_wp = None
                    
                    new_row_wp = {
                        'flight_id': get_new_flight_id(st.session_state['df_flights']),
                        'flight_code': flight_code_wp,
                        'departure_airport': departure_airport_wp,
                        'arrival_airport': arrival_airport_wp,
                        'departure_date': str(arrival_date_wp),
                        'arrival_date': str(arrival_date_wp),
                        'departure_time': str(departure_time_wp),
                        'arrival_time': str(arrival_time_wp),
                        'aircraft_code': aircraft_code_wp,
                        'economy_capacity': economy_capacity_wp,
                        'economy_pax_load': economy_pax_load_wp,
                        'economy_pax_count': np.floor((economy_pax_load_wp / 100) * economy_capacity_wp),
                        'business_capacity': business_capacity_wp,
                        'business_pax_load': business_pax_load_wp,
                        'business_pax_count': np.floor((business_pax_load_wp / 100) * business_capacity_wp),
                        # 'economy_avg_bag_count': economy_avg_bag_count_wp,
                        # 'business_avg_bag_count': business_avg_bag_count_wp,
                        'economy_avg_bag_weight': economy_avg_bag_weight_wp,
                        'business_avg_bag_weight': business_avg_bag_weight_wp,
                        'flight_status': 'scheduled'
                    }

                    new_row_wp_default_values = {
                        'departure_datetime': str(departure_date_wp) + ' ' + str(departure_time_wp),
                        'arrival_datetime': str(arrival_date_wp) + ' ' + str(arrival_time_wp),
                        'total_pax_count': np.floor((economy_pax_load_wp / 100) * economy_capacity_wp) + np.floor((business_pax_load_wp / 100) * business_capacity_wp),
                        'economy_total_bag_weight': None, 
                        'business_ttal_bag_weight': None, 
                        'economy_total_bag_weight_backlog_prev_flight': None, 
                        'business_total_bag_weight_backlog_prev_flight': None, 
                        'economy_total_bag_weight_backlog_prev_flight_added': None,
                        'business_total_bag_weight_backlog_prev_flight_added': None, 
                        'economy_total_bag_weight_charged': None, 
                        'business_total_bag_weight_charged': None, 
                        'economy_total_bag_weight_backlog': None, 
                        'business_total_bag_weight_backlog': None, 
                        'pax_count_lower_bound': None, 
                        'pax_count_upper_bound': None, 
                        'max_total_bag_weight': None
                    }

                    if check_form_necessary_fields([flight_code_wp, departure_airport_wp, arrival_airport_wp, departure_date_wp, departure_time_wp, aircraft_code_wp]):

                        st.session_state['errors_list'].append("Champs nécessaires manquants: Code Vol, Aéroport Départ, Aéroport Arrivé, Date Départ, Temps Départ, Code d'Avion.")

                    elif not st.session_state['df_flights'][(st.session_state['df_flights']['flight_code'] == flight_code_wp) & 
                                                        (st.session_state['df_flights']['departure_airport'] == departure_airport_wp) & 
                                                        (st.session_state['df_flights']['flight_status'] == 'scheduled')].empty:
                        
                        st.session_state['errors_list'].append("Impossible d'avoir deux vols planifiés avec meme Code Vol et Date Départ")

                    elif st.session_state['df_aircrafts'][(st.session_state['df_aircrafts']['departure_airport'] == departure_airport_wp) & 
                                                        (st.session_state['df_aircrafts']['arrival_airport'] == arrival_airport_wp) & 
                                                        (st.session_state['df_aircrafts']['aircraft_code'] == aircraft_code_wp)].empty:
                    
                        st.session_state['warnings_list'].append(f"Flight ID: {new_row_wp['flight_id']}: Combinaison de Origine: {new_row_wp['departure_airport']} ,Destination: {new_row_wp['arrival_airport']} et Type Machine: {new_row_wp['aircraft_code']} n'est pas disponible dans la table aircrafts")

                    else:
                        # st.session_state['df_flights'].loc[len(st.session_state['df_flights'])] = new_row_wp
                        # st.session_state['df_final_wp'].loc[len(st.session_state['df_final_wp'])] = new_row_wp | new_row_wp_default_values

                        st.session_state['df_flights'] = pd.concat(
                            [st.session_state['df_flights'], pd.DataFrame([new_row_wp])], ignore_index=True
                        )
                        st.session_state['df_final_wp'] = pd.concat(
                            [st.session_state['df_final_wp'], pd.DataFrame([new_row_wp | new_row_wp_default_values])], ignore_index=True
                        )

                    st.rerun(scope='app')

            add_new_flight_wp()

        if st.session_state['cross_matrix_wp'] is not None:
            st.subheader("Matrice croisé avec période")
            st.dataframe(st.session_state['cross_matrix_wp'].style.applymap(color_backlog).format("{:2f}"), width='stretch', height=600)

    st.session_state['warnings_list'] = []
    st.session_state['errors_list'] = []
