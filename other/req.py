

def validate_school(school_name):
    url_find = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params_find = {
        "input": school_name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": "AIzaSyA69VnOMSSxL4jyEro_pyNBbJn8oMQoQhI"
    }
    response_find = requests.get(url_find, params=params_find)
    if response_find.status_code == 200:
        data_find = response_find.json()
        if data_find["candidates"]:
            place_id = data_find["candidates"][0]["place_id"]
            url_details = "https://maps.googleapis.com/maps/api/place/details/json"
            params_details = {
                "place_id": place_id,
                "fields": "name,address_component,type",
        "key": "AIzaSyA69VnOMSSxL4jyEro_pyNBbJn8oMQoQhI"
            }
            response_details = requests.get(url_details, params=params_details)
            if response_details.status_code == 200:
                data_details = response_details.json()
                if "school" in data_details["result"]["types"]:
                    school_info = {
                        "name": data_details["result"]["name"],
                        "address": " ".join([component["long_name"] for component in data_details["result"]["address_components"]])
                    }
                    return school_info
    return None
