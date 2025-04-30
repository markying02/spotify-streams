import pandas as pd

#download from here: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023/data

# Read your CSV (specify encoding if needed)
df = pd.read_csv('spotify-2023.csv', encoding='latin-1')

# delete Love Grows (Where My Rosemary Goes) since streams not listed
df = df[df['track_name'] != 'Love Grows (Where My Rosemary Goes)']

# delete Jhoome Jo Pathaan and Que Vuelvas since they're outliers for streams
df = df[df['track_name'] != 'Jhoome Jo Pathaan']
df = df[df['track_name'] != 'Que Vuelvas']

# Delete non-spotify columns
df.drop(columns=['in_apple_playlists', 'in_apple_charts', 'in_deezer_playlists', 'in_deezer_charts', 'in_shazam_charts'], inplace=True)

# Delete key since the data is not good
df.drop(columns=['key'], inplace=True)

# Rename to standard 'year','month','day'
df_renamed = df.rename(
    columns={
        'released_year': 'year',
        'released_month': 'month',
        'released_day': 'day'
    }
)
# Create the new 'released_date' column
df['released_date'] = pd.to_datetime(df_renamed[['year','month','day']])

# Calculate day difference
ref_date = pd.to_datetime('2024-04-09')
df['days_released'] = (ref_date - df['released_date']).dt.days

# delete: 'released_year', 'released_month', 'released_day'
df.drop(columns=['released_date', 'released_year', 'released_month', 'released_day'], inplace=True)

# map mode to dummy variable
df['is_minor'] = df['mode'].map({'Minor': 1, 'Major': 0})

# delete: 'mode'
df.drop(columns=['mode'], inplace=True)

# divide danceability_%	valence_%	energy_%	acousticness_%	instrumentalness_%	liveness_%	speechiness_% all by 100
df['danceability'] = df['danceability_%'] / 100
df['valence'] = df['valence_%'] / 100
df['energy'] = df['energy_%'] / 100
df['acousticness'] = df['acousticness_%'] / 100
df['instrumentalness'] = df['instrumentalness_%'] / 100
df['liveness'] = df['liveness_%'] / 100
df['speechiness'] = df['speechiness_%'] / 100

# delete: 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'
df.drop(columns=['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'], inplace=True)

# rename in_spotify_playlists to num_playlists
df.rename(columns={'in_spotify_playlists': 'num_playlists'}, inplace=True)

# rename in_spotify_charts to chart_position
df.rename(columns={'in_spotify_charts': 'chart_rank'}, inplace=True)

# rename artist(s)_name to artist_name
df.rename(columns={'artist(s)_name': 'artist_name'}, inplace=True)

# # dummy variable for if a song is ranked
df['is_ranked'] = df['chart_rank'].apply(lambda x: 1 if x > 0 else 0)

# get max of chart_position as max_chart_position
max_chart_position = df['chart_rank'].max()

# create inverse chart_position column. keep 0 as 0
df['inverse_rank'] = df['chart_rank'].apply(lambda x: 0 if x == 0 else 1/x)

# Identify rows that have at least one missing value
rows_with_missing = df[df.isnull().any(axis=1)]

print("Rows with missing values:")
# Print the number of rows with missing values
print(f"Number of rows with missing values: {len(rows_with_missing)}")

# Print them (or you could export to a file, etc.)
# print(rows_with_missing)

# sort sheet by streams from greatest to least
# Convert 'streams' to numeric, forcing errors to NaN
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
# Drop rows where 'streams' is NaN
df.dropna(subset=['streams'], inplace=True)
# Sort the DataFrame by 'streams' in descending order
df.sort_values(by='streams', ascending=False, inplace=True)

# organization
df = df[['track_name', 'artist_name', 'artist_count', 'streams', 'days_released', 'is_ranked', 'chart_rank', 'inverse_rank', 'num_playlists', 'is_minor', 'bpm', 'danceability', 'valence', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']]

print("Sorted DataFrame:")
# Print the sorted DataFrame
print(df.head(10))  # Print top 10 rows

df.to_csv('output.csv', index=False)
