#Functions I made that work 

#API and CX keys
google_apikey = "AIzaSyA_w7fBUTy6JMCn9swEe-yibBzwfjuEB6s"
google_CX = "3024d6990d0a143ec"
ebird_api_key = 'v0b8g2g8kh7r'

flickr_api_key ="eaba8dca2a3c789e79cc7c3925643475"

flicker_secret = "d4d3dfb76ed7e3e4"

def com_to_sci(common_name):
    # make it not case sensitve 
    common_name = common_name.lower()
    scientific_name = species_data.loc[species_data['en_common'].str.lower() == common_name, 'scientific_name'].values[0]
    return scientific_name

def sci_to_com(scientific_name):
    scientific_name = scientific_name.lower()
    common_name = species_data.loc[species_data['scientific_name'].str.lower() == scientific_name, 'en_common'].values[0]
    return(common_name)

def list_types(sub_species):
    matching_names = species_data[species_data['en_common'].str.contains(sub_species, case=False)]['en_common'].tolist()
    return matching_names

#works in maps 
def com_des(common_name):
    common_name = common_name.replace(" ", "-")
    url = f"https://www.audubon.org/field-guide/bird/{common_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", class_="bird_discussion")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        return "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelling"

#does not work in maps
def sci_des(scientific_name):
    scientific_name = scientific_name.replace(" ", "_")
    url = f"https://picturebirdai.com/wiki/{scientific_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", {"id": "description-content"}).find("div", {"class": "field_value_description"}).find("div")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        return "Bird not found. Make sure you are inputing the proper scientfic name. Use function com_to_sci to get proper name"


# this does not work in maps yet bc of sci_des
def bird_description(common_name):
    common_name1 = common_name.replace(" ", "-")
    url = f"https://www.audubon.org/field-guide/bird/{common_name1}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    bird_div = soup.find("div", class_="bird_discussion")
    if bird_div is not None:
        return bird_div.text.strip()
    else:
        scientific_name = com_to_sci(common_name)
        if scientific_name is not None:
            scientific_name = scientific_name.replace(" ", "_")
            url = f"https://picturebirdai.com/wiki/{scientific_name}.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            bird_div = soup.find("div", {"id": "description-content"}).find("div", {"class": "field_value_description"}).find("div")
            if bird_div is not None:
                return bird_div.text.strip()
            else:
                return "Bird not found. Make sure you are inputting the proper scientific name. Use function com_to_sci to get the proper name"
        else:
            return "Bird not found on Audubon Bird Guide. The guide only has access to birds of North America. If the bird is in North America, check spelli

def wiki_pic(common_name):
    # Make a GET request to the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{common_name}"
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

        # Get the source URL of the image
        image_url = image["src"]

        # Make a GET request to the image URL
        response = requests.get("https:" + image_url)

        picture_url = ("https:" + image_url)
      
    # If there is no image in the infobox table, look for the first image in the thumbinner div
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

  def wiki_pic_map(common_name):
    # Make a GET request to the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{common_name}"
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

        # Get the source URL of the image
        image_url = image["src"]

        # Make a GET request to the image URL
        response = requests.get("https:" + image_url)

        # Encode the image content as base64
        image_data = base64.b64encode(response.content).decode()

        # Return the base64-encoded image data
        return image_data

    # If there is no image in the infobox table, look for the first image in the thumbinner div
    else:
        picbox = soup.find("div", class_=["thumbinner"])
        if picbox:
            # Find the first image in the thumbinner div
            image2 = picbox.find("img")

            # Get the source URL of the image
            image_url = image2["src"]

            # Make a GET request to the image URL
            response = requests.get("https:" + image_url)

            # Encode the image content as base64
            image_data = base64.b64encode(response.content).decode()

            # Return the base64-encoded image data
            return image_data

        # If no image is found, return None
        else:
            return None 

