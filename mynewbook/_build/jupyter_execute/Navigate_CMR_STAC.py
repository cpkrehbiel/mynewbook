#!/usr/bin/env python
# coding: utf-8

# ---
# # 1. Getting Started <a id="getstarted"></a>

# ## 1.1 Import Packages <a id="1.1"></a>
# #### Import the required packages and set the input/working directory to run this Jupyter Notebook locally.

# In[1]:


import requests as r
from skimage import io
import matplotlib.pyplot as plt


# ---
# # 2. Navigating the CMR-STAC API <a id="navigatestac"></a>
# #### Learn about navigating NASA's Common Metadata Repository (CMR) SpatioTemporal Asset Catalog ([STAC](https://stacspec.org/)) API.  

# ## 2.1 Introduction to the CMR-STAC API <a id="2.1"></a>
# ### What is STAC?
# > STAC is a specification that provides a common language for interpreting geospatial information in order to standardize indexing and discovering data. 
# ### Four STAC Specifications:
# 1. [STAC API](https://github.com/radiantearth/stac-api-spec)  
# 2. [STAC Catalog](https://github.com/radiantearth/stac-spec/blob/master/catalog-spec/catalog-spec.md)  
# 3. [STAC Collection](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md)  
# 4. [STAC Item](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md)  
# #### In the section below, we will walk through an example of each specification. For additional information, check out: https://stacspec.org/. 

# ### 1. STAC API: Endpoint that enables the querying of STAC items.
# #### Below, set the CMR-STAC API Endpoint to a variable, and use the `requests` package to send a GET request to the endpoint, and set the response to a variable.

# In[2]:


stac = 'https://cmr.earthdata.nasa.gov/stac/' # CMR-STAC API Endpoint
stac_response = r.get(stac).json()            # Call the STAC API endpoint
for s in stac_response: print(s)


# In[3]:


print(f"You are now using the {stac_response['id']} API (STAC Version: {stac_response['stac_version']}). {stac_response['description']}")
print(f"There are {len(stac_response['links'])} STAC catalogs available in CMR.")


# #### You will notice above that the CMR-STAC API contains many different endpoints--not just from NASA LP DAAC, but also contains endpoints for other NASA ESDIS DAACs.
# ### 2. STAC Catalog: Contains a JSON file of links that organize all of the collections available. 
# #### Below, search for LP DAAC Catalogs, and print the information contained in the Catalog that we will be using today, `LPCLOUD`.

# In[4]:


stac_lp = [s for s in stac_response['links'] if 'LP' in s['title']]  # Search for only LP-specific catalogs

# LPCLOUD is the STAC catalog we will be using and exploring today
lp_cloud = r.get([s for s in stac_lp if s['title'] == 'LPCLOUD'][0]['href']).json()
for l in lp_cloud: print(f"{l}: {lp_cloud[l]}")


# #### Below, print the links contained in the LP CLOUD STAC Catalog:

# In[5]:


lp_links = lp_cloud['links']
for l in lp_links: 
    try: 
        print(f"{l['href']} is the {l['title']}")
    except:
        print(f"{l['href']}")       


# ### 3. STAC Collection: Extension of STAC Catalog containing additional information that describe the STAC Items in that Collection.
# #### Below, get a response from the LPCLOUD Collection and print the information included in the response.

# In[6]:


lp_collections = [l['href'] for l in lp_links if l['rel'] == 'collections'][0]  # Set collections endpoint to variable
collections_response = r.get(f"{lp_collections}").json()                        # Call collections endpoint
print(f"This collection contains {collections_response['description']} ({len(collections_response['collections'])} available)")


# #### As of March 3, 2021, there are three collections available, and more will be added in the future. 
# #### Print out one of the collections:

# In[7]:


collections = collections_response['collections']
collections[1]


# #### In CMR, `id` is used to query by a specific product, so be sure to save the ID for the HLS S30 and L30 V1.5 products below:

# In[8]:


# Search available collections for HLS and print them out
hls_collections = [c for c in collections if 'HLS' in c['title']]
for h in hls_collections: print(f"{h['title']} has an ID (shortname) of: {h['id']}")


