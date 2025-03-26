import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from models import load_playoff_teams


def get_seed_success_rate(df: pd.DataFrame) -> pd.DataFrame:
    # Create an empty list to hold the data for the DataFrame
    data = []

    # For each seed, calculate the percentage of teams that advanced to each round
    for seed in df['seed'].unique():
        seed_data = df[df['seed'] == seed]

        # Calculate the total number of teams for that seed
        total_teams = len(seed_data)

        # Calculate the number of teams that advanced to each round
        # Round 1: advanced to the second round (round_victories >= 1)
        round_1 = (seed_data['round_victories'] >= 1).sum()

        # Round 2: advanced to the conference finals (round_victories >= 2)
        round_2 = (seed_data['round_victories'] >= 2).sum()

        # Round 3: advanced to the NBA finals (round_victories >= 3)
        round_3 = (seed_data['round_victories'] >= 3).sum()

        # Round 4: won the NBA finals (round_victories == 4)
        round_4 = (seed_data['round_victories'] == 4).sum()

        # Store the results in the list
        data.append({
            '1st Round': round_1 / total_teams,
            'Conference Semifinals': round_2 / total_teams,
            'Conference Finals': round_3 / total_teams,
            'NBA Finals': round_4 / total_teams,
        })

    # Convert the list of results into a DataFrame and set 'Seed' as the index
    result_df = pd.DataFrame(data, index=df['seed'].unique())

    # Optionally, sort the index to ensure seeds are ordered
    result_df = result_df.sort_index()

    return result_df


if __name__ == '__main__':
    data = load_playoff_teams('playoff_teams')

    df = pd.DataFrame([team.model_dump() for team in data])
    final_results = get_seed_success_rate(df)
    print(len(df))
    plt.figure(figsize=(10, 6))
    sns.heatmap(final_results * 100,
                annot=final_results.applymap(lambda x: f'{x*100:.1f}%'),
                cmap='coolwarm', fmt="", linewidths=0.5, cbar=False)

    plt.title(f'Chance to Advance to and Win Round by Seed\n\n{len(df)} Team-Seasons (1985-2024)')
    plt.xlabel('Round')
    plt.ylabel('Seed')

    plt.show()
