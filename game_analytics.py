import pandas as pd

# Read the CSV file
fn = "data/processed_games/OMOTB_ding202410.csv"
df = pd.read_csv(fn)

# Convert only the 'Event' column to lowercase
df['Event'] = df['Event'].str.lower()

# Filter rows where the 'Date' column starts with "2024"
df_2024 = df[df['Date'].str.startswith('2024')]

# Define the keywords to filter out
excluded_events = ['rapid', 'freestyle', 'armageddon', 'blitz', 'bullet', "bl"]

# Filter out rows where any of the excluded events are mentioned in the 'Event' column
mask = df_2024['Event'].str.contains('|'.join(excluded_events), na=False)
df_2024_filtered = df_2024[~mask]

# Filter games where either WhiteElo or BlackElo is in the 2700s
df_2024_filtered = df_2024_filtered[((df_2024_filtered['WhiteElo'] >= 2700) & (df_2024_filtered['WhiteElo'] < 2800)) |
                            ((df_2024_filtered['BlackElo'] >= 2700) & (df_2024_filtered['BlackElo'] < 2800))]

# Filter games where Ding Liren is the White player and the black player is 2700-2800
ding_white = df_2024_filtered[df_2024_filtered['White'] == 'Ding Liren']
ding_white = ding_white[(ding_white['BlackElo'] >= 2700) & (ding_white['BlackElo'] < 2800)]
ding_white_wins = ding_white[ding_white['Result'] == '1-0']
print("Ding white wins", ding_white_wins)

ding_white_losses = ding_white[ding_white['Result'] == '0-1']
print("Ding white losses", ding_white_losses)

# Filter games where Ding Liren is the Black player and the white player is 2700-2800
ding_black = df_2024_filtered[df_2024_filtered['Black'] == 'Ding Liren']
ding_black = ding_black[(ding_black['WhiteElo'] >= 2700) & (ding_black['WhiteElo'] < 2800)]
ding_black_wins = ding_black[ding_black['Result'] == '0-1']
print("Ding black wins", ding_black_wins)

ding_black_losses = ding_black[ding_black['Result'] == '1-0']
print("Ding black losses", ding_black_losses)

# Filters drawn games against 2700-2800 players
ding_black_draws = ding_black[ding_black['Result'] == '1/2-1/2']
print("Ding black draws", ding_black_draws)

ding_white_draws = ding_white[ding_white['Result'] == '1/2-1/2']
print("Ding white draws", ding_white_draws)

# Ding had one win against a 2700, playing black in the Giuocco Pianissimo, and it happened to be against Gukesh
# Print numbers
print("Ding Liren wins as white:", len(ding_white_wins))
print("Ding Liren wins as black:", len(ding_black_wins))
print("Ding Liren losses as white:", len(ding_white_losses))
print("Ding Liren losses as black:", len(ding_black_losses))
print("Ding Liren draws as white:", len(ding_white_draws))
print("Ding Liren draws as black:", len(ding_black_draws))

# Ding Liren wins as white: 0
# Ding Liren losses as white: 4
# Ding Liren draws as white: 17

# Ding Liren wins as black: 1
# Ding Liren losses as black: 10
# Ding Liren draws as black: 10