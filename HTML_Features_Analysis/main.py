from collections import Counter
from random import randint

from fastapi import FastAPI
from pydantic import BaseModel

from Database.database import databaseSearch
from HTML_main import HTML_feature_classification

app = FastAPI()

class RequestPayload(BaseModel):
    text: str


@app.get("/cyberHunter")
def predict_output():
    prediction = randint(0, 1)
    return {"predictions": prediction}


@app.post("/cyberHunter/post")
async def receive_message(payload: RequestPayload):
    # call database
    url = payload.text

    print(url)

    pred_list = []

    if url is not None:
        # check URL on database 
        # for url_item in url:
        print("url in item is :"+url)
        databaseReturn = databaseSearch(url)
        if databaseReturn is not None:
            pred_list.append(databaseReturn)
        else:
            RF_predicted_label,  = call_URL_models(url)
            pred_list.append(RF_predicted_label)

    print(pred_list)
    most_common_prediction = Counter(pred_list).most_common(1)[0][0]

    # count predictions
    # if RF_predicted_label and BERT_predicted_label is not None:
    #     if RF_predicted_label == BERT_predicted_label:
    #         print("HTML classification says URL is Phishing or legitimate")

    print(most_common_prediction)

    return {"predictions": most_common_prediction}


def call_URL_models(url):
    # check url from database 
    
    # distillBERT_prediction = predict_url(url)
    RF_predicted_label = HTML_feature_classification(url)
    # XGBoost_prediction = XGBoost_Predictions(url)

    # return XGBoost_prediction, distillBERT_prediction, RF_predicted_label, BERT_predicted_label
    return RF_predicted_label


