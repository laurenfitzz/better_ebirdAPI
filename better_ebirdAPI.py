name == "better_ebirdAPI"
author== 'Lauren Fitzgerald'
descrpition == "This module was created for bird watchers! To use better_ebirrdAPI the user requires an ebirdAPI 2.0 key"
install_requires=[
        "pandas",
    "IPython", 
    "geopandas",
    "requests",
    "bs4",
    "json",
    "folium",
    "requests",
    "google_images_search"]


# Common Name to Scientific Name
# this function can be used to retreive the scientific name of a bird using the common name as input
#for this function to work the user must download the "PFW-Species-translation-table.csv" and read it as species_data 
def com_to_sci(common_name):
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # make it not case sensitve 
    common_name = common_name.lower()
    scientific_name = species_data.loc[species_data['american_english_name'].str.lower() == common_name, 'scientific_name'].values
    # this was added because for some reason sometimes the mapping functions wouldnt work without it. dont ask, this was discovered because (i think) sometimes the name of some observations didn't match names in this csv and therefor errors would occur and the later maping functions wouldnt work. 
    if len(scientific_name) == 0:
        return None
    else:
        #no clue why this one requires '[0]' and its sister function com_to_sci doesnt. also dont ask, also no clue why this is needed in the .py file but not in the .ipynb tutorial. Makes no sense to me 
        return scientific_name[0]

#2 Scientific Name to Common Name 
#this function can be used to retrive the common bird name from the scientific name 
#Like com_to sci the user must download the "PFW-Species-translation-table.csv" and read it as species_data 
def sci_to_com(scientific_name):
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    scientific_name = scientific_name.lower()
    common_name = species_data.loc[species_data['scientific_name'].str.lower() == scientific_name, 'american_english_name'].values[0]
    if len(common_name) == 0:
        return None
    else:
        return common_name


#3 List types of birds using a Key Word 
#this function works to match names and get a list of possible sub species such as a list of all names containing duck or wren, 
#this function isnt perfect as it can miss related speices that do not contain matching names, however its a good indicator
def list_types(keyword):
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    matching_names = species_data[species_data['american_english_name'].str.contains(keyword, case=False)]['american_english_name'].tolist()
    return matching_names

#4 Common Name Discription
# this can be used to get the description of a bird using its common name, this was made with sci_des to create 
# the function bird_description which can be used to get any descrption of any bird in the world 
#this only works with North American birds 
def com_des(common_name):
    import bs4
    from bs4 import BeautifulSoup
    import requests
    # we must replace all spaces with a '-' for the function to work
    common_name = common_name.replace(" ", "-")
    # we know the common name goes at the end based off of exploring the website
    url = f"https://www.audubon.org/field-guide/bird/{common_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # by inspecting the website we know where the desription of the bird is located
    bird_div = soup.find("div", class_="bird_discussion")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        return "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelling"

#5 Scientific Name description 
# this was created to be combined with com_des to create bird_description 
# this only works using the proper scientific name and is case sensitive 
def sci_des(scientific_name):
    import bs4
    from bs4 import BeautifulSoup
    import requests
    # we must replace all spaces with a '_' for the function to work
    scientific_name = scientific_name.replace(" ", "_")
     # we know the scientific name is inputted at the end and followed by a ".html" by exploring the website 
    url = f"https://picturebirdai.com/wiki/{scientific_name}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # by inspecting the website we know where the desription of the bird is located
    bird_div = soup.find("div", {"id": "description-content"})
    if bird_div is not None:
        field_value_div = bird_div.find("div", {"class": "field_value_description"})
        if field_value_div is not None:
            div = field_value_div.find("div")
            if div is not None:
                return div.text.strip()
            return "Bird not found. Make sure you are inputting the proper scientific name. Use function com_to_sci to get the proper name"


