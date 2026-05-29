import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

#list with all functions, when more are added, add to list
possible_functions = ["Describe data", "Correlate data", "Graph Scatter Plot"]
#messages for correlation and describe function.
select_message = "\nInput any (including multiple) of the following data"

def find_file():
    """ 
    Asks for file name, opening and reading its contents

    Return:
        data (pd.DataFrame) Dataframe of file contents
    """
    while True:
        file_name = input("File name: ")
        try:
            #find file path
            file_location = Path(__file__).parent
            
            #validate type and open file
            suffix = file_name.split(".")[-1]

            if suffix.lower() == "csv":
                #use file path to open csv file
                data = pd.read_csv(file_location / file_name)
                return data
            elif suffix.lower() == "xlsx":
                #use file path to open excel file
                data = pd.read_excel(file_location / file_name)
                return data
            elif suffix.lower() == "json":
                #use file path to open excel file
                data = pd.read_json(file_location / file_name)
                return data
            else:
                print("The file type input is not valid, please try again.\n")

        except FileNotFoundError:
            print("The input file was not found. Please try again.\n")


def make_action(data):
    """ 
    Asks user what action they wish to make, then running the corresponding function

    Parameter:
        data (pd.DataFrame) Dataframe of file contents
    """
    #make variable for only numeric data for numeric only functions
    numeric_data = data.select_dtypes(include="number")
    #create counter and run for loop to make list of functions
    count = 1
    print("Choose an action to perform on the data:")
    for i in possible_functions:
        print(f"{count}. {i}")
        count += 1

    while True:
        try:
            chosen_action = int(input("\nChosen Action Number: "))

            if chosen_action == 1:
                describe_data(numeric_data)
                return
            elif chosen_action == 2:
                correlate_data(numeric_data)
                return
            elif chosen_action == 3:
                graph_scatter_plot(numeric_data)
                return
            else:
                print("Invalid action. Try again")
        except ValueError:
            print("Invalid action. Please input the corresponding number of your action.")

def find_selected_data(available):
    """ 
    Finds data from chosen variables in file dataframe

    Parameter:
        available (list) List of numerical variable names
    
    Returns:
        available: if all variables are selected
        selected (list) all selected variable names
    """
    #create temporary dictionary with index being lowercase column name for lookup, 
    #and element being column name with correct capitalization
    column_dict = {i.lower(): i for i in available}
    while True:
        selected = []
        #lets user select data columns and validates selection
        selected_data = input(f"{select_message} {', '.join(available)}. Type 'All' "
                            "to select all available columns. ")
        
        #remove all commas and format selected data
        valid_data = selected_data.replace(',', "")
        selected_data_list = valid_data.split()

        #check is 'all is selected'
        if selected_data.strip().lower() == "all":
            return available
        
        #for each element in the user input, check if it is in the dicionary of columns
        valid = True
        for o in selected_data_list:
            if o.lower() not in column_dict:
                print("Invalid input. Ensure all words are in the column list.")
                valid = False
                break
            #append correctly capitalized string into selected list 
            selected.append(column_dict[o])
    
        if valid == True:
            return selected

def describe_data(numeric_data):
    """ 
    Sets data into a format that can be passed analysis functions, printing the results

    Parameter:
        numeric_data (Dataframe) All number based variables in the chosen file
    
    Returns:
        Printed message of eval_mean, eval_iqr and eval_range
    """
    #gets headings of all numeric data
    available_data = list(numeric_data.columns)

    #create done variable for while loop which is returned true when input is validated
    selected_list = find_selected_data(available_data)

    #describe selected data
    data_described = numeric_data[selected_list].describe()
    print(data_described)

    mean_message = eval_mean(selected_list, data_described)
    iqr_message = eval_iqr(selected_list, data_described)
    range_message = eval_range(selected_list, data_described)
    print(mean_message, iqr_message, range_message)

def eval_mean(selected, described):
    """ 
    Makes printable mean data information

    Parameter:
        selected (list) Selected valiable names to be analysed
        described (pd.DataFrame) Statistical summary of file's numeric data
    
    Returns:
        Mean data string
    """
    mean_list = []

    for column in selected:
        mean_list.append(described.loc['mean', column])

    if len(selected) > 1:
        #gets mean values
        mean_high = max(mean_list)
        mean_high_index = mean_list.index(mean_high)

        mean_low = min(mean_list)
        mean_low_index = mean_list.index(mean_low)

        #get column names of high/low means
        mean_high_column = described.columns[mean_high_index]
        mean_low_column = described.columns[mean_low_index]

        return f"""
Highest mean:
    {mean_high_column}, {mean_high:.4f}
Lowest mean:
    {mean_low_column}, {mean_low:.4f}
Mean difference:
    {mean_high - mean_low}
"""
    
    else:
        return f"""
Mean: 
    {mean_list[0]}
"""

