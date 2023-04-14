# better_ebirdAPI 

This python package was created for a Concordia Univeristy Geog464: Programming for Geospatial technologies class. The package is made for birders using the ebirdAPI. 

A tutorial using the module can be found in the .ipynd file "Using_better_ebirdAPI_Module". For those who want to understand how the module was created see the .ipynd file "better_ebirdAPI_tutorial".

Some of the functions require a google API key but they are not necessary if the user doesn't have one. The maping functions ending with "GAPI" have been found to more consitantly return/load pictures with the maps. The reasonings for why some images do not appear in the maps is unclear, we can assume that its due to the amount of data the function is going through. 

**This package contains the following functions**
1. ***com_to_sci*** - This function allows the user to input the *common name of any bird and retrives the scientific name for said bird.* This is done using the file "PFW-species-translation-table.csv" which was retrieved from the [ebird data access](https://ebird.org/data/download)
2. ***sci_to com*** - This function allows the user to input the *scientific name of any bird and retrives the common name for said bird*. This is done using the file "PFW-species-translation-table.csv" which was retrieved from the [ebird data access](https://ebird.org/data/download)
3. **list_types** - This function name matches a list of bird using a key word. Some examples of key words include "duck", "wren", "blackbird" ... etc. This function will compile a list of bird and can be used to identify species of bird types. 
4. **com_des** - This function was created to be used within *bird_description*. It scrapes [audubon.org](https://www.audubon.org/field-guide/bird/) using the common name as query to retrive a description of the inputted bird. This website only searches birds of North America
5. **sci_des**- This function was created to be used within *bird_description*. It scrapes [picturebirdai.com](https://picturebirdai.com/wiki/.html) using the scientific name as query to retrive a description of the inputted bird. This website searches birds of the world
6. **bird_description** - This function was created by combining *com_des* and *sci_des**. Users input the common name of any bird and retieves a description of said bird. 
7. **google_API_pic** - This function uses a Google API and Google CX key. For those who do not have access to a google api key, wiki pic functions the same. The function retrives pictures of any specified bird by searching google images. 
8. **google_API_pic4map** - This function uses the Google API and Google CX to retrive the image and encode it to be used within the mapping functions ending with GAPI. 
9. **wiki_pic** - This function retrives picture of any specified bird by scraping [wikipedia](https://en.wikipedia.org/wiki/Main_Page). It can be used by those who don't have access to a google API. 
11. **wiki_pic_map** - This function scrapes wikipedia to retrive the image and encode it to be used within the mapping functions. 
12. **retrieve_species_data** - this function uses the ebirdAPI to reieve basic data on any inputed species. It requires the scientific name of the specified bird. If the user doesnt know the scientific name they may use the *com_to_sci* function
13. **nearby_observations**- This function creates a map which shows the most recent observations of a specified area. It takes in the lat/lng coordinates and a radius in km. This can be used by those curious about the birds within any area. It calls on some of functions previously mentioned in order to provide information inclusing a description and picture of the bird within the marker popup. 
14. **nearby_observations_GAPI**- This function is equivalent to *nearby_observations* but uses google API keys and the functions associated with Google API. 
15. **nearby_bird** - This function creates a map which shows the most recent observations of a specified bird, with a default radius of 10km It calls on some of functions previously mentioned in order to provide information inclusing a description and picture of the bird within the marker popup.
16. **nearby_bird_GAPI** - This function is equivalent to *nearby_bird* but uses google API keys and the functions associated with Google API. 
17. **notable_bird** - This function creats a map of notable or rare birds within a specified area. It calls on some of functions previously mentioned in order to provide information inclusing a description and picture of the bird within the marker popup.
18. **notable_bird_GPI** - This function is equivalent to *notable_bird* but uses google API keys and the functions associated with Google API.
19. **gethotspot** - This function provides a list of hotspots within 5km of a specifed area. It helps users find where people frequently bird watch near their location.