#6 Bird description 
# This is the best function for getting a description of any species. It combines com_des and sci_des into one!
# it takes the common name as input
def bird_description(common_name):
    import bs4
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # the .split function ensures that any parantheses are removed as this function couldnt return the description of birds which includes "(common)" at the end of its name 
    #  i discovered this problem as it couldnt return the description in the maps for a bird called "Northern Cardinal (common)" but could for "Northern Cardinal"
    # since it also converts the name to scientific name if nothing is returned then it will always return an accurate description. 
    common_name = common_name.split(' (')[0] 
    common_name1 = common_name.replace(" ", "-")
    common_name = common_name.split(' (')[0]
    url = f"https://www.audubon.org/field-guide/bird/{common_name1}"
    response = requests.get(url)
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
                    else:
                        return "Bird not found"

#7 Retrieve species data 
# this retieves all the information of a bird using ebirdAPI 2.0 
def retrieve_species_data(scientific_name, ebird_api_key):
    import requests
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

#8 this is used to retieve a bird image for those who do not have access to a google API key and therefore cannot use the function "google_API_pic"
def wiki_pic(common_name):
    import requests
    import IPython 
    from IPython.display import Image
    import bs4
    from bs4 import BeautifulSoup
    # Make a GET request to the Wikipedia page
    #it searches the scientfic name because wikipedia automattically connects the scientfic name and the common name to the same page
    # doing this ensures that the function will only return pictures of birds not other things of the same name
    sci_name = com_to_sci(common_name).replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{sci_name}"
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
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
    display(Image(url=picture_url))


#9 Google API PIC 
#This function retreives pictures using Google Image Search. It works great for those who have access to a premium google api key
#for those who do not have access to a google api key there is another function, "wiki_pic" which scrapes wikipedia for bird images. 
def google_API_pic(bird_name, google_apikey, google_CX):
    from google_images_search import GoogleImagesSearch
    import IPython 
    from IPython.display import Image
    import requests
    # Initialize GoogleImagesSearch object
    gis = GoogleImagesSearch(google_apikey, google_CX)
    # Set search parameters
    _search_params = {
        # + bird is added to ensure that only bird images get retieved or else you would retieve TV images if merlin is search or sports team logos etc
        "q": bird_name + " bird",
        "imgSize": "large",
        "num": 1
    }
    # Search for images
    gis.search(search_params=_search_params)
    # Get image URL
    image_url = gis.results()[0].url
    pic = requests.get(image_url)
    # Display image in notebook
    return Image(pic.content)


#10 
#this is used to retieve a bird image for those who do not have access to a google API key and therefore cannot use the function "google_API_pic4map"
def wiki_pic_map(common_name):
    import requests
    import base64
    import bs4
    from bs4 import BeautifulSoup
    # Make a GET request to the Wikipedia page
    sci_name = com_to_sci(common_name)
    url = f"https://en.wikipedia.org/wiki/{sci_name}"
    common_name = common_name.replace(" ", "_")
    response = requests.get(url)
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

#11
def google_API_pic4map(bird_name, google_apikey, google_CX):
    import base64
    import requests
    # Initialize GoogleImagesSearch object
    gis = GoogleImagesSearch(google_apikey, google_CX)

    # Set search parameters
    _search_params = {
        "q": bird_name + " bird",
        "imgSize": "large",
        "num": 1
    }

    # Search for images
    gis.search(search_params=_search_params)
    image_data = requests.get(gis.results()[0].url).content
    # Encode image data as base64
    image_base64 = base64.b64encode(image_data).decode()
    
    return image_base64

# Find Nearby birds! 
# this function will create a map of nearby observations based off the ebirdAPI. It allows the user to see the birds in a specified radius. The radius can be any distance however that effects the loading of the map. It is reccomended the users radius is under 10km. 
def nearby_observations(lat, lng, distance_km, ebird_api_key):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
    #dis = 15km 
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
        bird_image_data = wiki_pic_map(bird_name)
        
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

#Find nearby birds! GAPI version
# this function is equivalent to nearby_observations
def nearby_observations_GAPI(lat, lng, distance_km, ebird_api_key, google_apikey, google_CX):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
    #dis = 15km 
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
        bird_image_data = wiki_pic_map(bird_name)
        
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



