"""
Fri Nov 5 2021

DS 2000 and 2001 Final Project:
    Researching different questions relating to how certain stats
    relate to winning in the NBA

@author: Beckett Sanderson & Max Rizzuto
"""
"""
Project Description:
    We will examine how pace and age relate to each other and to winning
    percentages. For age and winning percentage specifically, we will create
    a bar graph for different age ranges as compared to the avg winning
    percentage of each age range. We would also like to compare winning 
    percentages with three-point attempts for all teams during a season in the 
    ‘70s, ‘90s, and the modern era to see if and how the league has evolved in 
    regards to 3 point shooting.
"""

import matplotlib.pyplot as plt
import numpy as np

PER_GAME_2018 = "2018-19 Per Game Data.txt"
PER_GAME_1999 = "1999-00 Per Game Data.txt"
PER_GAME_1979 = "1979-80 Per Game Data.txt"
ADVANCED_2018 = "2018-19 Advanced Data.txt"
ADVANCED_1999 = "1999-00 Advanced Data.txt"
ADVANCED_1979 = "1979-80 Advanced Data.txt"


def read_file(file_name):
    """
    Read in a file and return a 2d list of the data by row by spltting
    txt file on the commas

    Parameters
    ----------
    file_name : txt file containing data by team separated by commas

    Returns
    -------
    file_data : 2d list containing rows of data as input from file

    """    
    # initialize empty list variable
    file_data = []
   
    # open file we are reading in
    with open(file_name, 'r') as file:
       
        cur_line = file.readline()
       
        # loops through txt file until empty line at the end occurs
        while cur_line != "":
           
            # adds each row to file_data as a list split on commas
            file_data.append(cur_line.strip().split(","))
           
            # resets new line to check if need to exit while loop
            cur_line = file.readline()
   
    # removes header file that doesn't contain team data
    headers = file_data.pop(0)
   
    return file_data


def remove_asterisks(team_data):
    """
    Removes asterisks from the names of each of our datasets to allow
    them to be compared to each other more easily

    Parameters
    ----------
    team_data : 2d list
        list containing rows of data for NBA teams with the name of the
        team at index 1

    Returns
    -------
    None.

    """
    # loop through each team in the dataset
    for team in team_data:
       
        # initialize empty variables
        idx = 0
        temp_name = ""
       
        # loops through each character in the team name string
        for char in team[1]:
           
            # checks if character is an asterisk
            if char != "*":
           
                # adds character to name if not an asterisk
                temp_name += char
               
            idx += 1
       
        # sets team's name as itself without the asterisks
        team[1] = temp_name
               

def create_team_dict(team_data):
    """
    Create a dictionary that we can use to add data to or search up data
    from any NBA team

    Parameters
    ----------
    team_data : 2d list
        list containing rows of data for NBA teams with the name of the
        team at index 1

    Returns
    -------
    team_dict : dictionary
        a dictionary containing all the team's names and a corresponding
        empty data list

    """
    # initializes an empty dictionary
    team_dict = {}
   
    # loop through each team in the dataset
    for team in team_data:
       
        # add each teams namw to the dictionary along with an empty list
        team_dict[team[1]] = []
       
    return team_dict


def add_data_to_team(team_data, team_dict, data_col = -1, win_rate = False):
    """
    Adds a set of data to the corresponding teams' lists in the dictionary

    Parameters
    ----------
    team_data : 2d list
        list containing rows of data for NBA teams
    team_dict : dictionary
        a dictionary containing all the team's names and a corresponding
        data list
    data_col : int, -1 by default
        an integer providing the column number of the data to add to teams.
        -1 by default to prevent putting an arbitrary number in function call
    win_rate : boolean, False by default
        determines whether or not we would like to include the win rate

    Returns
    -------
    None.

    """
    # checks if user is adding win rate to their data
    if win_rate == True:
       
        # iterates through each team in data set
        for team in team_data:
           
            # calculates the win percentage for each team
            win_pct = get_win_rate(float(team[3]), float(team[4]))
           
            # appends the win rate to the dictionary
            team_dict[team[1]].append(win_pct)
           
    else:
        # loop through each team in the dataset
        for team in team_data:
           
            # add the chosen data to its cooresponding name in the dict
            team_dict[team[1]].append(float(team[data_col]))
   

def get_win_rate(wins, losses):
    """
    Gets the win percentage for a team given its wins and losses

    Parameters
    ----------
    wins : int
        number of games a team won over a year
    losses : int
        number of games a team lost over a year

    Returns
    -------
    win_rate : float
        a float representing a percentage of games won over a season

    """
    total_games = wins + losses
   
    # calculates win rate and converts into percent form, rounds to 1 decimal
    win_rate = round((wins / total_games) * 100, 1)
   
    return win_rate


