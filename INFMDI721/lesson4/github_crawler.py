import requests
from bs4 import BeautifulSoup
from github import Github

ACCESS_TOKEN = 'a8f657dd208713df6db3e0a948caa089224479c4'

def get_soup_from_url(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    return soup


def get_top_github_contributors():
    url = 'https://gist.github.com/paulmillr/2657075'

    soup = get_soup_from_url(url)
    contributors = []

    table = soup.find('tbody')
    for row in table.find_all('tr'):
        if (row.find('th', {'scope': 'row'}) != None):
            contributors.append(row.find('a').text)

    return contributors


if __name__ == '__main__':
    # https://gist.github.com/paulmillr/2657075
    # connect to github
    g = Github(ACCESS_TOKEN)
    contributors = get_top_github_contributors()

    # initialize dictionnary
    avg_stars_per_user = {}

    # loop over top contributors
    for idx, c in enumerate(contributors):
        user = g.get_user(c)
        avg_stars_per_user[user.login] = 0.0

        print("{}:{}".format(idx, user.login))

        count = 0
        # loop over all repositories
        for r in user.get_repos():
            avg_stars_per_user[user.login] += r.stargazers_count
            count += 1

         # compute the average
        if count > 0:
            avg_stars_per_user[user.login] /= count

    sorted_avg = sorted(avg_stars_per_user.items(),
                        key=lambda kv: kv[1], 
                        reverse=True)

    with open('top256Contributors.txt', 'w') as file:
        for key, value in sorted_avg:
            file.write('{} : {:.3f}\n'.format(key, value))
