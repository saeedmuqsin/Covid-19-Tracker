"""
    => This API fetchs data of the covid-19 pandemic all across the globe 
    and also provide the cases recorded in every country
"""

from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests

tracker_api = Flask(__name__)

@tracker_api.route("/", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        CountryName = request.form['country_name']
        return redirect(url_for('country_view', country = CountryName))

    # request received from the frontend
    try: # checking error after request made
        website_url = "https://www.worldometers.info/coronavirus/"
        website_content = requests.get(website_url)

    except Exception:
        pass
    
    else:
        website_scrap = BeautifulSoup(website_content.content, "html.parser")

        # list to store the pandemic statistic around the globe 
        stats = [ ]
        for span in website_scrap.find_all('div', 'maincounter-number'):
            for numbers in span.find('span'):
                # storing the figure into the global variable
                stats.append(numbers)

        #dict stores the collected figures based the totalcases, deathcases, people who recovered
        GlobalStats = {
            'covidcases': stats[0],
            'deathcases': stats[1],
            'recovered': stats[2] 
            }
        return render_template('home.html', context=GlobalStats)

# this url redirects the user to where cases recorded by a country based on the request from the user
@tracker_api.route('/country/<country>')
def country_view(country):
    if country=="Us" or country=="us" or country=="USA" or country == "United States" or country == "UNITED STATES" or country=="united states":
        url = "https://www.worldometers.info/coronavirus/country/us/"
        country = "United states"

    elif country =="UK" or country =="Uk" or country == "United Kingdom" or  country =="UNITED KINGDOM" or country=="united kingdom" or country =="uk":
        url = "https://www.worldometers.info/coronavirus/country/uk/"
        country = "United Kingdom"

    else:
        url = "https://www.worldometers.info/coronavirus/country/{0}".format(country)
    
    try:
        UserRequest = requests.get(url)
    
    except Exception:
        return "404"
    
    else:
        PageScrap = BeautifulSoup(UserRequest.content, 'html.parser')
        # store the figure into a dict
        CountryRecord = { }
        CountryRecord['country_name'] = country

        #scraping the country's Flag from the external source
        flag = PageScrap.find('div', 'content-inner')
        CountryRecord['Country_Flag'] = flag.img['src']

        #scrap for cases recorded for a particular country
        figures = [ ]
        for tag in PageScrap.find_all('div', 'maincounter-number'):
            for num in tag.span:
                figures.append(num)
        

        CountryRecord['total_cases'] = figures[0]
        CountryRecord['death_cases'] = figures[1]
        CountryRecord['recovered'] = figures[2]
        
        return render_template("country.html", context=CountryRecord)
    
if __name__ == "__main__":
    tracker_api.run(debug=True)