# Find the location of a specifed bird!
# this function will create a map of nearby observations of a specifed bird based off the ebirdAPI. It allows the user to see where a species is sighted within a 10km radius
def nearby_bird(lat, lng, sci_name, ebird_api_key):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
    #dis = 10km
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist=10&sci={sci_name}&fmt=json'

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
        # this function defaults to using wiki_pic_map however it can be replace with google_API_pic4map. 
        #google_API_pic4map is better if the user doesnt have a limit in querys as it is more reliable 
        # to use the function replace the next line of code with " bird_image_data = google_API_pic4map(bird_name)
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

# Find the location of a specifed bird GAPI Version
# this is equivalent to the nearby_bird function
def nearby_bird_GAPI(lat, lng, sci_name, ebird_api_key, google_apikey, google_CX):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
    #dis = 10km
    url = f'https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist=10&sci={sci_name}&fmt=json'
    headers = {'X-eBirdApiToken': ebird_api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    bird_map = folium.Map(location=[lat, lng], zoom_start=10)
    
    for obs in data:
        bird_name = obs['comName']
        sci_name = obs['sciName']
        obs_date = obs['obsDt']
        location = [obs['lat'], obs['lng']]
        bird_description_text = bird_description(bird_name)
        bird_image_data = google_API_pic4map(bird_name, google_apikey, google_CX)
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

# Find rare or notable birds! 
# this function will create a map of rare or notable observations based off the ebirdAPI. It allows the user to see intresting birds within a specifed radius. The radius can be any distance however that effects the loading of the map. It is reccomended the users radius is under 10km.
def notable_bird(lat, lng, distance_km, ebird_api_key):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
  
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
        #if bird_description_text == "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelling":
          #  bird_description_text = sci_des(sci_name)
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


# Find Notable birds GAPI version
def notable_bird_GAPI(lat, lng, distance_km, ebird_api_key, google_apikey, google_CX):
    import requests
    import json
    import folium
    import pandas as pd
    species_data = pd.read_csv("PFW-species-translation-table.csv")
    # Define the API endpoint URL
  
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
        #if bird_description_text == "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelling":
          #  bird_description_text = sci_des(sci_name)
         #google_API_pic4map is better if the user doesnt have a limit in querys as it is more reliable 
        bird_image_data = google_API_pic4map(bird_name, google_apikey, google_CX)
        
        
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

# Get birding hotspots! 
# this function can help new birders find places where people regulary observe and record data using ebird. 
# hotspots dont mean there are more birds, it refers to where people frequently birdwatch.
def get_hotspot(lat, lng, ebird_api_key):
    import requests
    import json
    import folium
    url = f'https://api.ebird.org/v2/ref/hotspot/geo?lat={lat}&lng={lng}&dist=5&fmt=json'
    headers = {'X-eBirdApiToken': ebird_api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    bird_map = folium.Map(location=[lat, lng], zoom_start=13)

    for obs in data:
        loc_id = obs['locId']
        #then use the api to go find the hotspot information so it can be put into the markers 
        hotspot_url = f"https://api.ebird.org/v2/ref/hotspot/info/{loc_id}"
        hotspot_response = requests.get(hotspot_url, headers=headers)
        hotspot_data = hotspot_response.json()
        if hotspot_response.status_code == 200:
            # Create popup text with hotspot info
            popup_text = f"<b> Name: </b><br>{hotspot_data['name']}</br>" \
                         f"<b>Region:</b><br>{hotspot_data['subnational2Name']}</br>" \
                         f"<b>Province/State:</b><br>{hotspot_data['subnational1Name']}</br>" \
                         f"<b>Country:</b><br>{hotspot_data['countryCode']}</br>" \
                         f"<b>Latitude & Longitude:</b><br>{hotspot_data['latitude']}, {hotspot_data['longitude']}</br>"\
            
        else:
            popup_text = "Error getting hotspot info"
            location = obs['lat'], obs['lng']
            marker = folium.Marker(location=location, popup=popup_text)
            marker.add_to(bird_map)

    return bird_map






















