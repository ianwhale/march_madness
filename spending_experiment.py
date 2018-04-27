#
# spending_experiment.py
#   - See how well correlated spending is with Glicko-2 score.
#

import pandas as pd
import numpy as np
from utils import append_glicko
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.lines import Line2D


def main():
    """
    Main entry point.
    """
    spending2017 = {     # NCAAB spending for 2016-17 season by top-ten Glicko-2 team ID.
        1242: 11126047,  # Kansas
        1437: 11120378,  # Villanova
        1246: 19180059,  # Kentucky
        1112: 9852596,   # Arizona
        1314: 21408475,  # North Carolina
        1211: 8874752,   # Gonzaga
        1181: 19507686,  # Duke
        1332: 9229004,   # Oregon
        1257: 17065364,  # Louisville
        1438: 8555125,   # Virgina
        1452: 9453611,   # West Virginia
        1124: 9097264,   # Baylor
        1374: 7269481,   # Southern Methodist
        1345: 8099562,   # Purdue
        1323: 6793853,   # Notre Dame
        1235: 6858775,   # Iowa State
        1458: 9564602,   # Wisconsin
        1455: 6380482,   # Wichita State
        1417: 9856861,   # UCLA
        1274: 7547589,   # Miami FL
        1268: 7442558,   # Maryland
        1153: 6970262,   # Cincinnati
        1139: 5489704,   # Butler
        1276: 16913194,  # Michigan
        1277: 10975215,  # Michigan State
    }

    N = 25
    remove_outliers = True
    spendings = list(spending2017.values())

    if remove_outliers:
        # Calculate the Tukey fences.
        k = 1.5
        q1, q3 = np.percentile(spendings, [25, 75])
        iqr = q3 - q1
        outlier_lb = q1 - k * iqr
        outlier_up = q3 + k * iqr

    assert N == len(spending2017)

    df, glicko_dict = append_glicko(pd.read_csv('./data/RegularSeasonCompactResults.csv'))
    top_N = sorted(glicko_dict.items(), key=lambda x: x[1].getRating(), reverse=True)[:N]
    top_N_ids, top_N_glicko = [i[0] for i in top_N], [i[1].getRating() for i in top_N]
    ordered_spending = [spending2017[tid] for tid in top_N_ids]

    if remove_outliers:
        inlier_spending, inlier_glicko, inlier_ids = [], [], []
        for tid, glicko, spending in zip(top_N_ids, top_N_glicko, ordered_spending):
            if outlier_lb < spending < outlier_up:
                inlier_spending.append(spending)
                inlier_glicko.append(glicko)
                inlier_ids.append(tid)

        top_N_ids = inlier_ids
        top_N_glicko = inlier_glicko
        ordered_spending = inlier_spending

    r_val = pearsonr(ordered_spending, top_N_glicko)
    print("Corrcoef for spending and glicko: {}".format(r_val))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for tid, glicko, spending in zip(top_N_ids, top_N_glicko, ordered_spending):
        ax.scatter(spending, glicko, c='b')

    z = np.polyfit(ordered_spending, top_N_glicko, 1)
    p = np.poly1d(z)
    plt.plot(ordered_spending, p(ordered_spending))
    plt.ylabel("Glicko-2 Rating")
    plt.xlabel("Men's 2016-17 Basketball Expenses")
    plt.legend(
        [Line2D([0], [0], color='b', lw=3)], ["r = {}".format(round(r_val[0], 4))]
    )
    f_name = "glickos_by_spending.png" if not remove_outliers else "glickos_by_spending_no_outliers.png"
    f_name = "./plots/" + f_name
    plt.savefig(f_name, dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
