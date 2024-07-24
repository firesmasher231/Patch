import argparse
import random
import requests
import os

import concurrent.futures


def generate_random_image():
    # Generate random coordinates for location
    xmin = random.uniform(550000, 560000)
    ymin = random.uniform(650000, 660000)
    xmax = xmin + random.uniform(100, 500)
    ymax = ymin + random.uniform(100, 500)

    # Define the variables
    url = "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task/execute"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://webapps.geohive.ie",
        "priority": "u=1, i",
        "referer": "https://webapps.geohive.ie/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    data = {
        "f": "json",
        "Web_Map_as_JSON": (
            '{"mapOptions":{"showAttribution":true,"extent":{"xmin":'
            + str(xmin)
            + ',"ymin":'
            + str(ymin)
            + ',"xmax":'
            + str(xmax)
            + ',"ymax":'
            + str(ymax)
            + ',"spatialReference":{"wkid":2157,"latestWkid":2157}},"spatialReference":{"wkid":2157,"latestWkid":2157},"scale":1000},"operationalLayers":[{"id":"layer2","title":"layer2","opacity":1,"minScale":0,"maxScale":0,"url":"https://utility.arcgis.com/usrsvcs/servers/fa6c480e60fd48a2959d066e3e0a9b96/rest/services/MapGenieImagery2013to2018ITM/MapServer"},{"id":"Countries2020AdministrativeUnits_3013","title":"Countries 2020 - Administrative Units","opacity":0.7,"minScale":0,"maxScale":0,"layerDefinition":{"drawingInfo":{"renderer":{"type":"simple","label":"","description":"","symbol":{"color":[214,214,214,255],"outline":{"color":[214,214,214,255],"width":0.4,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}}},"definitionExpression":"(OBJECTID <> 97) AND (OBJECTID <> 259)"},"url":"https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Countries2020AdministrativeUnits/FeatureServer/0"}],"exportOptions":{"outputSize":[500,500],"dpi":96},"layoutOptions":{"titleText":"","authorText":"","copyrightText":"","customTextElements":[{"Date":"23/07/2024, 16:27:06"}],"scaleBarOptions":{"metricUnit":"esriKilometers","metricLabel":"km","nonMetricUnit":"esriMiles","nonMetricLabel":"mi"},"legendOptions":{"operationalLayers":[]}}}'
        ),
        "Format": "JPG",
        "Layout_Template": "MAP_ONLY",
        "printFlag": "true",
    }
    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check the response status
    if response.status_code == 200:
        response_json = response.json()
        # Extract the image URL from the response
        image_url = response_json["results"][0]["value"]["url"]
        print(f"Image URL: {image_url}")

        # Create a folder to save the images
        os.makedirs("images", exist_ok=True)

        # Download and save the image
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            image_filename = f"images/downloaded_image_{random.randint(1, 100000)}.jpg"
            with open(image_filename, "wb") as file:
                file.write(image_response.content)
            print(f"Image downloaded successfully: {image_filename}")
        else:
            print("Failed to download the image.")
    else:
        print("Failed to get a valid response from the server.")


# Number of agents (threads) to use
num_agents = 200

# Create a ThreadPoolExecutor with the specified number of agents
with concurrent.futures.ThreadPoolExecutor(max_workers=num_agents) as executor:
    print("Generating random images...")
    # Generate 1000 random images with random coordinates using multiple threads
    while True:
        executor.submit(generate_random_image)