def eval_iqr(selected, described):
    """ 
    Makes printable inter-quartile range data information

    Parameter:
        selected (list) Selected valiable names to be analysed
        described (pd.DataFrame) Statistical summary of file's numeric data
    
    Returns:
        Inter-quartile range data string
    """
    lower_q_list = []
    upper_q_list = []
    iqr_list = []

    for column in selected:
        lower_q_list.append(described.loc['25%', column])
        upper_q_list.append(described.loc['75%', column])
        iqr_list.append(described.loc['75%', column] - described.loc['25%', column])

    if len(selected) > 1:
        #get iqr values
        iqr_high = max(iqr_list)
        iqr_high_index = iqr_list.index(iqr_high)

        iqr_low = min(iqr_list)
        iqr_low_index = iqr_list.index(iqr_low)

        #get iqr column names
        iqr_high_column = described.columns[iqr_high_index]
        iqr_low_column = described.columns[iqr_low_index]

        return f"""
Largest inter-quartile range:
    {iqr_high_column}: Upper Quartile {upper_q_list[iqr_high_index]}, Lower Quartile {lower_q_list[iqr_high_index]}, IQR {iqr_high:.4f}
Smallest inter-quartile range:
    {iqr_low_column}: Upper Quartile {upper_q_list[iqr_low_index]}, Lower Quartile {lower_q_list[iqr_low_index]}, IQR {iqr_low:.4f}
"""
    
    else:
        return f"""
Inter-quartile range:
    Upper Quartile {upper_q_list[0]}, Lower Quartile {lower_q_list[0]}, IQR {iqr_list[0]}
"""

def eval_range(selected, described):
    """ 
    Makes printable range data information

    Parameter:
        selected (list) Selected valiable names to be analysed
        described (pd.DataFrame) Statistical summary of file's numeric data
    
    Returns:
        Range data string
    """
    min_list = []
    max_list = []
    range_list = []

    for column in selected:
        min_list.append(described.loc['min', column])
        max_list.append(described.loc['max', column])
        range_list.append(described.loc['max', column] - described.loc['min', column])

    if len(selected) > 1:
        #get range values
        high_range = max(range_list)
        high_range_index = range_list.index(high_range)

        low_range = min(range_list)
        low_range_index = range_list.index(low_range)

        #get range column names
        high_column = described.columns[high_range_index]
        low_column = described.columns[low_range_index]

        return f"""
Largest range:
    {high_column}: Maximum {max_list[high_range_index]}, Minimum {min_list[high_range_index]}, Range {high_range:.4f}
Smallest range:
    {low_column}: Maximum {max_list[low_range_index]}, Minimum {min_list[low_range_index]}, Range {low_range:.4f}
"""
    
    else:
        return f"""
Range:
    Maximum {max_list[0]}, Lower Quartile {min_list[0]}, Range {range_list[0]}
"""


def correlate_data(numeric_data):
    """ 
    Makes printable correlated data information

    Parameter:
        numeric_data (Dataframe) All number based variables in the chosen file
    
    Returns:
        Correlation data string
    """
    # gets headings of all numeric data
    available_data = list(numeric_data.columns)
    # get numeric data
    selected_list = find_selected_data(available_data)

    data_correlated = numeric_data[selected_list].corr().abs()

    # remove self-correlations
    np.fill_diagonal(data_correlated.values, np.nan)

    # turn table into list
    correlated_series = data_correlated.stack()

    # highest correlation
    corr_high_index = correlated_series.idxmax()
    corr_high = correlated_series.loc[corr_high_index]

    # lowest correlation
    corr_low_index = correlated_series.idxmin()
    corr_low = correlated_series.loc[corr_low_index]
    
    #make a message to show on interface
    correlation_message = f"""
Highest Correlation:
    {corr_high_index[0]} : {corr_high_index[1]}: {corr_high:.6f}

Lowest Correlation:
    {corr_low_index[0]} : {corr_low_index[1]}: {corr_low:.6f}
"""
    #print message
    print(correlation_message)

