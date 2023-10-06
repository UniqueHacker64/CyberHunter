# import time
import pandas as pd
import pickle
import warnings
import urllib.request
warnings.filterwarnings("ignore", category=RuntimeWarning)
# import ssl
from extract_numarical_values_functions import extract_numarical_values, extract_links
# from HTML_Features_Analysis.Database import VirusTotalCall


def HTML_feature_classification(url):
    # url = expand_short_url(url)
    print(url)

    # get numarical values from extract_numarical_values in internal_external.py file 
    script_ratio, css_ratio, img_ratio, a_tag_ratio, a_tag_null_ratio, null_ratio, form_count, total_links = extract_numarical_values(
        url)
    # print(script_ratio, css_ratio, img_ratio, a_tag_ratio, a_tag_null_ratio, null_ratio, form_count, total_links)

    results = extract_links(total_links, url)
    if results is not None:
        Internal_Links_Ratio, External_Links_Ratio, External_to_Internal_Ratio, error_hyperlinks_ratio = results
        # print(results)

    # load trained random forest model
    MODELSPATH = 'HTML_Features_Analysis\models\RF_model.pkl'
    # Load the saved model
    with open(MODELSPATH, 'rb') as f:
        rf = pickle.load(f)

    # Define a new sample to predict
    new_sample = {
        'script_ratio': script_ratio,
        'css_ratio': css_ratio,
        'img_ratio': img_ratio,
        'a_ratio': a_tag_ratio,
        'a_null_ratio': a_tag_null_ratio,
        'null_ratio': null_ratio,
        'internal_links_ratio': Internal_Links_Ratio,
        'external_links_ratio': External_Links_Ratio,
        'external_to_internal_ratio': External_to_Internal_Ratio,
        'form_count': form_count,
        'error_link_count': error_hyperlinks_ratio
    }

    # Convert the new sample to a DataFrame and predict its label
    # ========HTML tag features Prediction ============
    new_sample_df = pd.DataFrame([new_sample])
    RF_predicted_label_list = rf.predict(new_sample_df)
    RF_predicted_label = RF_predicted_label_list[0]
    # print("RF Predicted label:", RF_predicted_label)

    return RF_predicted_label

def print_dotted_box(message):
    line = '─' * (len(message) + 4)
    print(f'┌{line}┐')
    print(f'│  {message}  │')
    print(f'└{line}┘')


# ===================== Check URL for 400 range status codes ======================= #
def check_urls_for_400_range(url):
    try:
        with urllib.request.urlopen(url) as response:
            status_code = response.getcode()
            return status_code

    except urllib.error.URLError as e:
        # print(f"Error occurred while retrieving HTML content for URL: {url}: {e}")
        return 'error'
    except Exception as e:
        # print(f"Error processing file {url}: {e}")
        return 'error'


# ===================== Main Function ======================= #
# url = 'https://courseweb.sliit.lk/'



# call to virustotal API
# responseFromAPI = virusToalCall(url)
# responseFromAPI = None
# if responseFromAPI is not None:
#     RF_predicted_label = responseFromAPI
# else:
def mainFunction(url):
    errors = check_urls_for_400_range(url)
    if errors == 'error':
        # print("URL is not legitimate is blocking access to the website.")
        RF_predicted_label =1
    else:
        RF_predicted_label= HTML_feature_classification(url)

    # # ===================== Print Predictions Output =======================
    if RF_predicted_label == 1:
        prediction = 'Phishing website'
    else:
        prediction = 'Legitimate website'

    # Print the prediction in a dotted box
    print("\n-----------HTML Classifier Prediction----------------")
    print("URL:", url)
    print("RF predicted Label:", RF_predicted_label)
    print_dotted_box(prediction)

    return RF_predicted_label

