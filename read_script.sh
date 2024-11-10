#!/bin/bash

year="2024"

# From month 10 to 10 inclusive
for month in $(seq 10 10); do
    # Format the month with a leading zero
    formatted_month=$(printf "%02d" $month)

    #file_path="data/OMOTB${year}${formatted_month}PGN.pgn"
    file_path="data/dingliren.pgn"
    file_path="data/gukesh.pgn"
    echo "Processing file: $file_path"
    cat $file_path | python read_data.py $year $month
    if [ $? -eq 0 ]; then
        echo "Successfully processed $file_path"
    else
        echo "Failed to process $file_path" >&2
    fi
done
