# from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Request
from timeseries import find_hotspots
import tt_parse_data as ttp

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/")
async def upload_files(
    # request: Request,
    browsing_history: UploadFile = File(None, alias="browsing-history"),
    # like_history: UploadFile = File(None, alias="like-history"),
    # search_history: UploadFile = File(None, alias="search-history"),
    # share_history: UploadFile = File(None, alias="share-history"),
    # favorite_history: UploadFile = File(None, alias="favorite-history"),
):
    print(browsing_history)
    # data = dict()
    # print(browsing_history)
    # print(like_history)
    # print(search_history)
    # print(share_history)
    # if browsing_history:
    #     print("browsing history uploaded")
    #     data["browsing"] = browsing_history
    #     ttp.parse_brows_hist(browsing_history, data, None)
    #     # find_hotspots(data["browsing"])
    # # if like_history:
    # #     data["liked"] = like_history
    # #     ttp.parse_liked(like_history, data, None)
    # # if search_history:
    # #     data["searches"] = search_history
    # #     ttp.parse_searches(search_history, data, None)
    # # if share_history:
    # #     data["shares"] = share_history
    # #     ttp.parse_shares(share_history, data, None)
    # # if favorite_history:
    # #     data["favorites"] = favorite_history
    # #     ttp.parse(browsing_history, data, None)
    # return {"message": "Files uploaded"}
