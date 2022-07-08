#!/usr/bin/env bash

while [[ $# -gt 0 ]] && [[ "$1" == "--"* ]] ;
do
    opt="$1";
    shift;
    case "$opt" in
        "--" ) break 2;;
        "--app-id" )
           APP_ID="$1"; shift;;
        "--app-secret" )
           APP_SECRET="$1"; shift;;
        *) echo >&2 "Invalid option: $@"; exit 1;;
   esac
done

export praw_client_id=$APP_ID
export praw_client_secret=$APP_SECRET

source venv/bin/activate
./refresh/obtain_refresh_token.py