def data_for_one_year(year, adv_data_cols, per_data_cols, win_rate = False):
    """
    Creates a dictionary containing all the data needed for a team

    Parameters
    ----------
    year : string
        the year to create the dictionary for
    adv_data_cols : list
        a list containing the column values of our desired data in the
        advanced data file
    per_data_cols : list
        a list containing the column values of our desired data in the
        per game data file
    win_rate : Boolean, False by default
        determines whether to add win_rate to team data

    Returns
    -------
    team_data_dict : dictionary
        a dictionary containing the teams and their corresponding data

    """
    # creates file path using input year
    advanced_file = year + " Advanced Data.txt"
    per_game_file = year + " Per Game Data.txt"
   
    # reads files using file path variables
    advanced_data = read_file(advanced_file)
    per_game_data = read_file(per_game_file)
   
    # removes asterisks
    remove_asterisks(advanced_data)
    remove_asterisks(per_game_data)
   
    # creates a team dict containing all team names
    team_data_dict = create_team_dict(per_game_data)
   
    # checks if user wants win rate
    if win_rate:
       
        # adds win rate to dictionary
        add_data_to_team(advanced_data, team_data_dict, None, win_rate)
   
    # iterates through columns in our list of desired columns
    for col in adv_data_cols:
       
        # adds each data point into its respective team
        add_data_to_team(advanced_data, team_data_dict, col)
   
    for col in per_data_cols:
       
        add_data_to_team(per_game_data, team_data_dict, col)
       
    return team_data_dict


def plot_scatterplot(team_data_dict, x_col, y_col, x_title, y_title, 
                     graph_title, color = "darkorchid", label = None):
    '''
    Plots two set of data points decided on by the input

    Parameters
    ----------
    team_data_dict : dictionary
        a dictionary containing the teams and their corresponding data.
    x_col : int
        the column containing the data we want on the x axis.
    y_col : int
        the column containing the data we want on the y axis.
    x_title : string
        title for the data on the x-axis.
    y_title : string
        title for the data on the y-axis.
    graph_title : string
        title for the graph.
    color : string, default "darkorchid"
        color to plot the points as.
    label : string, default None
        label for the data being plotted.

    Returns
    -------
    None.

    '''
    # creates counter to assist with legend
    label_count = 0
    
    # create initial lists for line of best fit
    x_vals = []
    y_vals = []
    
    # loops through each team in the dictionary
    for team in team_data_dict:
        
        # checks to make sure function plots only one point with a label
        if label_count == 0:
            
            # plots point for each team given input data from user
            plt.plot(team_data_dict[team][x_col], team_data_dict[team][y_col], 
                     "o", color = color, label = label)
            # adds to count so only one point is plotted with label
            label_count += 1
            
            # appends x and y values for line of best fit
            x_vals.append(team_data_dict[team][x_col])
            y_vals.append(team_data_dict[team][y_col])
        
        else:
            
            plt.plot(team_data_dict[team][x_col], team_data_dict[team][y_col],
                     "o", color = color)
            x_vals.append(team_data_dict[team][x_col])
            y_vals.append(team_data_dict[team][y_col])
    
    # create data for line of best fit using numpy built in functions
    x = np.array(x_vals)
    y = np.array(y_vals)
    m, b = np.polyfit(x, y, 1)
    
    # creates line of best fit as a string to allow it to be added to legend
    lobf_as_str = str(round(m, 2)) + " * x + " + str(round(b, 2))

    # plot line of best fit
    plt.plot(x, m * x + b, color = color, label = lobf_as_str)
    
    # graph organization
    plt.legend()
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(graph_title)

   
def get_data_by_age_range(team_data_dict, data_col = 0, age = 1):
    '''
    Takes a dictionary and returns a nested list of age and the desired column

    Parameters
    ----------
    team_data_dict : dict
        a dictionary containing all the previously retrieved columns
    data_col : int, optional, 0 by default
        the desired data column's index. The default is 0 (win percent).
    age : int, optional, 1 by default
        the index for the age column. The default is 1.

    Returns
    -------
    lst_of_ranges : lst
        a nested list containing 5 groups of 6 teams sorted by age.

    '''
    
    # initializes the overarching list
    league_attributes = []

    # loops through each team in dictionary
    for team in team_data_dict.keys():
        
        # initializes a list for each team
        team_attributes = []
        
        # defines team age
        team_age = team_data_dict[team][age]
                
        # defines team win percentage
        team_win_pct = team_data_dict[team][data_col]
        
        # appends each of these to the team's list, which is then appended
        # to the overarching list
        team_attributes.append(team_age)
        team_attributes.append(team_win_pct)
        league_attributes.append(team_attributes)
    
    # sorts league attributes by age
    league_attributes = sorted(league_attributes)
    
    # initializes a list of ranges
    lst_of_ranges = []
    
    # creates a nested list of 5 groups of 6 teams using slicing
    range_1 = league_attributes[0:6]
    lst_of_ranges.append(range_1)
    
    range_2 = league_attributes[6:12]
    lst_of_ranges.append(range_2)
    
    range_3 = league_attributes[12:18]
    lst_of_ranges.append(range_3)
    
    range_4 = league_attributes[18:24]
    lst_of_ranges.append(range_4)
    
    range_5 = league_attributes[24:30]
    lst_of_ranges.append(range_5)
    
    return lst_of_ranges
    

