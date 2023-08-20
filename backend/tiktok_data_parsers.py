import pandas as pd
from datetime import datetime
from fastapi import UploadFile

# Dataframe fields
DATE_FIELD = "date"
ID_FIELD = "id"
COMMENT_FIELD = "comment"
SEARCH_FIELD = "search"
SHARE_TYPE_FIELD = "type"
METHOD_FIELD = "method"


async def parse_date_id(data: UploadFile, limit: int or None = None) -> pd.DataFrame:
    """
    Extracts date and video ID from txt file.
    Works for browsing history, liked, and favorites

    Args:
        data (UploadFile): File data
        limit (intorNone): (Optional) how much data, in days, to parse

    Returns:
        pd.DataFrame: DataFrame with columns "date" and "id"
    """
    content = await data.read()
    content = content.decode('UTF-8')
    lines = content.strip().split('\n')

    videos = []
    curr = {}
    for line in lines:
        line = line.strip()
        try:
            if line.startswith("Date:"):
                date_str = line[len("Date: "):]
                curr[DATE_FIELD] = datetime.strptime(
                    date_str, "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Link:"):
                curr[ID_FIELD] = _get_id(line)
            elif line == "" and DATE_FIELD in curr and ID_FIELD in curr:
                videos.append(curr.copy())
        except ValueError:
            print(f"Skipping malformatted line: {line}")
            curr.clear()
    return pd.DataFrame(videos)


async def parse_comments(data: UploadFile, limit: int | None = None) -> pd.DataFrame:
    """
    Extracts date and comment from txt file.
    Works for comment history only.

    Args:
        data (UploadFile): File data
        limit (int | None, optional): (Optional) how much data, in days, to parse

    Returns:
        pd.DataFrame: Dataframe with columns "date" and "comment"
    """
    content = await data.read()
    content = content.decode('UTF-8')
    lines = content.strip().split('\n')

    comments = []
    curr = {}
    for line in lines:
        line = line.strip()
        try:
            if line.startswith("Date:"):
                date_str = line[len("Date: "):]
                curr[DATE_FIELD] = datetime.strptime(
                    date_str, "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Comment:"):
                curr[COMMENT_FIELD] = line[len("Comment: "):]
            elif line == "" and DATE_FIELD in curr and COMMENT_FIELD in curr:
                comments.append(curr.copy())
        except ValueError:
            print(f"Skipping malformatted line: {line}")
            curr.clear()
    return pd.DataFrame(comments)


async def parse_searches(data: UploadFile, limit: int | None = None) -> pd.DataFrame:
    """
    Extracts date and searches from txt file.
    Works for search history only.

    Args:
        data (UploadFile): File data
        limit (int | None, optional): (Optional) how much data, in days, to parse

    Returns:
        pd.DataFrame: Dataframe with columns "date" and "search"
    """
    content = await data.read()
    content = content.decode('UTF-8')
    lines = content.strip().split('\n')

    searches = []
    curr = {}
    for line in lines:
        line = line.strip()
        try:
            if line.startswith("Date:"):
                date_str = line[len("Date: "):]
                curr[DATE_FIELD] = datetime.strptime(
                    date_str, "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Search Term:"):
                curr[SEARCH_FIELD] = line[len("Search Term: "):]
            elif line == "" and DATE_FIELD in curr and SEARCH_FIELD in curr:
                searches.append(curr.copy())
        except ValueError:
            print(f"Skipping malformatted line: {line}")
            curr.clear()
    return pd.DataFrame(searches)


async def parse_shares(data: UploadFile, limit: int | None = None) -> pd.DataFrame:
    """
    Extracts date, content type, id, and method from txt file.
    Works for share history only.

    Args:
        data (UploadFile): File data
        limit (int | None, optional): (Optional) how much data, in days, to parse

    Returns:
        pd.DataFrame: Dataframe with columns "date", "type", "id", and "method"
    """
    content = await data.read()
    content = content.decode('UTF-8')
    lines = content.strip().split('\n')

    shares = []
    curr = {}
    for line in lines:
        line = line.strip()
        try:
            if line.startswith("Date:"):
                date_str = line[len("Date: "):]
                curr[DATE_FIELD] = datetime.strptime(
                    date_str, "%Y-%m-%d %H:%M:%S")
            elif line.startswith("Shared Content:"):
                curr[SHARE_TYPE_FIELD] = line[len("Shared Content: "):]
            elif line.startswith("Link:"):
                curr[ID_FIELD] = _get_id(line)
            elif line.startswith("Method:"):
                curr[METHOD_FIELD] = line[len("Method: "):]
            elif line == "" and DATE_FIELD in curr and SHARE_TYPE_FIELD in curr and ID_FIELD in curr and METHOD_FIELD in curr:
                shares.append(curr.copy())
        except ValueError:
            print(f"Skipping malformatted line: {line}")
            curr.clear()
    return pd.DataFrame(shares)


def _get_id(line: str) -> str:
    return line.split("/")[-2].strip()
