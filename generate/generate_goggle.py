import os
import sqlite3
import tldextract
from collections import defaultdict
from datetime import timezone, datetime

# Environment variables
APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT")
GOGGLE_NAME = os.environ.get('GOGGLE_NAME')
GOGGLE_DESCRIPTION = os.environ.get('GOGGLE_DESCRIPTION')
GOGGLE_PUBLIC = os.environ.get('GOGGLE_PUBLIC')
GOGGLE_AUTHOR = os.environ.get('GOGGLE_AUTHOR')
GOGGLE_AVATAR = os.environ.get('GOGGLE_AVATAR')
GOGGLE_HOMEPAGE = os.environ.get('GOGGLE_HOMEPAGE')
GOGGLE_EXTRAS = os.environ.get('GOGGLE_EXTRAS')
GOGGLE_FILENAME = os.environ.get('GOGGLE_FILENAME')
SUBREDDITS = os.environ.get('SUBREDDITS').split(',')
SCORE_THRESHOLD = int(os.environ.get('SCORE_THRESHOLD'))
MIN_EPOCH_TIME = int(os.environ.get('MIN_EPOCH_TIME'))
MIN_FREQUENCY = int(os.environ.get('MIN_FREQUENCY'))
TOP_DOMAINS_BEHAVIOR = os.environ.get('TOP_DOMAINS_BEHAVIOR').lower()
TOP_DOMAINS_DOWNRANK_VALUE = int(os.environ.get('TOP_DOMAINS_DOWNRANK_VALUE'))


def dict_factory(cursor, row):
    """Return dicts for SQLite queries.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def header():
    """Generate the Goggle metadata.
    """
    return (
        f"! name: {GOGGLE_NAME}\n"
        f"! description: {GOGGLE_DESCRIPTION}\n"
        f"! public: {GOGGLE_PUBLIC}\n"
        f"! author: {GOGGLE_AUTHOR}\n"
        f"! avatar: {GOGGLE_AVATAR}\n"
        f"! homepage: {GOGGLE_HOMEPAGE}\n"
    )


def extras():
    """Generate any extras to include in the Goggle.
    """
    comment = "! Goggle extras\n"
    if GOGGLE_EXTRAS is not None:
        extras = GOGGLE_EXTRAS.replace("\\n", "\n")
        return comment + extras + '\n'
    else:
        return ""


def boost(domain, amt):
    """Boost a site by an integer amount.
    """
    return f'$boost={amt},site={domain}'


def downrank(domain, amt):
    """Downrank a site by an integer amount.
    """
    return f'$downrank={amt},site={domain}'


def discard(domain):
    """Discard a site."
    """
    return f'$discard,site={domain}'


def TOP_DOMAINS_BEHAVIOR():
    if TOP_DOMAINS_BEHAVIOR in ['exclude', 'discard', 'include', 'downrank']:
        return TOP_DOMAINS_BEHAVIOR


def sort_domains(submissions):
    """Parse URLs and return sorted list of domains with exclusions.
    """
    domains = defaultdict(lambda: 0)
    domains_counts = defaultdict(lambda: 0)
    for item in submissions:
        score = item['score']
        url = item['url']
        if url is None:
            pass
        else:
            extracted = tldextract.extract(url)

        # Double check that we have a real domain
        if extracted[1] and extracted[2]:
            domain = '.'.join(extracted[1:]).lower()
            # Check if we want to include domains from the top domains list
            if TOP_DOMAINS_BEHAVIOR() != "include":
                if domain not in TOP_DOMAINS:
                    domains[domain] += score
                    domains_counts[domain] += 1
            else:
                domains[domain] += score
                domains_counts[domain] += 1

    # Remove domains that don't meet the frequency requirements
    for item in domains_counts:
        count = domains_counts[item]
        if count < MIN_FREQUENCY:
            domains.pop(item)

    # Sort domains by score
    sorted_domains = sorted(
        domains.items(), key=lambda item: item[1], reverse=True)
    return sorted_domains


def generate(domains):
    """Generate rankings in Goggle format.
    """
    with open(f'{APPLICATION_ROOT}/data/{GOGGLE_FILENAME}', 'w') as target:
        target.write(header())
        target.write(f"! generated: {datetime.now(timezone.utc)}\n")
        target.write('\n')
        target.write(extras())

        entries = len(domains)

        if TOP_DOMAINS_BEHAVIOR() == "discard":
            for domain in TOP_DOMAINS:
                target.write('\n')
                target.write(discard(domain))

        if TOP_DOMAINS_BEHAVIOR() == "downrank":
            for domain in TOP_DOMAINS:
                target.write('\n')
                target.write(downrank(domain, TOP_DOMAINS_DOWNRANK_VALUE))

        # Split up the list into thirds and assign a boost of 4, 3, or 2
        for item in range(len(domains)):
            domain = domains[item][0]
            place = item/entries
            if place <= 0.33:
                target.write('\n')
                target.write(boost(domain, 4))
            elif place <= 0.66:
                target.write('\n')
                target.write(boost(domain, 3))
            else:
                target.write('\n')
                target.write(boost(domain, 2))
    print(f'{GOGGLE_FILENAME} generated')


# Store top domains in memory
with open(f'{APPLICATION_ROOT}/generate/top_domains.txt', 'r') as top_domains_file:
    TOP_DOMAINS = top_domains_file.read().splitlines()

# Get data from SQLite database
submissions = []
for item in SUBREDDITS:
    if len(item) > 0:
        target_subreddit = item.lower()
        con = sqlite3.connect(
            f'{APPLICATION_ROOT}/data/subreddits/{target_subreddit}/{target_subreddit}.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(
            'SELECT score,url FROM submissions WHERE score >= ? AND created >= ?', (SCORE_THRESHOLD, MIN_EPOCH_TIME))
        submissions.extend(cur.fetchall())
        con.close()

# Sort domains and generate Goggle
sorted_domains = sort_domains(submissions)
generate(sorted_domains)
