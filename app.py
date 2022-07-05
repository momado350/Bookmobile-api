from flask import Flask, request, jsonify, render_template
import pandas as pd # to load cities dataset
import numpy as np
from geopy import distance # to calculate distance on the surface

import requests
import urllib.parse
branch = pd.read_csv("data/LATLON.CSV")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_loc',methods=['GET', 'POST'])    
def get_loc():
    #address = '201 East 75th St. Kansas City, MO 64114'
    address = request.form.get("Patron Address")
    
    
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    #print(response[0]["lat"])
    #print(response[0]["lon"])
    lst = []
    for index, row in branch.iterrows():
        d = distance.distance((row['lat'], row['long']), (response[0]["lat"], response[0]["lon"]))
        lst.append(d.miles)
    lst1 = sorted(lst,key=float)
    if lst1[0] < 1:
            #print("You are less than One mile away from " + row['branch'] +' '+ "Branch")
        #return render_template('index.html', prediction_text='This Address is located less than One Mile away from  {}'.format(row['branch']) + ' ' + 'Branch. Bookmobile Services are not avialable for this Address!')
        return render_template('index.html', prediction_text='Sorry,This Address is located less than One Mile away from One of our Library Branches. Bookmobile Services are not avialable for this Address!')
    else:
        return render_template('index.html', prediction_text='Bookmobile Services are Avialable for this Area!')
            
# get_loc("201 East 75th St. Kansas City, MO 64114")
#get_loc(input())
if __name__ == "__main__":
    app.run(debug=True, port=5000)




