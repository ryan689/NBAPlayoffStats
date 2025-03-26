import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from models import PlayoffTeam, save_to_json

BASE_URL = 'https://www.basketball-reference.com'
teams_url = BASE_URL + '/teams'


teams = [
    'BOS', 'NYK', 'TOR', 'BRK', 'PHI', 'CLE', 'IND', 'MIL', 'DET', 'CHI', 'ATL', 'ORL', 'MIA', 'CHO', 'WAS', 'OKC',
    'DEN', 'MIN', 'POR', 'UTA', 'LAL', 'GSW', 'LAC', 'SAC', 'PHO', 'HOU', 'MEM', 'DAL', 'SAS', 'NOP', 'NJN', 'WSB',
    'CHH', 'VAN', 'SEA', 'NOJ', 'NYN', 'BUF', 'KCK', 'CHA', 'NOH'
]

# seasons = reversed(list(range(1985, 2025)))
seasons = reversed(list(range(1985, 1998)))


def get_playoff_results(team: str, season: int):
    print(f'Finding results for {team} in {season}')
    result_url = teams_url + '/' + team + '/' + str(season) + '.html'
    response = requests.get(result_url)
    soup = BeautifulSoup(response.text, features='lxml')
    if soup.find('h1', string='Rate Limited Request (429 error)'):
        print('Too many requests')
        return

    if not (playoffs_text := soup.find('a', string=F'NBA {season} Playoffs')):
        return

    # find team name
    if not (roster_element := soup.find('span', string='Roster and Stats')):
        print('has no roster!')
        return
    team_name = roster_element.previous_sibling.previous_sibling.text

    # find round victories
    playoff_element = playoffs_text.parent.parent.parent
    round_victories = playoff_element.text.count('Won ')

    # find seed
    series_link = soup.find('a', string='Series Stats').attrs['href']
    response = requests.get(BASE_URL + series_link)
    soup = BeautifulSoup(response.text, features='lxml')
    seed_text = soup.find(id='content').find('a', string=team_name).previous_sibling.text
    if not (match := re.search(r'#(\d+)', seed_text)):
        print('could not find seed text')
        return
    seed = int(match.group(1))

    return PlayoffTeam(
        team_name=team_name,
        season=season,
        seed=seed,
        round_victories=round_victories
    )


def scrape_teams():
    folder = Path('playoff_teams')
    folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist
    results = []
    for season in seasons:
        season_results = []
        filename = folder / f'playoff_teams_{season}.json'
        for team in teams:
            if playoff_results := get_playoff_results(team, season):
                season_results.append(playoff_results)
            time.sleep(6)
        save_to_json(season_results, filename=filename)
        results.extend(season_results)
    return results


if __name__ == '__main__':
    data = scrape_teams()
