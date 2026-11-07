# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import statistics


# EXTRA CREDIT: shows a number with st.metric and how much it changed
# name is the spot in session state where we remember the old number
def show_metric(label, value, name):
    # the first time, remember the number and say it hasn't changed yet
    if name not in st.session_state:
        st.session_state[name] = value
        st.session_state[name + "_change"] = 0

    # if the number is different from last time, save how much it changed
    if value != st.session_state[name]:
        st.session_state[name + "_change"] = value - st.session_state[name]
        st.session_state[name] = value

    change = st.session_state[name + "_change"]
    if change == 0:
        st.metric(label, f"{value:.1f}")
    else:
        st.metric(label, f"{value:.1f}", f"{change:.1f}")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
st.header("Part 1: Suits by the Numbers")

# open the json file and load it into a dictionary
with open("data.json") as file:
    data = json.load(file)

# go through each data point and put the info into lists
seasons = []
episodes = []
years = []
for point in data["data_points"]:
    seasons.append(point["label"])
    episodes.append(point["value"])
    years.append(point["year"])


# STATIC GRAPH: bar chart of episodes per season (does not change)
st.subheader(data["chart_title"])
st.write("How many episodes each season of Suits had.")

bar_data = pd.DataFrame({"Season": seasons, "Episodes": episodes})
st.bar_chart(bar_data, x="Season", y="Episodes", x_label="Season", y_label="Number of Episodes")


# DYNAMIC GRAPH: line chart that changes with the slider and radio
st.subheader("Explore the Seasons")
st.write("Pick a range of seasons and what you want to see.")

# set up session state the first time the page loads
if "season_range" not in st.session_state:
    st.session_state.season_range = (1, 9)
if "view" not in st.session_state:
    st.session_state.view = "Episodes per season"

# user inputs (the key saves the choice in session state)
st.slider("Seasons to show:", 1, 9, key="season_range")
st.radio("What do you want to see?", ["Episodes per season", "Total episodes so far"], key="view")

start = st.session_state.season_range[0]
end = st.session_state.season_range[1]

# only keep the seasons the user picked
picked_years = years[start - 1:end]
picked_episodes = episodes[start - 1:end]

# if they want the total, add up the episodes as we go
if st.session_state.view == "Total episodes so far":
    totals = []
    total = 0
    for count in picked_episodes:
        total = total + count
        totals.append(total)
    y_values = totals
    y_label = "Total Episodes"
else:
    y_values = picked_episodes
    y_label = "Episodes in Season"

# make the matplotlib line chart
fig, ax = plt.subplots()
ax.plot(picked_years, y_values, marker="o", color="black")
ax.set_title(f"Suits: {st.session_state.view} (Seasons {start}-{end})")
ax.set_xlabel("Year Aired")
ax.set_ylabel(y_label)
ax.set_xticks(picked_years)
st.pyplot(fig)

st.write(f"Seasons {start} to {end} had **{sum(picked_episodes)}** episodes total.")

# EXTRA CREDIT: mean and median of what the line chart is showing
# remember which view was picked last time
if "p1_last_view" not in st.session_state:
    st.session_state.p1_last_view = st.session_state.view

# if the user switched views, forget the old numbers so we don't compare
# "episodes per season" to "total episodes" (they measure different things)
if st.session_state.view != st.session_state.p1_last_view:
    del st.session_state["p1_mean"]
    del st.session_state["p1_median"]
    st.session_state.p1_last_view = st.session_state.view

col1, col2 = st.columns(2)
with col1:
    show_metric("Mean", statistics.mean(y_values), "p1_mean")
with col2:
    show_metric("Median", statistics.median(y_values), "p1_median")


# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Part 2: What Suits Fans Think")

# read the survey answers from data.csv into a table (DataFrame)
survey = pd.read_csv("data.csv")

# if nobody has taken the survey yet, don't try to make graphs
if len(survey) == 0:
    st.info("No survey answers yet! Go to the Survey page and add some.")
else:
    st.write(f"Based on **{len(survey)}** survey answers.")

    # count how many people picked each character
    counts = {}
    for name in survey["Category"]:
        if name in counts:
            counts[name] = counts[name] + 1
        else:
            counts[name] = 1


    # STATIC GRAPH: pie chart of favorite characters (does not change)
    st.subheader("Favorite Suits Characters")

    fig2, ax2 = plt.subplots()
    ax2.pie(counts.values(), labels=counts.keys(), autopct="%1.0f%%")
    ax2.set_title("Who Is Everyone's Favorite Character?")
    st.pyplot(fig2)


    # DYNAMIC GRAPH: bar chart of seasons watched, changes with the radio
    st.subheader("How Much Have Fans Watched?")
    st.write("Pick a character to only see the people who chose them.")

    # set up session state the first time the page loads
    if "fan_pick" not in st.session_state:
        st.session_state.fan_pick = "Everyone"

    # the choices are "Everyone" plus every character someone picked
    options = ["Everyone"]
    for name in counts:
        options.append(name)

    # user input (the key saves the choice in session state)
    st.radio("Show answers from:", options, key="fan_pick")

    # only keep the answers from the people the user picked
    picked_seasons = []
    for i in range(len(survey)):
        if st.session_state.fan_pick == "Everyone" or survey["Category"][i] == st.session_state.fan_pick:
            picked_seasons.append(int(survey["Value"][i]))

    # count how many people watched 0 seasons, 1 season, ... up to 9
    people = []
    for number in range(10):
        people.append(picked_seasons.count(number))

    seasons_data = pd.DataFrame({"Seasons Watched": list(range(10)), "People": people})
    st.bar_chart(seasons_data, x="Seasons Watched", y="People", x_label="Seasons Watched", y_label="Number of People")

    average = sum(picked_seasons) / len(picked_seasons)
    # change the sentence depending on who is picked
    if st.session_state.fan_pick == "Everyone":
        st.write(f"Everyone who took the survey watched **{average:.1f}** seasons on average.")
    else:
        st.write(f"**{st.session_state.fan_pick}** fans watched **{average:.1f}** seasons on average.")

    # EXTRA CREDIT: mean and median of the seasons watched for the picked fans
    col3, col4 = st.columns(2)
    with col3:
        show_metric("Mean Seasons Watched", statistics.mean(picked_seasons), "p2_mean")
    with col4:
        show_metric("Median Seasons Watched", statistics.median(picked_seasons), "p2_median")
