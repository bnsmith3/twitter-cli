# twitter-cli

A simple command line tool to grab tweets via the Twitter API

---

## Quick Start
Using twitter-cli is fairly straightforward. To see the command line arguments, issue the following command from the directory that contains `search.py`:
`python search.py --help`

When running `search.py`, the script takes 3 arguments, 2 of which are required:
* One of the following (required):
	* `-t` or `--term`: A term to search for on Twitter. This flag can be used multiple times.
	* `-tf` or `--terms_file`: The file that holds the terms to be search. Each line holds one term.
	* `-u` or `--user_id`: The user ID of a user whose tweets to retrieve.
	* `-s` or `--screen_name`: The username of a user whose tweets to retrieve.
* `-f` or `--tweets_file` (required): The pickle file to which to write the list of retrieved tweets.
* `-o` or `--or_terms`: Include this flag if multiple terms should be ORed. The default is that the terms will be ANDed.

To run without error, the `search.py` file is expecting a config file named `config.cfg` to be in the same directory that holds at least one section named "twitter" that contains four keys:
- consumer_key: the Twitter app consumer key (i.e., App Key)
- consumer_secret: the Twitter app consumer secret (i.e., App Secret)
- access_token: the Twitter app access token for user authentication
- access_token_secret: the Twitter app access token secret for user authentication