def get_graph_variables(available, var_type):
    """ 
    Asks user what variables they want to be used for a scatter plot

    Parameter:
        available (list) List of numerical variable names
        var_type (str) Axes the variable will be on (x/y)
    
    Returns:
        axis_data (pd.DataFrame) relevant data for plotting
    """
    #see find_selected_data()
    column_dict = {i.lower(): i for i in available}
    while True:
        axis_data = input(f"Select a {var_type} variable from {', '.join(available)}. ")

        #checks if axis_data is in the column list
        if axis_data.strip().lower() not in column_dict:
            print("Invalid input, please ensure your variable is in the lis of columns.\n")
        else:
            #gets correct capitalization of axis_data (from dictionary) to get data from dataframe
            axis_data = column_dict[axis_data.strip().lower()]
            return axis_data

def get_regression_line(x, y):
    """ 
    Asks user if they want a regression line and if so, begins fitting calculations

    Parameter:
        x (np.ndarray) Array of x values for plotting
        y (np.ndarray) Array of y values for plotting
    
    Returns:
        regression_line: Status of whether there will be a regression line (True/False)
        xs: sorted array of x values 
        y_fitted: y values of regression line
    """

    while True:
        try:
            regression_status = input("Would you like a regression line? (y/n) ")
            if regression_status.strip().lower() == 'y':
                degree = input("\nPlease select a degree for the regression line. ")
                coefficients = np.polyfit(x, y, deg=int(degree))

                #sort xs and fitted y so a continous line is drawn
                sorted_indicies = np.argsort(x)
                sorted_xs = x[sorted_indicies]

                #gets the y_fitted values
                xs, y_fitted = get_fitted_values(sorted_xs, coefficients)
                return True, xs, y_fitted
            
            elif regression_status.strip().lower() == 'n':
                #return false so no line is made with no values
                return False, None, None
            else:
                print("Please pick either 'y' or 'n'.\n")
        except ValueError:
            print("Invalid regression line degree type. Please try again and ensure the degree is an integer.")

def get_fitted_values(xs, coefficients):
    """ 
    Calculates y_fitted values for regression line based off given coefficients

    Parameter:
        xs (np.ndarray) sorted x values for plotting
        coefficients (np.ndarray) Coefficients based off regression line degree
    
    Returns:
        xs: sorted x values 
        y_fitted: y values of regression line
    """
    #makes initial array that will be added to over each degree of the polynomial
    fitted_y = np.zeros(len(xs))
    exponent = len(coefficients) - 1


    for coefficient in coefficients:
        degree_fit = coefficient * (xs ** exponent)
        fitted_y = fitted_y + degree_fit
        exponent -= 1

    return xs, fitted_y


def graph_scatter_plot(numeric_data):
    """ 
    Graphs scatter plot using the numeric data selected

    Parameter:
        numeric_data (Dataframe)
    
    Returns:
        Matplotlib scatter plot
    """
    # gets headings of all numeric data
    available_data = list(numeric_data.columns)
    
    #get x variable
    x_var = get_graph_variables(available_data, 'x')
    #remove axis_data from available list so graph cant have same variables
    available_data.remove(x_var)
    #get y variable
    y_var = get_graph_variables(available_data, 'y')

    #get x and y values
    xs = np.array(numeric_data.loc[:, x_var])
    ys = np.array(numeric_data.loc[:, y_var])

    #validate xs and ys so there are no nan or inf
    valid_mask = np.isfinite(xs) & np.isfinite(ys)
    xs = xs[valid_mask]
    ys = ys[valid_mask]

    #ask if use wants a line of best fit
    regression_line, sorted_xs, y_fitted = get_regression_line(xs, ys)

    axes = plt.axes()
    axes.plot(xs, ys, 'go')
    if regression_line:
        # axes.plot(xs, slope * ys + intercept)
        axes.plot(sorted_xs, y_fitted, '-b')
    axes.set_title(f"{x_var} by {y_var}.")
    axes.set_xlabel(x_var)
    axes.set_ylabel(y_var) 
    plt.show()

def main():
    """main function of program, welcoming user and describing the choose file steps"""

    print("Welcome to the data analysis tool. To get started please input the name of the file "
        "you wish to use.\nNote: Please ensure the file you wish to use is in the same folder as " 
        "this script.\n")

    data = find_file()
    make_action(data)

main()