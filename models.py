import json
from pathlib import Path

from pydantic import BaseModel


class PlayoffTeam(BaseModel):
    team_name: str
    seed: int
    season: int
    round_victories: int


def save_to_json(results, filename):
    with open(filename, 'w+') as f:
        json.dump([result.dict() for result in results], f, indent=4)


eastern_teams = [
    'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Bobcats', 'Charlotte Hornets', 'Chicago Bulls',
    'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Miami Heat', 'Milwaukee Bucks', 'New Jersey Nets',
    'New York Knicks', 'Orlando Magic', 'Philadelphia 76ers', 'Toronto Raptors', 'Washington Bullets',
    'Washington Wizards'
]
western_teams = [
    'Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors', 'Houston Rockets', 'Los Angeles Clippers',
    'Los Angeles Lakers', 'Memphis Grizzlies', 'Minnesota Timberwolves', 'New Orleans Hornets',
    'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings',
    'San Antonio Spurs', 'Seattle SuperSonics', 'Utah Jazz'
]


def load_playoff_teams(folder: str, year_greater_than: int = 1985, year_less_than: int = 2025,
                       conference: str = None) -> list[PlayoffTeam]:
    folder_path = Path(folder)
    all_teams = []

    for file in folder_path.glob('*.json'):  # Load all JSON files in the folder
        with open(file, 'r') as f:
            data = json.load(f)
            all_teams.extend(PlayoffTeam(**item) for item in data)

    results = [
        team for team in all_teams
        if year_greater_than <= team.season <= year_less_than
    ]
    # Apply conference filter if needed
    if conference == 'eastern':
        return [
            team for team in results
            if team.team_name in eastern_teams or (team.team_name == 'New Orleans Hornets' and team.season <= 2004)
        ]
    elif conference == 'western':
        return [
            team for team in results
            if team.team_name in western_teams and (team.team_name != 'New Orleans Hornets' or team.season >= 2005)
        ]
    else:
        return results
