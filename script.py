from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


# Setting up pandas so that it displays all columns instead of collapsing them
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

video_play = pd.read_csv("video_play.csv")
# print(video_play.head())
# fill empty country fields with "NaN" so that it will be counted/grouped further on !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
video_play.country.fillna(value="NaN", inplace=True)
# Add unique id column for counting as all other columns contain duplicates!!!!
video_play["id"] = range(len(video_play.time))


# Get top 10 most viewed games------------------------------------------------------------------------------------------
games = video_play\
                    .groupby("game")\
                    .id\
                    .count()\
                    .reset_index()\
                    .rename(columns={"id": "frequency"})
games_sorted = games\
                    .sort_values(by='frequency', ascending=False)\
                    .iloc[:10]\
                    .reset_index(drop=True)
# print(games_sorted)

# Get top 12 of LoL viewers by country
countries = video_play[video_play.game == "League of Legends"]\
                    .groupby("country")\
                    .id\
                    .count()\
                    .reset_index()\
                    .rename(columns={"id": "frequency"})
countries_sorted = countries\
                    .sort_values(by='frequency', ascending=False)\
                    .iloc[:11]\
                    .reset_index(drop=True)
# Add 'Other countries' to create a top 12. 12 being the aggregate of all other countries outside the top 11.
other_countries_freq = video_play.id.count()-sum(countries_sorted.frequency)
other_countries = pd.DataFrame([['Other Countries', other_countries_freq]], columns=['country', 'frequency'])
countries_sorted = pd.concat([countries_sorted, other_countries]).reset_index(drop=True)

# print(countries_sorted)

# Get total views per hour of the day---------------------------------------------------------------------------------
stripped = video_play\
                    .time\
                    .apply(lambda x: x.split(":")[0][-2:])\
                    .reset_index()
time_freq = stripped\
                    .groupby("time")\
                    .index\
                    .count()\
                    .reset_index()\
                    .rename(columns={"index": "frequency"})
print(time_freq)


# Barplot of top 10 games by viewer count---------------------------------------------------------------------------
ax = plt.subplot()
ax.set_xticks(range(len(games_sorted.game)))
ax.set_xticklabels(games_sorted.game)

plt.bar(range(len(games_sorted.game)), games_sorted.frequency)
plt.title("Viewers per game (top 10)")
plt.legend(["Twitch"])
plt.xlabel("games")
plt.xticks(rotation=75)
plt.ylabel("viewers")
plt.subplots_adjust(bottom=0.30)
plt.show()
plt.close('all')

# Pie charts of all LoL viewers by country ---------------------------------------------------------------------------
colors = ['lightskyblue', 'gold', 'lightcoral', 'gainsboro', 'royalblue', 'lightpink', 'darkseagreen', 'sienna',
          'khaki', 'gold', 'violet', 'yellowgreen']
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
explode2 = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
ax = plt.subplot(1, 2, 1)
plt.pie(countries_sorted.frequency,
        explode=explode,
        shadow=True,
        startangle=90,
        autopct='%1.0f%%',
        pctdistance=1.13,
        colors=colors,
        textprops={'fontsize': 7})
plt.title("League of Legends Viewers' Whereabouts")
plt.legend(countries_sorted.country)

ax = plt.subplot(1, 2, 2)
plt.pie(countries_sorted.frequency[:-1],
        explode=explode2,
        startangle=90,
        autopct='%1.0f%%',
        pctdistance=1.1,
        colors=colors,
        textprops={'fontsize': 9})
plt.title("League of Legends Viewers' Whereabouts w/o 'Other Countries'")

plt.show()
plt.close('all')

# Line chart showing peak hours --------------------------------------------------------------------------------------
y_upper = [i*1.15 for i in time_freq.frequency]
y_lower = [i*0.85 for i in time_freq.frequency]

plt.plot(time_freq.time, time_freq.frequency)
plt.fill_between(time_freq.time, y_upper, y_lower, alpha=0.2)
plt.title("Time Series")

plt.xlabel("Hour")
plt.ylabel("Viewers")

plt.show()
