#1 common to scientific 
# this function can be used to retreive the scientific name of a bird using the common name as input
# for this function to work the user must download the "PFW-Species-translation-table.csv" and read it as species_data 
#use the following:
#species_data = pd.read_csv("PFW-species-translation-table.csv")
def com_to_sci(common_name):
    # make it not case sensitve 
    common_name = common_name.lower()
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    scientific_name = species_data.loc[species_data['american_english_name'].str.lower() == common_name, 'scientific_name'].values[0]
    return scientific_name

#2 scientific to common 
#this function can be used to retrive the common bird name from the scientific name 
#Like com_to sci the user must download the "PFW-Species-translation-table.csv" and read it as species_data 
def sci_to_com(scientific_name):
    scientific_name = scientific_name.lower()
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    common_name = species_data.loc[species_data['scientific_name'].str.lower() == scientific_name, 'american_english_name'].values[0]
    return(common_name)

#3 List_types
#this function works to match names and get a list of possible sub species such as a list of all names containing duck or wren, 
#this function isnt perfect as it can miss related speices that do not contain matching names, however its a good indicator
def list_types(sub_species):
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    matching_names = species_data[species_data['american_english_name'].str.contains(sub_species, case=False)]['american_english_name'].tolist()
    return matching_names

#4 common name discription
# this can be used to get the description of a bird using its common name, this was made with sci_des to create 
# the function bird_description which can be used to get any descrption of any bird in the world 
#this only works with North American birds 
def com_des(common_name):
    common_name = common_name.replace(" ", "-")
    url = f"https://www.audubon.org/field-guide/bird/{common_name}"
    import requests
    response = requests.get(url)
    import bs4
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", class_="bird_discussion")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        return "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelling"

#5 Scientific name description 
# this was created to be combined with com_des to create bird_description 
#this only works using the proper scientific name and is case sensitive  
def sci_des(scientific_name):
    scientific_name = scientific_name.replace(" ", "_")
    url = f"https://picturebirdai.com/wiki/{scientific_name}.html"
    import requests
    response = requests.get(url)
    import bs4
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", {"id": "description-content"})
    if bird_div is not None:
        field_value_div = bird_div.find("div", {"class": "field_value_description"})
        if field_value_div is not None:
            div = field_value_div.find("div")
            if div is not None:
                return div.text.strip()
            return "Bird not found. Make sure you are inputting the proper scientific name. Use function com_to_sci to get the proper name"

#6 Bird description 
# this is the best function for retriveing a description about a bird. It is made by combining the previous 2 functions to scrape for information from 2 sites 
def bird_description(common_name):
    common_name1 = common_name.replace(" ", "-")
    url = f"https://www.audubon.org/field-guide/bird/{common_name1}"
    import requests
    response = requests.get(url)
    import bs4
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", class_="bird_discussion")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        scientific_name = com_to_sci(common_name)
        if scientific_name is not None:
            scientific_name1 = scientific_name.replace(" ", "_")
            url = f"https://picturebirdai.com/wiki/{scientific_name1}.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            bird_div = soup.find("div", {"id": "description-content"})
            if bird_div is not None:
                field_value_div = bird_div.find("div", {"class": "field_value_description"})
                if field_value_div is not None:
                    div = field_value_div.find("div")
                    if div is not None:
                        return div.text.strip()
            return "Bird not found. Make sure you are inputting the proper scientific name. Use function com_to_sci to get the proper name"
        else:
            return "Bird not found"
           
#7 Google API PIC 
#This function retreives pictures using Google Image Search. It works great for those who have access to a premium google api key
#for those who do not have access to a google api key there is another function, "wiki_pic" which scrapes wikipedia for bird images. 
def google_API_pic(common_name, google_apikey, google_CX):
    import requests
    # Initialize GoogleImagesSearch object
    gis = GoogleImagesSearch(google_apikey, google_CX)
    # Set search parameters
    _search_params = {
        "q": common_name + " bird",
        "imgSize": "large",
        "num": 1
    }
    # Search for images
    gis.search(search_params=_search_params)
    # Get image URL
    image_url = gis.results()[0].url
    pic = requests.get(image_url)
    # Display image in notebook
    import IPython 
    from IPython.display import Image
    return Image(pic.content)

#8
#This function retreives pictures using Google Image Search and uses base64 to encode the image for the later mapping functions
#It works great for those who have access to a premium google api key, however wiki_pic_4map works interchangebly for those who do not have an google API key
#this function is more reliable at loading the images, and it is reccomended to use this 
def google_API_pic4map(common_name, google_apikey, google_CX):
    import requests
    # Initialize GoogleImagesSearch object
    gis = GoogleImagesSearch(google_apikey, google_CX)

    # Set search parameters
    _search_params = {
        "q": common_name + " bird",
        "imgSize": "large",
        "num": 1
    }

    # Search for images
    gis.search(search_params=_search_params)
    image_data = requests.get(gis.results()[0].url).content
    # Encode image data as base64
    import base64
    image_base64 = base64.b64encode(image_data).decode()
    
    return image_base64