# > #### Note that the "id" shortname is in the format: productshortname.vVVV (where VVV = product version)

# #### Explore the attributes contained in the HLSS30 Collection.

# In[9]:


s30 = [h for h in hls_collections if h['id'] == 'HLSS30.v1.5'][0]  # Grab HLSS30 collection
for s in s30['extent']: print(f"{s}: {s30['extent'][s]}")          # Check out the extent of this collection


# #### So here we can see that the extent is global, and can also see the temporal range--where "None" means on-going or to present.

# In[10]:


print(f"HLS S30 Start Date is: {s30['extent']['temporal']['interval'][0][0]}")
s30_id = s30['id']


# #### Next, explore the attributes of the HLSL30 collection.

# In[11]:


l30 = [h for h in hls_collections if h['id'] == 'HLSL30.v1.5'][0]     # Grab HLSL30 collection
for l in l30['extent']: print(f"{l}: {l30['extent'][l]}")             # Check out the extent of this collection
print(f"HLS L30 Start Date is: {l30['extent']['temporal']['interval'][0][0]}")
l30_id = l30['id']


# #### Above, notice that the L30 product has a different start date than the S30 product. 

# ### 4. STAC Item: Represents data and metadata assets that are spatiotemporally coincident
# #### Below, query the HLSS30 collection for items and return the first item in the collection. 

# In[12]:


# Below, go through all links in the collection and return the link containing the items endpoint
s30_items = [s['href'] for s in s30['links'] if s['rel'] == 'items'][0]  # Set items endpoint to variable
s30_items


# In[13]:


s30_items_response = r.get(f"{s30_items}").json()                        # Call items endpoint
s30_item = s30_items_response['features'][0]                             # select first item (10 items returned by default)
s30_item


# #### STAC metadata provides valuable information on the item, including a unique ID, when it was acquired, the location of the observation, and a cloud cover assessment.  

# In[14]:


# Print metadata attributes from this observation
print(f"The ID for this item is: {s30_item['id']}")
print(f"It was acquired on: {s30_item['properties']['datetime']}")
print(f"over: {s30_item['bbox']} (Lower Left, Upper Right corner coordinates)")
print(f"It contains {len(s30_item['assets'])} assets")
print(f"and is {s30_item['properties']['eo:cloud_cover']}% cloudy.")


# #### Below, print out the ten items and the percent cloud cover--we will use this to decide which item to visualize in the next section. 

# In[15]:


for i, s in enumerate(s30_items_response['features']):
    print(f"Item at index {i} is {s['properties']['eo:cloud_cover']}% cloudy.")


# #### Using the information printed above, set the `item_index` below to whichever observation is the least cloudy above.

# In[16]:


item_index = 9  # Indexing starts at 0 in Python, so here select the eighth item in the list at index 7


# In[17]:


s30_item = s30_items_response['features'][item_index]  # Grab the next item in the list

print(f"The ID for this item is: {s30_item['id']}")
print(f"It was acquired on: {s30_item['properties']['datetime']}")
print(f"over: {s30_item['bbox']} (Lower Left, Upper Right corner coordinates)")
print(f"It contains {len(s30_item['assets'])} assets")
print(f"and is {s30_item['properties']['eo:cloud_cover']}% cloudy.")


# #### Below, print out the names of all of the assets included in this item.

# In[18]:


print("The following assets are available for download:")
for a in s30_item['assets']: print(a)


# #### Notice that each HLS item includes a browse image. Read the browse file into memory and visualize the HLS acquisition.

# In[19]:


s30_item['assets']['browse']


# #### Use the `skimage` package to load the browse image into memory and `matplotlib` to quickly visualize it.

# In[20]:


image = io.imread(s30_item['assets']['browse']['href'])  # Load jpg browse image into memory

# Basic plot of the image
plt.figure(figsize=(10,10))              
plt.imshow(image)
plt.show()


# #### Congrats! You have visualized your first Cloud-Native HLS asset!
