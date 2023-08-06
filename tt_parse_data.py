import supabase as sb
import os
from datetime import datetime
import pandas as pd
import requests

sb_url = os.environ.get("SUPABASE_URL")
sb_key = os.environ.get("SUPABASE_KEY")
sb_cli = sb.create_client(sb_url, sb_key)
dataframe_dict = {}


# Should send all the items to the server... pretty poor workflow however
def parse_all_tts(entries: dict, limit: int) -> str:
    # Only need browsing history
    if entries["brows_hist"] is not None:
        # Find reference month, only using limited months of data
        first_line = entries["brows_hist"].readline().strip().decode("UTF-8")
        entries["brows_hist"].seek(0)
        ref_month = int(datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S").strftime("%m"))

        # Basic parsing of Date and ID + supabase and API calls
        current_video = {}
        final_list = []
        api_response = ""
        for data in entries["brows_hist"]:
            line = data.strip().decode("UTF-8")
            # Can check lines here using print:
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(line, "Date: %Y-%m-%d %H:%M:%S")
                current_video["viewed_at"] = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            elif line.startswith("Link:"):
                current_video["id"] = line.split("/")[-2].strip()
                # url = requests.head(line.split("Link: ")[1].strip(), allow_redirects=True)
                # url_list.append(url.url)
            elif line == "":
                if "id" in current_video and "viewed_at" in current_video:
                    final_list.append(current_video.copy())
                    check_limit = datetime.strptime(current_video["viewed_at"],
                                                    "%Y-%m-%d %H:%M:%S").strftime("%m")
                    if int(check_limit) + limit < ref_month:
                        # api_response = str(sb_cli.table("tiktoks").upsert(final_list,
                        #                                                   on_conflict="id",
                        #                                                   ignore_duplicates=True).execute())
                        watch_history_df = pd.DataFrame(columns=["id", "viewed_at"], data=final_list)
                        print(watch_history_df)
                        dataframe_dict['watch_history'] = watch_history_df
                        break
                    current_video.clear()
    else:
        raise FileNotFoundError("This should not happen.")

    return "Finished sending all Tik Toks! " + api_response


def parse_personal_tts(entries: dict, limit: int, acc_id: int) -> str:
    # Liked Videos
    if entries["liked"] is not None:
        print("Liked!")
    else:
        raise FileNotFoundError("This should not happen.")

    # Searched Videos (not required)
    if entries["searched"] is not None:
        print("Searched!")

    # Shared Videos (not required)
    if entries["shared"] is not None:
        print("Shared!")

    # Favorite Videos (not required)
    if entries["favorites"] is not None:
        print("Favorited")

    return "done parsing!"
