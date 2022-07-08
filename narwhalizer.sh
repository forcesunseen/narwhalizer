#!/usr/bin/env bash

# This is where we have everything set up in the container
export APPLICATION_ROOT=/app

# Get ready
source "$APPLICATION_ROOT"/venv/bin/activate
cd "$APPLICATION_ROOT"/data

# Update database for each subreddit using timesearch
IFS=',' read -ra TARGET_SUBREDDITS <<< "$SUBREDDITS"
for SUBREDDIT in "${TARGET_SUBREDDITS[@]}"; do
	echo "Running timesearch for subreddit: $SUBREDDIT"
	python "$APPLICATION_ROOT"/timesearch/timesearch.py get_submissions -r "$SUBREDDIT"
done

# Generate Goggle
python "$APPLICATION_ROOT"/generate/generate_goggle.py
