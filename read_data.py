import re
import pickle
import chess
import chess.pgn
import time
import sys
import pandas as pd


def parse_game(game):
    """Parses game object to extract evaluations, clocks and positions."""
        
    # board = game.board()
    # moves = []
    # node = game
    # Take in the mainline, annotated pgn might have multiple variations
    # while node.variations:
    #     next_node = node.variation(0)
    #     move = next_node.move
    #     board.push(move)
    #     moves.append(move.uci())
    #     node = next_node

    # Last name, First name
    # Year.Month.Day

    return {
        "WhiteElo": game.headers.get("WhiteElo", None),
        "BlackElo": game.headers.get("BlackElo", None),
        "Result": game.headers.get("Result", None),
        "Date": game.headers.get("Date", None),
        "White": game.headers.get("White", None),
        "Black": game.headers.get("Black", None),
        "ECO": game.headers.get("ECO", None),
        "Event": game.headers.get("Event", None),
    }


def process_pgn_file(filename):
    """Processes each game in a PGN file."""
    with open(filename) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            game_info = parse_game(game)
            if game_info:
                yield game_info


def process_pgn_stream():
    """Processes each game from the PGN data read from stdin."""
    while True:
        game = chess.pgn.read_game(sys.stdin)
        #print(game)
        if game is None:
            break
        game_info = parse_game(game)
        #print(game_info)
        if game_info:
            yield game_info

def has_exact_match(name, keyword):
    # Use \b to denote word boundaries for exact matches
    #pattern = rf'\b{re.escape(keyword)}\b'
    #return "ding" in name and "liren" in name
    return "gukesh" in name
    #return re.search(pattern, name) is not None

#test = "liren, ding"

def main():
    year = sys.argv[1]
    month = sys.argv[2]
    file_path = f"data/OMOTB{year}{month}PGN.pgn"
    max_game_per_month = 100000000
    out_dir = "data/processed_games/"
    game_count = 0
    start = time.time()
    games_list = []
    out_file = "data/processed_games/OMOTB_ding" + year + month + ".csv"
    out_file = "data/processed_games/OMOTB_gukesh" + year + month + ".csv"
    for game_info in process_pgn_stream():
        #print(game_info)
        if game_count % 100000 == 0:
            print(game_count)
        if game_info == -1:
            print("error", game_count)
            continue
        filename = f"{out_dir}lichess_db_standard_rated_{year}-{month}_{game_count}.pkl"
        white_name = game_info["White"].lower()
        black_name = game_info["Black"].lower()
        #print(white_name)
        #print(white_name, black_name)
        #if has_exact_match(white_name, "liren, ding") or has_exact_match(black_name, "liren, ding"):
            #print(white_name, black_name)
            #print(game_info)
        games_list.append(game_info)
            # with open(filename, 'wb') as file:
            #    pickle.dump(game_info, file)
        game_count += 1
        if game_count >= max_game_per_month:
            print("Finished saving data")
            break
    #print("names", names)
    # Convert the games list to a DataFrame and save to CSV
    if games_list:
        df = pd.DataFrame(games_list)
        df.to_csv(out_file, index=False)
        print(f"Saved {len(games_list)} games to {out_file}")
    end = time.time()
    print(file_path)
    print("seconds: ", round(end - start))


if __name__ == "__main__":
    main()
