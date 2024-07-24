import argparse
import random
import requests

def download_map_image(width, height):
    # Generate random coordinates for location
    xmin = random.uniform(550000, 560000)
    ymin = random.uniform(650000, 660000)
    xmax = xmin + random.uniform(100, 500)
    ymax = ymin + random.uniform(100, 500)
def download_map_image(width, height):



    # Define the variables
    url = 'https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task/execute'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://webapps.geohive.ie',
        'priority': 'u=1, i',
        'referer': 'https://webapps.geohive.ie/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    data = {
        'f': 'json',
        'Web_Map_as_JSON': (
            '{"mapOptions":{"showAttribution":true,"extent":{"xmin":550833.5766329573,"ymin":651360.0247826162,"xmax":551194.7336052713,'
            '"ymax":651590.7419107172,"spatialReference":{"wkid":2157,"latestWkid":2157}},"spatialReference":{"wkid":2157,"latestWkid":2157},'
            '"scale":1000},"operationalLayers":[{"id":"layer2","title":"layer2","opacity":1,"minScale":0,"maxScale":0,'
            '"url":"https://utility.arcgis.com/usrsvcs/servers/fa6c480e60fd48a2959d066e3e0a9b96/rest/services/MapGenieImagery2013to2018ITM/MapServer"},'
            '{"id":"Countries2020AdministrativeUnits_3013","title":"Countries 2020 - Administrative Units","opacity":0.7,"minScale":0,"maxScale":0,'
            '"layerDefinition":{"drawingInfo":{"renderer":{"type":"simple","label":"","description":"","symbol":{"color":[214,214,214,255],'
            '"outline":{"color":[214,214,214,255],"width":0.4,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}}},'
            '"definitionExpression":"(OBJECTID <> 97) AND (OBJECTID <> 259)"},"url":"https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/'
            'Countries2020AdministrativeUnits/FeatureServer/0"}],"exportOptions":{"outputSize":[%d,%d],"dpi":96},"layoutOptions":{"titleText":"",'
            '"authorText":"","copyrightText":"","customTextElements":[{"Date":"23/07/2024, 16:27:06"}],"scaleBarOptions":{"metricUnit":"esriKilometers",'
            '"metricLabel":"km","nonMetricUnit":"esriMiles","nonMetricLabel":"mi"},"legendOptions":{"operationalLayers":[]}}}' % (width, height),
        ),
        'Format': 'JPG',
        'Layout_Template': 'MAP_ONLY',
        'printFlag': 'true'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check the response status
    if response.status_code == 200:
        response_json = response.json()
        # Extract the image URL from the response
        image_url = response_json['results'][0]['value']['url']
        print(f"Image URL: {image_url}")

        # Download and save the image
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            with open('downloaded_image.jpg', 'wb') as file:
                file.write(image_response.content)
            print('Image downloaded successfully.')
        else:
            print('Failed to download the image.')
    else:
        print('Failed to get a valid response from the server.')

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Download map image with specified resolution.')
#     parser.add_argument('--width', type=int, default=500, help='Width of the image in pixels')
#     parser.add_argument('--height', type=int, default=500, help='Height of the image in pixels')

#     args = parser.parse_args()

#     download_map_image(args.width, args.height)

download_map_image(500,500)
