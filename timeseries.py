import pandas as pd
from datetime import timedelta

HOTSPOT_AMOUNT = 50


def find_hotspots(df: pd.DataFrame):
    # Switch to datetime fields
    df['viewed_at'] = pd.to_datetime(df['viewed_at'])

    # Find view sessions
    df['time_diff'] = df['viewed_at'] - df['viewed_at'].shift(-1)
    df['new_session'] = ((df['time_diff'].isna()) | (
        df['time_diff'] > pd.Timedelta(minutes=15))).astype(int)
    df['session_id'] = df['new_session'][::-1].cumsum()
    df = df.drop(columns=['time_diff', 'new_session'])

    # Find hotspots
    sessions = df.groupby('session_id')['viewed_at'].agg(['min', 'max'])
    sessions['session_length'] = sessions['max'] - sessions['min']
    avg_len = sessions['session_length'].mean()
    print(f"total sessions: {sessions.shape[0]}")
    print(f"average session time: {avg_len}")

    top_50 = sessions.sort_values(
        by='session_length', ascending=False).head(50)
    video_counts = df.groupby('session_id').size()
    top_50 = top_50.merge(video_counts.rename(
        'num_videos'), left_index=True, right_index=True)
    print(top_50[['min', 'num_videos', 'session_length']])


if __name__ == '__main__':
    df = pd.read_csv("tmp.csv")
    find_hotspots(df)