#9 Wiki picture
#this is used to retieve a bird image for those who do not have access to a google API key and therefore cannot use the function "google_API_pic"
def wiki_pic(common_name):
    import requests
    # Make a GET request to the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{common_name}"
    common_name = common_name.replace(" ", "_")
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    import bs4
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the infobox table with either class name
    infobox = soup.find("table", class_=["infobox biota", "taxobox"])
    # if there is an infobox find image
    if infobox:
        # Find the image link within the infobox table
        image = infobox.find("img")
        # Get the source URL of the image
        image_url = image["src"]
        # Make a GET request to the image URL
        response = requests.get("https:" + image_url)
        picture_url = ("https:" + image_url)
    # if no infobox they are usually in a div called thmbinner
    else:
        picbox = soup.find("div", class_=["thumbinner"])
        if picbox:
            # Find the first image in the thumbinner div
            image2 = picbox.find("img")
            # Get the source URL of the image
            image_url = image2["src"]
            # Make a GET request to the image URL
            response = requests.get("https:" + image_url)
            picture_url = ("https:" + image_url)
        else:
            return "image not found"  
    #return(picture_url)
    import IPython 
    from IPython.display import Image
    display(Image(url=picture_url))

#10 
#this is used to retieve a bird image for those who do not have access to a google API key and therefore cannot use the function "google_API_pic4map"
def wiki_pic_map(common_name):
    import requests
    import base64
    # Make a GET request to the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{common_name}"
    common_name = common_name.replace(" ", "_")
    response = requests.get(url)
    import bs4
    from bs4 import BeautifulSoup
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the infobox table with either class name
    infobox = soup.find("table", class_=["infobox biota", "taxobox"])
    # Find the first image in the infobox table, if it exists
    if infobox:
        # Find the image link within the infobox table
        image = infobox.find("img")
        # Get the URL of the image
        image_url = image["src"]
        response = requests.get("https:" + image_url)
        # Encode the image content as base64
        image_data = base64.b64encode(response.content).decode()
        # Returnimage data
        return image_data
    # If there is no image in the infobox table, look for the first image in the thumbinner div
    else:
        picbox = soup.find("div", class_=["thumbinner"])
        if picbox:
            # Find the first image in the thumbinner div
            image2 = picbox.find("img")
            # Get the URL of the image
            image_url = image2["src"]
            response = requests.get("https:" + image_url)
            # Encode the image content as base64
            image_data = base64.b64encode(response.content).decode()
            # Return image data
            return image_data
        # If no image is found, return None
        else:
            return None 

        
