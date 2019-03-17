from botocore.vendored import requests
import json

api_key = '-2aFNxQXNgs0leCMSjogKhcsoDdMKYRojBQ-D-jStBRfk7KEcCO8H-CSKLqNRfugPLkM0yfap-PCRf9GEWhcEK_4wR2HkkP6zoIH7wLdgNqpOCtW3bdXdxUZG1SFXHYx'
headers = {'Authorization': 'Bearer %s' % api_key}
url = 'https://api.yelp.com/v3/businesses/search'


# search food from yelpFusion by paramter and return in parsed
def find_from_fusion(foodtype, location, date, time, amount):
    params = {'term': 'food', 'location': location, 'categories': foodtype}
    req = requests.get(url, params=params, headers=headers)
    parsed = json.loads(req.text)
    return parsed["businesses"]


# texts  = findfood('chinese','new york',1,1,1)["businesses"]
# for count in range(5):
#     print("Name:", texts[count]["name"])
#     print("Rating:", texts[count]["rating"])
#     print("Address:", " ".join(texts[count]["location"]["display_address"]))
#     print("Phone:", texts[count]["phone"])
#     print("\n")

# change parsed into list
def getlist(parsed):
    results = []
    for count in range(3):
        results.append(parsed[count])
    return results


# transform the url text into sentence
def trans_into_string(results):
    strings = ""
    for result in results:
        tempString = result["name"] + "in" + "".join(
            result["location"]["display_address"]) + " the phone number is" + " " + result["phone"]
        strings += tempString + ";"
    return strings


def findfood(foodtype, location, date, time, amount):
    parsed = find_from_fusion(foodtype, location, date, time, amount)
    results = getlist(parsed)
    return trans_into_string(results)


texts = findfood('chinese', 'new york', 1, 1, 1)
print(texts)
