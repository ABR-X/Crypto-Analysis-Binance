import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st



def multiline_pyplot(combined, selected_coins, ax = None):
    combined = combined.copy()
    print(combined)
    dates = mdates.date2num(combined.index.to_pydatetime())
    fig, ax = plt.subplots(figsize=(10, 6))

    for selected_coin in selected_coins:
        ax.plot(dates, combined[selected_coin], label=selected_coin)
        
    # set x-axis to display years only
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.yscale("log")
    plt.legend(loc="upper right")
    return fig, ax

def correlation(combined, ax = None):
    import seaborn as sns
    combined = combined.copy()
    combined = combined.pct_change().corr(method="pearson")
        # Set the color scheme
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(combined, annot=True, cmap=cmap, square=True, ax=ax)

    # Set the title and axis labels
    ax.set_title("Correlation Matrix", fontsize=16)
    ax.set_xlabel("Coins", fontsize=12)
    ax.set_ylabel("Coins", fontsize=12)

    # Increase the font size of the annotations
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        
    plt.xticks(fontsize=10, rotation=45)
    plt.yticks(fontsize=10, rotation=0)

    return fig, ax