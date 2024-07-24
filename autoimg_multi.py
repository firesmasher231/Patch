import multiprocessing
import random
import os
import aiohttp
import asyncio

async def fetch_image(session, data, headers):
    url = "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task/execute"
    
    async with session.post(url, headers=headers, data=data) as response:
        if response.status == 200:
            response_json = await response.json()
            image_url = response_json["results"][0]["value"]["url"]

            # Create a folder to save the images
            os.makedirs("images", exist_ok=True)

            # Download and save the image
            async with session.get(image_url) as image_response:
                if image_response.status == 200:
                    image_filename = f"images/downloaded_image_{random.randint(1, 100000)}.jpg"
                    with open(image_filename, "wb") as file:
                        file.write(await image_response.read())
                    print(f"Image downloaded successfully: {image_filename}")
                else:
                    print("Failed to download the image.")
        else:
            print("Failed to get a valid response from the server.")

def generate_random_data():
    # Generate random coordinates for location
    xmin = random.uniform(550000, 560000)
    ymin = random.uniform(650000, 660000)
    xmax = xmin + random.uniform(100, 500)
    ymax = ymin + random.uniform(100, 500)

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

    return data, headers

async def process_image(session):
    data, headers = generate_random_data()
    await fetch_image(session, data, headers)

async def main():
    num_images = 1000
    async with aiohttp.ClientSession() as session:
        tasks = [process_image(session) for _ in range(num_images)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    num_workers = multiprocessing.cpu_count()
    
    processes = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=asyncio.run, args=(main(),))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
