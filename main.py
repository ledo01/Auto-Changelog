import os
from subprocess import Popen, PIPE
from datetime import date
from collections import defaultdict

from pprint import pprint

# Dict for settings the display name of the categories
# For example, features are tag with `feat:` in the commits
# but I want to display Features in the changelog.
# Also, any category not in this dict are ignored, in this way
# you can control the categories you want to display.
CATEGORIES = {
    'feat': 'Feature',
    'fix': 'Bug Fixes'
}


def get_commits(ver):
    # Run cmd
    p = Popen(['git', 'log', '--format=%B%H----DELIMITER----',
               f'{ver}..HEAD'], stdout=PIPE)
    stdout, _ = p.communicate()

    # Split output and filter.
    outputs = filter(None, (stdout.decode()).split('----DELIMITER----\n'))
    commits = [{'sha': sha, 'message': msg}
               for msg, sha in map(lambda x: x.split('\n'), outputs)]

    commits_dict = defaultdict(list)

    for commit in commits:
        category, message = commit['message'].split(':', 1)
        commits_dict[category].append(message.strip())

    return commits_dict


def get_current_version():
    p = Popen(['git', 'describe'], stdout=PIPE)
    stdout, _ = p.communicate()
    version = stdout.decode().split('-')[0]
    return version


if __name__ == "__main__":
    current_date = date.today().isoformat()
    current_version = get_current_version()
    changelog = f"# {current_version} ({current_date})\n\n"

    commits = get_commits(current_version)
    for category, messages in commits.items():
        if category in CATEGORIES:
            changelog += f'## {CATEGORIES[category]}\n\n'
            for message in messages:
                changelog += f'- {message}\n'
            changelog += '\n'

    if os.path.exists('changelog.md'):
        with open('changelog.md', 'r') as f:
            data = f.read()
        with open('changelog.md', 'w') as f:
            f.write(changelog + '\n\n' + data)
    else:
        with open('changelog.md', 'w') as f:
            f.write(changelog)
