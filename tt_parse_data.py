import supabase as sb
import os
from datetime import datetime
import pandas as pd
import werkzeug.datastructures.file_storage as file_storage

# sb_url = os.environ.get("SUPABASE_URL")
# sb_key = os.environ.get("SUPABASE_KEY")
# sb_cli = sb.create_client(sb_url, sb_key)


# Should send all the items to the server... pretty poor workflow however
def parse_brows_hist(brows_hist: file_storage, dataframe_dict: dict, limit_in_days: int or None) -> str:
    # Only need browsing history
    if brows_hist is not None:
        # Find reference month, only using limited months of data
        first_line = brows_hist.readline().strip().decode("UTF-8")
        brows_hist.seek(0)
        ref_month = datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S")

        # Basic parsing of Date and ID + supabase and API calls
        current_video = {}
        final_list = []
        for data in brows_hist:
            line = data.strip().decode("UTF-8")
            # Stripping date in standard format from brows_hist
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(
                    line, "Date: %Y-%m-%d %H:%M:%S")
                current_video["viewed_at"] = datetime_obj.strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Link:"):
                current_video["id"] = line.split("/")[-2].strip()
                # url = requests.head(line.split("Link: ")[1].strip(), allow_redirects=True)
                # url_list.append(url.url)
            elif line == "":
                # Finishes one complete Video Object
                if "id" in current_video and "viewed_at" in current_video:
                    final_list.append(current_video.copy())
                    check_limit = datetime.strptime(current_video["viewed_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        # api_response = str(sb_cli.table("tiktoks").upsert(final_list,
                        #                                                   on_conflict="id",
                        #                                                   ignore_duplicates=True).execute())
                        break
                    current_video.clear()
        watch_history_df = pd.DataFrame(
            columns=["id", "viewed_at"], data=final_list)
        # print(watch_history_df)
        dataframe_dict['watch_history'] = watch_history_df
    else:
        raise FileNotFoundError("Brows_hist File Error - This should not happen.")

    return "Parsed Browsing History"


def parse_liked(liked: file_storage, dataframe_dict: dict, limit: int) -> str:
    if liked is not None:
        "ok"
    else:
        raise FileNotFoundError("Liked File Error - This should not happen.")
    return "Parsed Liked Videos"