#11 retieves species data 
#this uses the ebirdAPI 2.0 to summarize and retieve the information about the bird using the scientfic name 
def retrieve_species_data(scientific_name, ebird_api_key):
    import requests
    import json
    url = "https://api.ebird.org/v2/ref/taxonomy/ebird"
    params = {
        "fmt": "json",
        "locale": "en",
        "species": scientific_name
    }
    headers = {
        "X-eBirdApiToken": ebird_api_key
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return data[0]
    else:
        return None


#12 this maps nearby observations and uses the functions bird_description, and 
def nearby_observations(lat, lng, distance_km, ebird_api_key):
    import requests
    import folium
    # Define the API endpoint URL
    #dis = 15km 
    import json
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist={distance_km}&cat=species&fmt=json'

    #API inp
    headers = {'X-eBirdApiToken': ebird_api_key}
    response = requests.get(url, headers=headers)

    data = response.json()
    
    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    # Loop through the data and add markers for each bird sighting
    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        popup_text = f"<b>{bird_name}</b><br>{sci_name}</br><br>Date:{obs_date}</br>"
            
 # Get bird description
        bird_description_text = bird_description(bird_name)
        import base64
        bird_image_data = wiki_pic_map(bird_name)
        
        #HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}" style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map

#13 Same this as nearby_observations, but uses google images API
def nearby_observations_GAPI(lat, lng, distance_km, ebird_api_key):
    import json
    
    # Define the API endpoint URL
    #dis = 15km 
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist={distance_km}&cat=species&fmt=json'

    #API inp
    headers = {'X-eBirdApiToken': ebird_api_key}
    import requests
    response = requests.get(url, headers=headers)

    data = response.json()
    
    import folium
    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    # Loop through the data and add markers for each bird sighting
    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        popup_text = f"<b>{bird_name}</b><br>{sci_name}</br><br>Date:{obs_date}</br>"
            
 # Get bird description
        bird_description_text = bird_description(bird_name)
        bird_image_data = google_API_pic4map(bird_name)
        
        #HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}" style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map

#14
#this searches for a specific bird using its common name in a specified radius 
def nearby_bird(lat, lng, distance_km, bird_name, ebird_api_key):
    import requests
    import json
    import folium
    # Define the API endpoint URL
    #dis = 15km
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist={distance_km}&sci={bird_name}&fmt=json'

    headers = {'X-eBirdApiToken': ebird_api_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        
        # Get bird description
        bird_description_text = bird_description(bird_name)
         # Get bird image, needs the encoded function
        bird_image_data = wiki_pic_map(bird_name)
        
        # HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}" style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map

#15 nearby_bird_GAPI
# does the same thing as nearby_bird but with the google api key 
def nearby_bird_GAPI(lat, lng, distance_km, bird_name, ebird_api_key):
    import requests
    import json
    import folium
    # Define the API endpoint URL
    #dis = 15km
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist={distance_km}&sci={bird_name}&fmt=json'

    headers = {'X-eBirdApiToken': ebird_api_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        
        # Get bird description
        bird_description_text = bird_description(bird_name)
         # Get bird image, needs the encoded function
        bird_image_data = google_API_pic4map(bird_name)
        
        # Create custom HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}" style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map

#16 notable bird 
# this finds the notable observation of rare or unique birds within a specified radius of inputed coordinates 
def notable_bird(lat, lng, distance_km, ebird_api_key):
    import json
    import requests
    import folium
    # Define the API endpoint URL
    #dis = 25km
    url =f'https://api.ebird.org/v2/data/obs/geo/recent/notable?lat={lat}&lng={lng}&dist={distance_km}&fmt=json'

    # Add API key to the request headers
    headers = {'X-eBirdApiToken': ebird_api_key}

    # Send GET request to API endpoint
    response = requests.get(url, headers=headers)

    # Convert response to JSON format
    data = response.json()

    # Create a map centered at the inputted lat/lng
    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        
        # Get bird description
        bird_description_text = bird_description(bird_name)
        # Get bird image, needs the encoded function
        bird_image_data = wiki_pic_map(bird_name)
        
        # Create custom HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}"style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map

#17 notable_bird_GAPI
# does the same thing as notable_bird but uses the google api 
def notable_bird_GAPI(lat, lng, distance_km, ebird_api_key):
    import json
    import requests
    import folium
    # Define the API endpoint URL
    #dis = 25km
    url =f'https://api.ebird.org/v2/data/obs/geo/recent/notable?lat={lat}&lng={lng}&dist={distance_km}&fmt=json'
    # Add API key to the request headers
    headers = {'X-eBirdApiToken': ebird_api_key}
    # Send GET request to API endpoint
    response = requests.get(url, headers=headers)
    # Convert response to JSON format
    data = response.json()
    # Create a map centered at the inputted lat/lng
    bird_map = folium.Map(location=[lat, lng], zoom_start=10)

    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        
        # Get bird description
        bird_description_text = bird_description(bird_name)
     # Get bird image, needs the encoded function
        bird_image_data = google_API_pic4map(bird_name)
        
        # Create custom HTML popup
        popup_html = f"""
        <h4>{bird_name}</h4>
        <img src="data:image/jpeg;base64,{bird_image_data}"style="max-width:100%;max-height:100%">
        <h5><p><b>Scientific name:</b> {sci_name}</p></h5>
        <p><b>Date:</b> {obs_date}</p>
        <p><b>Description:</b> {bird_description_text}</p>
        """
        
        marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=400))
        marker.add_to(bird_map)

    return bird_map


# 18 gethotspot
# this function identifys spots within 5km of the inputed coordinates where people regulary visit for birding 

# "Hotspots represent a set of public locations that people regularly visit for birding, 
# regardless of how amazing they are for birds. The primary requirement of a Hotspot is that it is publicly accessible
def gethotspot(lat, lng):
    import requests
    import json
    import folium
    url = f'https://api.ebird.org/v2/ref/hotspot/geo?lat={lat}&lng={lng}&dist=5&fmt=json'

    payload={}
    headers = {'X-eBirdApiToken': ebird_api_key}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    bird_map = folium.Map(location=[lat, lng], zoom_start=13)
    
    
    # Loop through the data and add markers for each bird sighting
    for obs in data:
        location = obs['lat'], obs['lng']
        hotspot_id = obs['locId']
        popup_text = f"<b>Id:</b><br>{hotspot_id}</br><b>coordinates:</b><br>{location}</br>" 
        marker = folium.Marker(location=location, popup=popup_text)
        marker.add_to(bird_map)

    return bird_map