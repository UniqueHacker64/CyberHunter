import requests

# defined API keys
api_key1 = 'be27b1069c0152da757743e2633c87f7de986eb97882cba775389e90e276ad36'  # 1st API key
api_key2 = '3b08f42c871f4a56c6cdd8a89065c85f7af0a4fa27c5a247891517f1d1635efa' # 2nd API key
api_endpoint = 'https://www.virustotal.com/vtapi/v2/url/report' # URL scan endpoint


def VirusTotal1(url_to_check):
    # Set up the parameters
    if api_key1:
        params = {'apikey': api_key1, 'resource': url_to_check}

        # Make the API request
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            
            # Check the response for scan results
            if result['response_code'] == 1:
                print(f"input URL: {result['resource']}")
                # print(f"Scan Date: {result['scan_date']}")
                # print(f"Total Scans: {result['total']}")
                # print(f"Positive Scans: {result['positives']}")

                if result['positives'] == 0:
                    # print("URL is legitimate")
                    predicted_label = 0
                elif result['positives'] > 3:
                    # print("URL is possibly suspicious")
                    predicted_label = 1
                else:
                    # print("URL is suspicious")
                    predicted_label = 0

                # Print detailed scan results if needed
                # print(f"Scan Results: {result['scans']}")
            else:
                # print(f"Scan Results: {result['scans']}")
                print("URL not found in Virus Totall database.")
                predicted_label = None

        elif response.status_code == 204:
            print("You have exceeded")
            # print("Use Virustotal redundent API for predictions")

            predicted_label = VirusTotal2(url_to_check)

    else:
        print("You need to provide an API key to use this script.")
        predicted_label = None

    return predicted_label

def VirusTotal2(url):
    if api_key2:
        params = {'apikey': api_key2, 'resource': url}

        # Make the API request
        response = requests.get(api_endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            
            # Check the response for scan results
            if result['response_code'] == 1:
                print(f"URL Input: {result['resource']}")
                # print(f"Scan Date: {result['scan_date']}")
                # print(f"Total Scans: {result['total']}")
                # print(f"Positive Scans: {result['positives']}")

                if result['positives'] == 0:
                    # print("URL is legitimate")
                    predicted_label = 0
                elif result['positives'] > 3:
                    # print("URL is possibly suspicious")
                    predicted_label = 1
                else:
                    # print("URL is suspicious")
                    predicted_label = 0

                # Print detailed scan results if needed
                # print(f"Scan Results: {result['scans']}")
            else:
                # print(f"Scan Results: {result['scans']}")
                print("URL not found in Large database.")
                predicted_label = None

        elif response.status_code == 204:
            print("You have exceeded 2nd API request ")
            predicted_label = None 

    else:
        print("You need to provide an API key to use this script.")
        predicted_label = None

    return predicted_label

def virusToalCall(recived_url):
    prediction = VirusTotal1(recived_url)
    return prediction

# # URL to check
# url_to_check = 'http://bit.ly/3R9vepy'
# prediction = virusToalCall(url_to_check)
# print("predicted output is:",prediction)