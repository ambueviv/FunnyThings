#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:33:51 2023

@author: annina
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd 
import csv
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]

# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

data = load_key(api_key, bin_id, username)
#st.write(data)


# Streamlit App
st.title('PCR Mastermix')
st.markdown('Dieses Programm führt Sie Schritt für Schritt durch den praktischen Ablauf einer PCR. Haben Sie einen Schritt ausgeführt, bestätigen Sie den Task mit einem Haken. Danach wird der nächste Schritt freigeschaltet.')

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.photocase.de/fotos/760967-pipette-glaskolben-und-mensuren-vor-blauem-hintergrund-photocase-stock-foto")
    }
   .sidebar .sidebar-content {
        background: url("https://www.photocase.de/fotos/760967-pipette-glaskolben-und-mensuren-vor-blauem-hintergrund-photocase-stock-foto")
    }
    </style>
    """,
    unsafe_allow_html=True
)



my_date = datetime.now()

proben_liste=[]

# Funktion zur Berechnung der Ergebnisse
def calculate(x):
    # Schleife zum Sammeln von Informationen über die Proben
    proben = {"Anzahl Proben": x, "Datum": my_date.strftime("%Y-%m-%d %H:%M:%S")}
    proben_liste.append(proben)
       
       # Berechnungen mit x durchführen
    result1 = x * 5
    result2 = x * 1
    result3 = x * 2
    result4 = x * 2
    result5 = x * 1
    result6 = x * 4
    result7 = x * 1 
    result8 = (max(int(x) * 50 - (result1 + result2 + result3 + result4 + result5 + result6 + result7), 0))

    # Speichern der Liste in einer JSON-Datei
    with open("proben.json", "a") as f:
        f.write("\n")
        json.dump(proben_liste, f)
    
    return result1, result2, result3, result4, result5, result6, result7, result8


# Anzahl der Proben eingeben
x = st.number_input("Gib deine Anzahl Proben ein (max. 96):", value=5, step=1)

# Anleitung für das Beschriften der Testtubes anzeigen
st.markdown("Für deine PCR brauchst du für jede Probe ein eigenes Test-Tube. Stelle für jede deiner Proben ein Test-Tube bereit und beschrifte sie entsprechend.")

# Checkboxen für die einzelnen Schritte anzeigen
results = calculate(x)

# Schritt 1: PCR Puffer pipettieren
checkbox1 = st.checkbox("Schritt 1: PCR Puffer pipettieren")
st.write("Für deine Anzahl Proben werden insgesamt", results[0], "Mikroliter PCR Puffer benötigt. Davon pipettierst du je 5 Mikroliter in jedes Testtube.")
if checkbox1:
        # Schritt 2: dNTP pipettieren
        checkbox2 = st.checkbox("Schritt 2: dNTP pipettieren")
        st.write("Für deine Anzahl Proben werden insgesamt", results[1], "Mikroliter dNTP benötigt. Davon pipettierst du je 1 Mikroliter in jedes Testtube.")
        if checkbox2:
            # Schritt 3: Vorwärtsprimer pipettieren
            checkbox3 = st.checkbox("Schritt 3: Vorwärtsprimer pipettieren")
            st.write("Für deine Anzahl Proben werden insgesamt", results[2], "Mikroliter Vorwärtsprimer benötigt. Davon pipettierst du je 1 Mikroliter in jedes Testtube.")
    
            if checkbox3:
                # Schritt 4: Rückwärtsprimer pipettieren
                checkbox4 = st.checkbox("Schritt 4: Rückwärtsprimer pipettieren")
                st.write("Für deine Anzahl Proben werden insgesamt", results[3], "Mikroliter Rückwärtsprimer benötigt. Davon pipettierst du je 1 Mikroliter in jedes Testtube.")
    
                if checkbox4:
                    # Schritt 5: Taq-DNA-Polymerase pipettieren
                    checkbox5 = st.checkbox("Schritt 5: Taq-DNA-Polymerase pipettieren")
                    st.write("Für deine Anzahl Proben werden insgesamt", results[4], "Mikroliter Taq-DNA-Polymerase benötigt. Davon pipettierst du je ")
                    
                    if checkbox5:
                        # Schritt 6: Template DNA pipettieren
                        checkbox6 = st.checkbox("Schritt 6: Template DNA pipettieren")
                        st.write("Für deine Anzahl Proben werden insgesamt", results[5], "Mikroliter Template DNA benötigt. Davon pipettierst du je 1 Mikroliter in jedes Testtube.")
                        if checkbox6:
                            # Schritt 7: MgCl2 pipettieren
                            checkbox7 = st.checkbox("Schritt 7: MgCl2 pipettieren")
                            st.write("Für deine Anzahl Proben werden insgesamt", results[6], "Mikroliter MgCl2 benötigt.Davon pippetierst du eine variable Menge in jedes Testtube, sodass das Endvolumen 50 Mikroliter beträgt.")
    
                            if checkbox7:
                                # Schritt 7: Wasser hinzufügen
                                checkbox8 = st.checkbox("Schritt 8: Wasser hinzufügen")
                                st.write("Für deine Anzahl Proben werden insgesamt", results[7], "Mikroliter Wasser benötigt. Davon pipettierst du je 1 Mikroliter in jedes Testtube.")
                                if checkbox8:
                                    st.write("Ihr Versuch ist nun beendet")
                                    new_results = [(x, my_date.strftime("%Y-%m-%d %H:%M:%S"))]

                                    # DataFrame erstellen oder vorhandenen laden
                                    try:
                                        df = pd.read_csv("results.csv")
                                    except FileNotFoundError:
                                        df = pd.DataFrame(columns=["Anzahl Proben", "Datum"])

                                    # Neue Ergebnisse zum DataFrame hinzufügen
                                    df = pd.concat([df, pd.DataFrame(new_results, columns=["Anzahl Proben", "Datum"])])

                                    # Ergebnisse als Tabelle in Streamlit darstellen
                                    st.table(df)

                                    # Ergebnisse in CSV-Datei speichern
                                    df.to_csv("results.csv", index=False)


      
 
     



        


        
      
        
      
        
      
        
      
        
      
        
      
    
