#
# rd_experiment.py
#   - Glicko rating deviation experiment.
#   - Used to find out behavior of rating deviation with more seasons used in the past.
#   - Note: conference tournaments only have data since 2001.
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from glicko2.glicko2 import Player, glicko_rounds


def main():
    """
    Main entry point.
    """
    end_year = 2017  # We are predicting the results of the 2017 tournament.

    reg = pd.read_csv('./data/RegularSeasonCompactResults.csv')
    ncaa_tourney = pd.read_csv('./data/NCAATourneyCompactResults.csv')
    start_years = range(1985, end_year + 1)
    plot_years = [end_year, end_year - 1, end_year - 5, end_year - 10, 1985]

    glickos = {}
    accuracies = {}  # Accuracy on the "end_year" NCAA tournament
    for start_year in start_years:
        reg_s = reg.loc[reg.Season > start_year - 1]
        ncaa_test = ncaa_tourney.loc[ncaa_tourney.Season == end_year]

        team_ids = set(reg_s.WTeamID).union(set(reg_s.LTeamID))
        glicko = {team_id: Player() for team_id in team_ids}

        glicko_rounds(glicko, [], reg_s)  # Update glickos on regular season data (includes conference tournament).

        predictions = []
        glicko_rounds(glicko, predictions, ncaa_test)  # Test the predictive quality of glicko training.

        glickos[start_year] = glicko
        accuracies[start_year] = sum(predictions) / len(predictions)

    means = {}      # Mean of ratings.
    stdevs = {}     # Mean of standard deviations.
    for start_year, glicko in glickos.items():
        rds = [team.getRd() for team in glicko.values()]
        ratings = [team.getRating() for team in glicko.values()]
        means[start_year] = np.mean(ratings)
        stdevs[start_year] = np.sqrt(np.mean(np.square(rds)))  # Average the variances, sqrt, then take mean.

    # Sort plotting by start_year, ascending.
    for_plot = [i for i in sorted(zip(means.items(), stdevs.items()), key=lambda x: x[0][0], reverse=True)
                if i[0][0] in plot_years]
    for (start_year, mean), (_, stdev) in for_plot:
        space = np.linspace(mean - 3 * stdev, mean + 3 * stdev, 100)
        plt.plot(space, mlab.normpdf(space, mean, stdev), label=start_year)

    plt.legend()
    plt.xlabel("Glicko2 Mean Rating")
    plt.ylabel("Density")
    plt.savefig("./plots/glicko_distributions.png", dpi=300)
    plt.show()

    accuracies = sorted(accuracies.items(), key=lambda x: x[0])
    plt.plot([pair[0] for pair in accuracies], [pair[1] for pair in accuracies])
    plt.xlabel("Start Year")
    plt.ylabel("Glicko-2 2017 Tournament Prediction Accuracy")
    plt.savefig("./plots/glicko_accuracies_by_start_year.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
