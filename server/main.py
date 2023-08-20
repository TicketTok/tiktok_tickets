from fastapi import FastAPI, UploadFile
import tiktok_data_parsers as parser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Server is running."}


@app.post("/upload/")
async def upload_files(
    browsing_history: UploadFile,
    like_history: UploadFile,
    favorite_history: UploadFile,
    comment_history: UploadFile,
    search_history: UploadFile,
    share_history: UploadFile,
):
    data = dict()
    if browsing_history:
        try:
            data["browsing"] = await parser.parse_date_id(browsing_history)
        except Exception as e:
            print(f"Error occured parsing browsing history: {e}")
        finally:
            await browsing_history.close()
    if like_history:
        try:
            data["liked"] = await parser.parse_date_id(like_history)
        except Exception as e:
            print(f"Error occured parsing like history: {e}")
        finally:
            await like_history.close()
    if favorite_history:
        try:
            data["favorites"] = await parser.parse_date_id(favorite_history)
        except Exception as e:
            print(f"Error occured parsing favorite history: {e}")
        finally:
            await favorite_history.close()
    if comment_history:
        try:
            data["comments"] = await parser.parse_comments(comment_history)
        except Exception as e:
            print(f"Error occured parsing comment history: {e}")
        finally:
            await comment_history.close()
    if search_history:
        try:
            data["searches"] = await parser.parse_searches(search_history)
        except Exception as e:
            print(f"Error occured parsing comment history: {e}")
        finally:
            await comment_history.close()
    if share_history:
        try:
            data["shares"] = await parser.parse_shares(share_history)
        except Exception as e:
            print(f"Error occured parsing comment history: {e}")
        finally:
            await comment_history.close()

    return {"message": "Files uploaded"}
