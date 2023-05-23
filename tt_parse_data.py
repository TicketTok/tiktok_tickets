from typing import Any
from TikTokApi import TikTokApi
import supabase as sb
import os
from datetime import datetime

sb_url: str = os.environ.get("SUPABASE_URL")
sb_key: str = os.environ.get("SUPABASE_KEY")
sb_cli: sb.Client = sb.create_client(sb_url, sb_key)


# Should send all the items to the server... pretty poor workflow however
def parse_all_tts(entries: dict, limit: int) -> str:
    # Only need browsing history
    if entries["brows_hist"] is not None:
        # Find reference month, only using limited months of data
        first_line: str = entries["brows_hist"].readline().strip().decode("UTF-8")
        entries["brows_hist"].seek(0)
        ref_month: int = int(datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S").strftime("%m"))

        # Basic parsing of Date and ID + supabase and API calls
        current_video: dict = {}
        final_list: list = []
        api_response: str = ""
        for line in entries["brows_hist"]:
            line: str = line.strip().decode("UTF-8")
            # Can check lines here using print:
            if line.startswith("Date:"):
                datetime_obj: datetime = datetime.strptime(line, "Date: %Y-%m-%d %H:%M:%S")
                current_video["date"]: str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            elif line.startswith("Link:"):
                current_video["id"]: str = line.split("/")[-2].strip()
            elif line == "":
                if "id" in current_video and "date" in current_video:
                    final_list.append(current_video.copy())

                    check_limit: str = datetime.strptime(current_video["date"],
                                                    "%Y-%m-%d %H:%M:%S").strftime("%m")
                    if int(check_limit) + limit < ref_month:
                        api_response = str(sb_cli.table("tiktoks").upsert({"id": current_video["id"],
                                                                           "viewed_at": current_video["date"]},
                                                                          on_conflict="id").execute())

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
