import supabase as sb
import os
from datetime import datetime
import pandas as pd
import werkzeug.datastructures.file_storage as file_storage

# sb_url = os.environ.get("SUPABASE_URL")
# sb_key = os.environ.get("SUPABASE_KEY")
# sb_cli = sb.create_client(sb_url, sb_key)


# Parsing each file from the TikTok Data Download separately.
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
            elif line == "":
                # Finishes one complete Video Object
                if "id" in current_video and "viewed_at" in current_video:
                    final_list.append(current_video.copy())
                    check_limit = datetime.strptime(current_video["viewed_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        break
                    current_video.clear()
        watch_history_df = pd.DataFrame(
            columns=["id", "viewed_at"], data=final_list)
        # print(watch_history_df)
        dataframe_dict['watch_history'] = watch_history_df
    else:
        raise FileNotFoundError("Brows_hist File Error - This should not happen.")
    return "Parsed Browsing History"


def parse_liked(liked: file_storage, dataframe_dict: dict, limit_in_days: int or None) -> str:
    if liked is not None:
        # Find reference month, only using limited months of data
        first_line = liked.readline().strip().decode("UTF-8")
        liked.seek(0)
        ref_month = datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S")

        # Basic parsing of Date and ID + supabase and API calls
        current_video = {}
        final_list = []
        for data in liked:
            line = data.strip().decode("UTF-8")
            # Stripping date in standard format from liked
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(
                    line, "Date: %Y-%m-%d %H:%M:%S")
                current_video["liked_at"] = datetime_obj.strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Link:"):
                current_video["id"] = line.split("/")[-2].strip()
            elif line == "":
                # Finishes one complete Video Object
                if "id" in current_video and "liked_at" in current_video:
                    final_list.append(current_video.copy())
                    check_limit = datetime.strptime(current_video["liked_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        break
                    current_video.clear()
        liked_df = pd.DataFrame(columns=["id", "liked_at"], data=final_list)
        # print(liked_df)
        dataframe_dict['liked'] = liked_df
    else:
        raise FileNotFoundError("Liked File Error - This should not happen.")
    return "Parsed Liked Videos"


def parse_comments(comments: file_storage, dataframe_dict: dict, limit_in_days: int or None) -> str:
    if comments is not None:
        # Find reference month, only using limited months of data
        first_line = comments.readline().strip().decode("UTF-8")
        comments.seek(0)
        ref_month = datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S")

        # Basic parsing of Date and ID + supabase and API calls
        current_comment = {}
        final_list = []
        for data in comments:
            line = data.strip().decode("UTF-8")
            # Stripping date in standard format from comments
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(
                    line, "Date: %Y-%m-%d %H:%M:%S")
                current_comment["commented_at"] = datetime_obj.strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Comment:"):
                current_comment["comment"] = line.split("Comment:", 1)[-1].strip()
            elif line == "":
                # Finishes one complete Video Object
                if "comment" in current_comment and "commented_at" in current_comment:
                    final_list.append(current_comment.copy())
                    check_limit = datetime.strptime(current_comment["commented_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        break
                    current_comment.clear()
        comments_df = pd.DataFrame(columns=["comment", "commented_at"], data=final_list)
        # print(comments_df)
        dataframe_dict['comments'] = comments_df
    else:
        raise FileNotFoundError("Comments File Error - This should not happen.")
    return "Parsed Comments"


def parse_searches(searches: file_storage, dataframe_dict: dict, limit_in_days: int or None) -> str:
    if searches is not None:
        # Find reference month, only using limited months of data
        first_line = searches.readline().strip().decode("UTF-8")
        searches.seek(0)
        ref_month = datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S")

        # Basic parsing of Date and ID + supabase and API calls
        current_search = {}
        final_list = []
        for data in searches:
            line = data.strip().decode("UTF-8")
            # Stripping date in standard format from searches
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(
                    line, "Date: %Y-%m-%d %H:%M:%S")
                current_search["searched_at"] = datetime_obj.strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Search Term:"):
                current_search["query"] = line.split("Search:", 1)[-1].strip()
            elif line == "":
                # Finishes one complete Search Object
                if "query" in current_search and "searched_at" in current_search:
                    final_list.append(current_search.copy())
                    check_limit = datetime.strptime(current_search["searched_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        break
                    current_search.clear()
        searches_df = pd.DataFrame(columns=["query", "searched_at"], data=final_list)
        # print(searches_df)
        dataframe_dict['searches'] = searches_df
    else:
        raise FileNotFoundError("Comments File Error - This should not happen.")
    return "Parsed Searches"


def parse_shares(shares: file_storage, dataframe_dict: dict, limit_in_days: int or None):
    if shares is not None:
        # Find reference month, only using limited months of data
        first_line = shares.readline().strip().decode("UTF-8")
        shares.seek(0)
        ref_month = datetime.strptime(first_line, "Date: %Y-%m-%d %H:%M:%S")

        # Basic parsing of Date and ID + supabase and API calls
        current_share = {}
        final_list = []
        for data in shares:
            line = data.strip().decode("UTF-8")
            # Stripping date in standard format from shares
            if line.startswith("Date:"):
                datetime_obj = datetime.strptime(
                    line, "Date: %Y-%m-%d %H:%M:%S")
                current_share["shared_at"] = datetime_obj.strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Shared Content:"):
                current_share["shared_content"] = line.split("Shared Content:", 1)[-1].strip()
            elif line.startswith("Link:"):
                current_share["id"] = line.split("/")[-2].strip()
            elif line.startswith("Method:"):
                current_share["method"] = line.split("Method:", 1)[-1].strip()
            elif line == "":
                # Finishes one complete Share Object
                if "id" in current_share and "shared_at" in current_share:
                    final_list.append(current_share.copy())
                    check_limit = datetime.strptime(current_share["shared_at"],
                                                    "%Y-%m-%d %H:%M:%S")
                    if limit_in_days is not None and (ref_month - check_limit).days > limit_in_days:
                        break
                    current_share.clear()
        shares_df = pd.DataFrame(columns=["id", "shared_content", "method", "shared_at"], data=final_list)
        # print(shares_df)
        dataframe_dict['shares'] = shares_df
    else:
        raise FileNotFoundError("Shares File Error - This should not happen.")
    return "Parsed Shares"
