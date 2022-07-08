# narwhalizer

<p align="center">
  <img src="https://i.snap.as/YLH9XsMZ.jpeg" width="450"/>
</p>

Goggles are a way to alter the ranking in a search engine. Brave is behind this technology and you should [read more about it](https://github.com/brave/goggles-quickstart). This tool lets you generate Goggles using your favorite subreddit(s). Forces Unseen uses this to generate [netsec-goggle](https://github.com/forcesunseen/netsec-goggle).

## Basic Usage

1. Build the container locally using the following command.

```
docker build . -t narwhalizer
```

2. Create an `.env` file. Refer to `netsec.env` for what you will need in there. The [Environment Variables](#environment-variables) section has more details about what each variable does. For your first time you can try it out with the `netsec.env` file by just replacing the variables that say `REPLACE`. Refer to the [Reddit API Credentials](#reddit-api-credentials) section for obtaining credentials for Reddit.

3. Run the container using your `.env` file. The following command shows `netsec.env` being used.

```
docker run -it -v ${PWD}/data:/app/data --env-file netsec.env narwhalizer
```

The first run will take longer since timesearch will have to build a database for the subreddit first. Afterwards updates will be much quicker. After execution completes the `data` directory will contain the subreddit database and generated `output.goggle` file. Every time the container is run, timesearch will check for updates and the `output.goggle` file will be re-generated. If at any point you terminate the container or your computer crashes, timesearch will continue from where it left off in building the database.


## Reddit API Credentials

Timesearch requires Reddit API credentials and other identifiers. These steps only have to be completed one time.

1. Go to https://old.reddit.com/prefs/apps/
2. Create an application with the `script` type and the redirect URL set to `http://localhost:8081`.
3. Copy the application ID and secret that was generated. (The application ID is near the top, under the name of your application)
4. Run the following command to obtain a refresh token. Replace the variables with the application ID and secret generated in the previous step.

```
docker run -it -p 127.0.0.1:8081:8081 narwhalizer ./scripts/refresh.sh --app-id <replace> --app-secret <replace>
```

After this you should be able to fill out the `APP_ID`, `APP_SECRET`, and `APP_REFRESH` variables within your `.env` file.

*Note: The script requests the following scopes: `read` and `wikiread`*

## Environment Variables

Everything is controlled through environment variables. Reference `netsec.env` for a real example and/or use `template.env` if you want a more bare-bones starting point.

### Timesearch

`USERAGENT` should be set to a description of your API usage. In this case we just left it as `narwhalizer`.

`CONTACT_INFO` should be set to an email address or Reddit username.

See the [Reddit API Credentials](#reddit-api-credentials) section to obtain values for the `APP_ID`, `APP_SECRET`, and `APP_REFRESH` variables.

**Example:**
```
USERAGENT=narwhalizer
CONTACT_INFO=<REPLACE_WITH_EMAIL_OR_REDDIT_USERNAME>
APP_ID=<REPLACE>
APP_SECRET=<REPLACE>
APP_REFRESH=<REPLACE>
```

### Goggle Metadata

This ends up as metadata at the top of the Goggle. More details about these can be these parameters can be found [here](https://github.com/brave/goggles-quickstart/blob/main/getting-started.md#goggles-syntax).

**Example:**
```
GOGGLE_NAME=Netsec
GOGGLE_DESCRIPTION=Prioritizes domains popular with the information security community. Primarily uses submissions and scoring from /r/netsec.
GOGGLE_PUBLIC=true
GOGGLE_AUTHOR=Forces Unseen
GOGGLE_AVATAR=#01ebae
GOGGLE_HOMEPAGE=https://github.com/forcesunseen/netsec-goggle
```

### Goggle

`SUBREDDITS` takes a comma delimited list of subreddits.

`GOGGLE_FILENAME` sets the output filename of the Goggle.

`GOGGLES_EXTRAS` allows you to include additional instructions in the final Goggle. Use `\n` to separate each instruction.

**Example:**
```
SUBREDDITS=netsec
GOGGLE_FILENAME=netsec.goggle
GOGGLE_EXTRAS=$boost=2,site=github.io\n$boost=2,site=github.com\n$boost=2,site=stackoverflow.com\n/blog.$boost=2\n/blog/$boost=2\n/docs.$boost=2\n/docs/$boost=2\n/doc/$boost=2\n/Doc/$boost=2\n/manual/$boost=2
```

### Algorithm

`SCORE_THRESHOLD` takes an integer for the minimum score of a submission to be included.

`MIN_FREQUENCY` takes an integer for the minimum frequency of a domain to be included.

`MIN_EPOCH_TIME` takes an integer representing Unix time for the oldest date submission to be included. Even though older submissions will not be included in the generated Goggle, we decided to still include all submissions when building the database with timesearch.

`TOP_DOMAINS_BEHAVIOR` takes one of four options: `exclude`, `include`, `discard`, or `downrank`.

   * **exclude** - top domains will be removed from the list of subreddit submissions.
   * **include** - top domains will be left in the list of subreddit submissions.
   * **discard** - top domains will be removed from the list of subreddit submissions and will also be marked as discard within the Goggle.
   * **downrank** - top domains will be removed from the list of subreddit submissions and will also be downranked using `TOP_DOMAINS_DOWNRANK_VALUE` within the Goggle.

`TOP_DOMAINS_DOWNRANK_VALUE` takes an integer for the amount to downrank. This is only used when `TOP_DOMAINS_BEHAVIOR` is set to `downrank`.

**Example:**
```
SCORE_THRESHOLD=20
MIN_FREQUENCY=1
MIN_EPOCH_TIME=0
TOP_DOMAINS_BEHAVIOR=exclude
TOP_DOMAINS_DOWNRANK_VALUE=2
```

Don't worry too much if there are completely irrelevant domains within your list. It most likely won't have a big impact because the rules are applied to Brave's "expanded recall set", as explained below.

>The instructions defined in a Goggle are not applied to Brave Search’s entire index, but to what we call the “expanded recall set,” which in turn is a function of the query. The set of candidate URLs can be in the tens of thousands, which is often more than enough to observe a noticeable effect; however, there are no guarantees that all possible URLs are surfaced (in search terminology, we have no guarantees on recall).

>Goggles do not apply to the whole Brave Search index, but to the expanded recall set which is a function of the input query. So if the target pages aren’t in the recall set, or even be in the Brave Search index, they won’t be captured by the Goggle.


## Development

The most common modifications can just be made through environment variables, but if you want you want to modify the `generate/generate_goggle.py` script you can mount the `generate` directory and run the container using the modified script. This can be done using the following command.

```
docker run -it -v ${PWD}/data:/app/data -v ${PWD}/generate:/app/generate --env-file netsec.env narwhalizer
```

### Make

Here are some make commands for you lazy ones.

```
make build
make run env=netsec.env
make dev env=netsec.env
```

## Thank You!

We owe it to [Ethan Dalool](https://github.com/voussoir) for creating [timesearch](https://github.com/voussoir/timesearch) and [Jason Baumgartner](https://github.com/pushshift) for creating [pushshift.io](https://pushshift.io/). Also, without Brave this project wouldn't even exist.

Thank you so much!