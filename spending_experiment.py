#
# spending_experiment.py
#   - See how well correlated spending is with Glicko-2 score.
#

import pandas as pd
import numpy as np
from utils import append_glicko
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

def main():
    """
    Main entry point.
    """
    spending2017 = {  # NCAAB spending for 2016-17 season by top-ten Glicko-2 team ID.
        1242: 11126047,  # Kansas
        1437: 11120378,  # Villanova
        1246: 19180059,  # Kentucky
        1112: 9852596,   # Arizona
        1314: 21408475,  # North Carolina
        1211: 8874752,   # Gonzaga
        1181: 19507686,  # Duke
        1332: 9229004,   # Oregon
        1257: 17065364,  # Louisville
        1438: 8555125    # Virgina
    }

    df, glicko_dict = append_glicko(pd.read_csv('./data/RegularSeasonCompactResults.csv'))
    teams = pd.read_csv('./data/Teams.csv')
    top_ten = sorted(glicko_dict.items(), key=lambda x: x[1].getRating(), reverse=True)[:10]
    top_ten_ids, top_ten_glicko = [i[0] for i in top_ten], [i[1].getRating() for i in top_ten]
    ordered_spending = [spending2017[tid] for tid in top_ten_ids]

    print("Corrcoef for spending and glicko: {}".format(pearsonr(ordered_spending, top_ten_glicko)))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for tid, glicko, spending in zip(top_ten_ids, top_ten_glicko, ordered_spending):
        ax.scatter(spending, glicko, c='b')
        ax.annotate(str(teams.loc[teams.TeamID == tid].TeamName.values[0]),
                    xy=(spending, glicko),
                    xytext=(spending + 1e-5 * spending, glicko + 1e-3 * glicko))

    z = np.polyfit(ordered_spending, top_ten_glicko, 1)
    p = np.poly1d(z)
    plt.plot(ordered_spending, p(ordered_spending))
    plt.ylabel("Glicko-2 Rating")
    plt.xlabel("Men's 2017 Basketball Expenses")
    plt.savefig("./plots/glickos_by_spending.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
