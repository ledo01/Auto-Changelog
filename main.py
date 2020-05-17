import os
from subprocess import Popen, PIPE
from datetime import date
from collections import defaultdict

from pprint import pprint


def get_commits():
    # Run cmd
    p = Popen(['git', 'log', '--format=%B%H----DELIMITER----'], stdout=PIPE)
    stdout, stderr = p.communicate()

    # Split output and filter.
    outputs = filter(None, (stdout.decode()).split('----DELIMITER----\n'))
    commits = [{'sha': sha, 'message': msg}
               for msg, sha in map(lambda x: x.split('\n'), outputs)]

    commits_dict = defaultdict(list)

    for commit in commits:
        category, message = commit['message'].split(':', 1)
        commits_dict[category.title()].append(message.strip())

    return commits_dict


if __name__ == "__main__":
    current_date = date.today().isoformat()
    changelog = f"# {current_date}\n\n"

    commits = get_commits()
    for category, messages in commits.items():
        changelog += f'## {category}\n'
        for message in messages:
            changelog += f'* {message}'

    if os.path.exists('changelog.md'):
        with open('changelog.md', 'r') as f:
            data = f.read()
        with open('changelog.md', 'w') as f:
            f.write(changelog + '\n\n' + data)
    else:
        with open('changelog.md', 'w') as f:
            f.write(changelog)
