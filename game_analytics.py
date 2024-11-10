import pandas as pd


def analyze_player(name, fn):
    df = pd.read_csv(fn)

    # Convert only the 'Event' column to lowercase
    df['Event'] = df['Event'].str.lower()

    # Filter rows where the 'Date' column starts with "2024"
    df_2024 = df[df['Date'].str.startswith('2024')]

    # Define the keywords to filter out
    excluded_events = ['rapid', 'freestyle', 'armageddon', 'blitz', 'bullet', "bl"]
    #excluded_events = ['rapid', 'freestyle', 'armageddon', 'blitz', 'bullet']

    # Filter out rows where any of the excluded events are mentioned in the 'Event' column
    mask = df_2024['Event'].str.contains('|'.join(excluded_events), na=False)
    df = df_2024[~mask]

     # Filter games where Ding Liren is the White player and the black player is 2700-2800
    #player_white = df[df['White'] == name]
    player_white = df[df['White'].str.contains(name, case=False, na=False)]
    player_white = player_white[(player_white['BlackElo'] >= 2700) & (player_white['BlackElo'] < 2800)]
    player_white_wins = player_white[player_white['Result'] == '1-0']
    #print("Ding white wins", ding_white_wins)

    player_white_losses = player_white[player_white['Result'] == '0-1']
    #print("Ding white losses", ding_white_losses)

    # Filter games where Ding Liren is the Black player and the white player is 2700-2800
    #player_black = df[df['Black'] == name]
    player_black = df[df['Black'].str.contains(name, case=False, na=False)]
    player_black = player_black[(player_black['WhiteElo'] >= 2700) & (player_black['WhiteElo'] < 2800)]
    player_black_wins = player_black[player_black['Result'] == '0-1']
    #print("black wins", player_black_wins["White"])

    player_black_losses = player_black[player_black['Result'] == '1-0']
    #print("Ding black losses", ding_black_losses)

    # Filters drawn games against 2700-2800 players
    player_black_draws = player_black[player_black['Result'] == '1/2-1/2']
    #print("Ding black draws", ding_black_draws)

    player_white_draws = player_white[player_white['Result'] == '1/2-1/2']
    #print("Ding white draws", ding_white_draws)

    # Ding had one win against a 2700, playing black in the Giuocco Pianissimo, and it happened to be against Gukesh
    # Print numbers
    print("wins as white:", len(player_white_wins))
    print("wins as black:", len(player_black_wins))
    print("losses as white:", len(player_white_losses))
    print("losses as black:", len(player_black_losses))
    print("draws as white:", len(player_white_draws))
    print("draws as black:", len(player_black_draws))
    average_white_score = (len(player_white_wins) + len(player_white_draws) * 0.5) / (len(player_white_wins) + len(player_white_losses) + len(player_white_draws))
    print("Average Score as White", average_white_score)
    average_black_score = (len(player_black_wins) + len(player_black_draws) * 0.5) / (len(player_black_wins) + len(player_black_losses) + len(player_black_draws))
    print("Average Score as Black", average_black_score)

    print("White score out of 7:", average_white_score * 7)
    print("Black score out of 7:", average_black_score * 7)

    return len(player_white_wins), len(player_black_wins), len(player_white_losses), len(player_black_losses), len(player_white_draws), len(player_black_draws)


def main():
    # Read the CSV file
    fn = "data/processed_games/OMOTB_ding202410.csv"

    print("Ding Liren Analysis")
    analyze_player("Ding Liren", fn)

    print("Gukesh Dommaraju Analysis")
    #analyze_player(df_2024_filtered, "Gukesh, D.")
    analyze_player("Gukesh", "data/processed_games/OMOTB_gukesh202410.csv")

    # 7.5 games needed to win the match
    print("Number of expected games", round(7.5 / (7.7/(7.7+4.8))))
    print("Gukesh score", 12 * (7.7/(7.7+4.8)))
    # Ding Liren wins as white: 0
    # Ding Liren losses as white: 4
    # Ding Liren draws as white: 17

    # 8.5 points out of 21 games as white

    # Ding Liren wins as black: 1
    # Ding Liren losses as black: 10
    # Ding Liren draws as black: 10

    # 6 points out of 21 games as black

    # 14.5 points out of 42 games total
    # 34.5% win rate
    # Out of 14 games, Ding is expected to win around 5 games

if __name__ == "__main__":
    main()
