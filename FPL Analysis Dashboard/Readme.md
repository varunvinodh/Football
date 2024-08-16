# Fantasy Premier League (FPL) Dashboard

## Introduction

As a Fantasy Premier League (FPL) player, I encountered various challenges at the beginning of this season, such as selecting the best team based on player performance, cost-effectiveness, and overall value. In my quest for answers, I decided to analyze FPL data myself. This project aims to provide insights into player performance, cost-efficiency, and strategic recommendations to aid in optimal team selection. The dashboard I developed visualizes key metrics to assist in making informed decisions for your FPL team.

## Data Gathering

The dataset used for this analysis was obtained via an API call from the official FPL website (FPL API). This API provides live data on players, teams, and performance metrics. For reproducibility, a copy of the dataset used in this project is included in the repository.

## Data Preparation

The raw data was cleaned and pre-processed to extract relevant information, including player names, positions, costs, points, and various performance metrics.

## Dashboard Overview

The dashboard enables users to visualize and analyze FPL player data through various metrics and filters. It includes the following tabs:

1. **Top Performers**: Displays the top 10 players based on total points.
2. **Cost-Effective Players**: Shows players' total points versus their cost, highlighting cost-efficiency.
3. **Expected Goals vs Goals Scored**: Compares players' expected goals against the goals they actually scored.
4. **Points per 90 Minutes**: Visualizes the points scored per 90 minutes of play.
5. **Player Selection Percentage**: Displays the top players based on their selection percentage by other FPL managers.

## How to Run

To run the FPL Dashboard, follow these steps:

1. **Ensure Python and Dependencies are Installed**

   Make sure you have Python installed on your machine. You will also need to install the required Python libraries. You can install these libraries using pip. The required libraries are:
   - `pandas`
   - `dash`
   - `plotly`

2. **Prepare the Dataset**

   Ensure the dataset file (`Players_data_23-24.csv`) is placed in the same directory as the `FPL_Dashboard.py` file.

3. **Run the Dashboard**

   Use the provided `Run_FPL.bat` file to start the dashboard. This batch file will execute the Python script and launch the dashboard in your default web browser.

   - **Windows**: Double-click the `Run_FPL.bat` file. Alternatively, you can run the script manually by navigating to the directory containing `FPL_Dashboard.py` and executing the following command in Command Prompt 'python FPL_Dashboard.py'

4. **Interacting with the Dashboard**

   Once the dashboard is open in your browser, you can:
   - Use the dropdown menu to filter players by position.
   - Adjust the cost range slider to select the budget.
   - Set the minimum minutes played using the slider.
   - Navigate through different tabs to view various metrics such as top performers, cost-effective players, and more.

## Contact

For any questions or feedback, feel free to reach out at varunvinodh25@gmail.com or [LinkedIn](https://www.linkedin.com/in/varunvinodh/).