def avg_by_col(lst_of_ranges, col = 1):
    '''
    Takes the average value by column and returns two lists (data, age range).

    Parameters
    ----------
    lst_of_ranges : list
        a nested list returned from the data by age range function
    col : int, optional, 1 by default
        the nested list index containing desired data. The default is 1.

    Returns
    -------
    ranges : list
        a list of tuples that contain the upper and lower bound of the age 
        range.
    averages : list
        a list of the desired data's average by win column.

    '''
    # initializes overarching lists
    averages = []
    ranges = []
    
    # loops through each range in the list of ranges
    for range_ in lst_of_ranges:
        
        # defines arbitrary min and max value, as well as initializing sum
        min_val = None
        max_val = None
        range_sum = 0
        
        for team in range_:
            
            # redefines min val for age if less than min val or no min value
            if min_val == None or team[0] < min_val:
                
                min_val = team[0]
                
            # redefines max val for age if greater than max val or no max val
            if max_val == None or team[0] > max_val:
                
                max_val = team[0]
            
            # adds the column to the range's sum
            range_sum += team[col]

        # takes average of the range's data, rounds, and appends to list 
        averages.append(round((range_sum / 6), 2))

        # appends range into range list
        ranges.append(f"{min_val} - {max_val}")
        
    return ranges, averages


def plot_bar_graph(x_data, y_data, graph_title, x_title, y_title, color =
                   "mediumseagreen"):
    '''
    Takes in x data, y data to plot a bar graph

    Parameters
    ----------
    x_data : list
        list containing the data to plot on the x-axis.
    y_data : list
        list containing the data to plot on the y-axis.
    graph_title : string
        title for the graph.
    x_title : string
        title for the data on the x-axis.
    y_title : string
        title for the data on the y-axis.
    color : string, "mediumseagreen" by default
        color with which to plot bar graph

    Returns
    -------
    None.

    '''
    # plots bar graph using input data and color
    plt.bar(x_data, y_data, color = color)
    
    # graph organization
    plt.title(graph_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)


def baskemtball():
   
    print("Welcome to our final project!\n")
    
    # creates a dict for 2018-19 containing by team: [win %, avg age, pace, 
    # 3 pt attempts]
    data_2018_19 = data_for_one_year("2018-19", [2, 13], [8], True)
    
    # creates a dict for 1999-00 containing by team: [win %, 3 pt attempts]
    data_1999_00 = data_for_one_year("1999-00", [], [8], True)
    
    # creates a dict for 1979-80 containing by team: [win %, 3 pt attempts]
    data_1979_80 = data_for_one_year("1979-80", [], [8], True)
    
    # returns the dictionaries for each year
    print("Teams in 2018-19 season:\n", data_2018_19, "\n")
    print("Teams in 1999-00 season:\n", data_1999_00, "\n")
    print("Teams in 1979-80 season:\n", data_1979_80, "\n")
    
    # plots average age as compared to pace in the 2018-19 season
    plot_scatterplot(data_2018_19, 1, 2, "Average Age", "Pace",
                     "How Average Age Correlates to Pace (2018-19 Season)",
                     "darkgreen")
    plt.show()
    
    # plots pace as compared to win % in the 2018-19 season
    plot_scatterplot(data_2018_19, 2, 0, "Pace", "Winning Percentage (%)", 
                     "How Pace Correlates to Winning Percentage " +  
                     "(2018-19 Season)", "deeppink")
    plt.show()
    
    # plots average age as compared to win % in the 2018-19 season
    plot_scatterplot(data_2018_19, 1, 0, "Average Age", "Winning Percentage" +
                     " (%)", "How Age Correlates to Winning Percentage " +
                     "(2018-19 Season)", "#ff6362")
    plt.show()
    
    # for each season plots 3 pt attemtps as compared to win %
    plot_scatterplot(data_2018_19, 0, 3, "Winning Percentage (%)", 
                     "Number 3 Pt. Attempts", "How 3 Pt Attempts Correlate " +
                     "to Winning Percentage Over Time", "mediumseagreen", 
                     "2018-19")
    plot_scatterplot(data_1999_00, 0, 1, "Winning Percentage (%)", 
                     "Number 3 Pt. Attempts", "How 3 Pt Attempts Correlate " +
                     "to Winning Percentage Over Time", "gold", "1999-00")
    plot_scatterplot(data_1979_80, 0, 1, "Winning Percentage (%)", 
                     "Number 3 Pt. Attempts", "How 3 Pt Attempts Correlate " +
                     "to Winning Percentage Over Time", "lightcoral", 
                     "1979-80")
    # sets legend to the right of the graph for ease of presentation
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    # plots bar graph of age compared to win percentage in the 2018-19 season
    wins = get_data_by_age_range(data_2018_19)
    
    wins_by_age = avg_by_col(wins)
    
    plot_bar_graph(wins_by_age[0], wins_by_age[1], "Average Age and Winning "
                   + "Percentage (2018-19 Season)", "Average Age",
                   "Winning Percentage (%)", "#ff6362")
        
    plt.show()
    
    print(data_2018_19["Philadelphia 76ers"])

if __name__ == "__main__":
   
    baskemtball()
    