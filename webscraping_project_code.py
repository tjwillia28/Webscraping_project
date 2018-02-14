import numpy as np
import scipy as sp
import pandas as pd
import re
from matplotlib import pyplot as plt
plt.style.use('ggplot')
from datetime import datetime 

#---------------
# Functions
#---------------

# Convert string $ into a float that we can work with
def money_to_float(currency):
    if (currency == 'NOT SET'):
        return None
    elif (currency == 'PENDING'):
        return None
    else:
        x = re.sub(r'[^\d.]', '', currency)
        x = float(x)
        return x

#Convert growth factors into floats
def growth_factor_conv(str_):
    y = str_[:-1]
    y = float(y)
    return y

# Convert 2018 dates to proper format for analysis
def date_to_2018(date_str):
    date_str = date_str[:-2] + '2018'
    date_ = datetime.strptime(date_str, '%m/%d/%Y')
    return date_

# Convert 2017 dates to proper format for analysis
def date_to_2017(date_str_2):
    date_str_2 = date_str_2[:-2] + '2017'
    date_2 = datetime.strptime(date_str_2, '%m/%d/%Y')
    return date_2

# Extract month and year from datetime object and convert to string for grouping
def month_year_str(input_):
    input_month = input_.month
    input_year = input_.year
    return (str(input_month) + '_' + str(input_year))

## Expected Value Equations

#Find the number of winning investments in a column; input is a string
def num_winners(col_name_str, year):
    df = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == year]
    winners_ = df.loc[df[col_name_str] > 1]
    return len(winners_)

#Find the mumber of losing investments in a column; input is string
def num_losers(col_name_str, year):
    df = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == year]
    losers_ = ico_comp_rows.loc[ico_comp_rows[col_name_str] < 1]
    return len(losers_)

#Find the number of flat investments in a column; input is string
def num_flat(col_name_str):
    flat_ = ico_comp_rows.loc[ico_comp_rows[col_name_str] == 1]
    return len(flat)

#Average winner
def avg_winner(col_name_str):
    winners_ = ico_comp_rows.loc[ico_comp_rows[col_name_str] > 1]
    return winners_[col_name_str].mean()

# Average loser
def avg_loser(col_name_str):
    losers_ = ico_comp_rows.loc[ico_comp_rows[col_name_str] < 1]
    return losers_[col_name_str].mean()-1

#Winning Probability
def prob_win(col_name_str): 
    return num_winners(col_name_str)/(num_losers(col_name_str) + num_winners(col_name_str) + num_flat(col_name_str))

# Losing probability
def prob_lose(col_name_str):
    return num_losers(col_name_str)/(num_losers(col_name_str) + num_winners(col_name_str) + num_flat(col_name_str))

# Flat probability
def prob_flat(col_name_str):
    return num_flat(col_name_str)/(num_losers(col_name_str) + num_winners(col_name_str) + num_flat(col_name_str))

# Expected Value of Trade 
def ev_trade(col_name_str):
    return (prob_win(col_name_str)*avg_winner(col_name_str) + prob_lose(col_name_str)*avg_loser(col_name_str) + prob_flat(col_name_str)*1)
#---------------------------------------------


#Upload datasets
ico_gen_orig = pd.read_csv('/Users/ty/Desktop/Scrape_that_web/icodrops_ended_icos.csv', thousands = ',')
ico_ret_orig = pd.read_csv('/Users/ty/Desktop/Scrape_that_web/icodrops_stats_2_10_18.csv')

#===============
# Prepare our Data
#===============

#----------
# Duplicates
#-----------
# Get rid of missing rows in returns dataset
ico_ret_no_na = ico_ret_orig.dropna(axis = 0, how = 'all')

# Get rid of duplicate rows 
#ico_ret = ico_ret_no_na.head(n = 189) # 189, comes from looking at csv, If we have time see if you can do this with unique elements
ico_ret = ico_ret_no_na.drop_duplicates()

# Get rid of missing rows in general dataset 
ico_gen_no_na = ico_gen_orig.dropna(axis = 0, how = 'all')

# Get rid of duplicate rows
#ico_gen = ico_gen_no_na.head(n = 306) #306 comes from looking at csv
ico_gen = ico_gen_no_na.drop_duplicates()


#-----------
# Dealing with Date; Adding new date and days since ICO column
#-----------

# Need to fix date column; add year and convert to date
# Break dataframe into 2 by year and then add them back together
year_2018 = ico_gen[:84]
values_2018 = year_2018.End_Date.map(date_to_2018)
year_2018 = year_2018.assign(End_Date_man = values_2018)

year_2017 = ico_gen[84:-1]
values_2017 = year_2017.End_Date.map(date_to_2017)
year_2017 = year_2017.assign(End_Date_man = values_2017)

ico_gen = pd.concat([year_2018, year_2017])

# Add days since ICO column
Days_Since_ICO = datetime.today() - ico_gen['End_Date_man']
Days_Since_ICO = list(map(lambda x: x.days, Days_Since_ICO))
ico_gen = ico_gen.assign(Days_Since_ICO = Days_Since_ICO)

# Add new column to dataframe containing month and year end date of ICO
Month_Year_End_Date = list(map(month_year_str, ico_gen['End_Date_man']))
ico_gen = ico_gen.assign(Month_Year_End_Date = Month_Year_End_Date)


# Add new columns for float values of Received and Goal columns
#ico_gen  = ico_gen.loc[ico_gen.Received != 'PENDING']
z_1 = ico_gen.Received.map(money_to_float)
ico_gen = ico_gen.assign(Received_fl = z_1)

z_2 = ico_gen.Goal.map(money_to_float)
ico_gen = ico_gen.assign(Goal_fl = z_2)

# Add new columns where the growth factors are floats
z_3 = ico_ret.USD_ROI.map(growth_factor_conv)
ico_ret = ico_ret.assign(USD_ROI_fl = z_3)

z_4 = ico_ret.ETH_ROI.map(growth_factor_conv)
ico_ret = ico_ret.assign(ETH_ROI_fl = z_4)

z_5 = ico_ret.BTC_ROI.map(growth_factor_conv)
ico_ret = ico_ret.assign(BTC_ROI_fl = z_5)


# Join our two datasets and keep all data
ico_all_rows = pd.merge(ico_gen, ico_ret, how = 'outer', on = 'Ticker')

# Join our two datasets and keep only complete rows
ico_comp_rows = pd.merge(ico_gen, ico_ret, how = 'inner', on = 'Ticker')

#=============================
# Data Analysis: Monthly Descriptive statistics
#=============================

# Monthly stats

Col_Fun_1 = {'USD_ROI_fl': ['count', 'min', 'max', 'mean', 'std', 'median'],
           'ETH_ROI_fl' : ['count', 'min', 'max', 'mean', 'std', 'median'],
          'BTC_ROI_fl': ['count', 'min', 'max', 'mean', 'std', 'median']}

monthly_stats = ico_comp_rows.groupby('Month_Year_End_Date').agg(Col_Fun_1)
monthly_stats.sort_values


# Breaking our dataframe into smaller dataframes by Month so we can pass it to functions
# and calculate trade statistics

df_8_2017 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '8_2017']
df_9_2017 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '9_2017']
df_10_2017 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '10_2017']
df_11_2017 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '11_2017']
df_12_2017 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '12_2017']
df_1_2018 = ico_comp_rows.loc[ico_comp_rows['Month_Year_End_Date'] == '1_2018']

#Dataframe Input
df = df_8_2017
# ROI metric input 
roi_metric = 'USD_ROI_fl'


#Total icos
total_trades = len(df)
print(total_trades)
#Number winners/flat
df_winners = df.loc[df[roi_metric] >= 1]
num_winners = len(df_winners)
print(num_winners)
#Number of losers
df_losers = df.loc[df[roi_metric] <1]
num_losers = len(df_losers)
print(num_losers)
# Average Winner
average_winner = df_winners[roi_metric].mean() - 1
print(average_winner)
# Average loser
average_loser = df_losers[roi_metric].mean() - 1
print(average_loser)
# Winning Probability
winning_prob = num_winners/total_trades
print(winning_prob)
# Losing Probability
losing_prob = num_losers/total_trades
print(losing_prob)
# Expected Value
Expected_value = average_winner*winning_prob + average_loser*losing_prob
print(Expected_value)

#===========================
# Data Visualzation
#============================

# Box Plots!

#ICO Growth Factors USD
plt.boxplot([df_8_2017['USD_ROI_fl'], df_9_2017['USD_ROI_fl'], df_10_2017['USD_ROI_fl'],
             df_11_2017['USD_ROI_fl'], df_12_2017['USD_ROI_fl'], df_1_2018['USD_ROI_fl']])
plt.xticks([1, 2, 3, 4, 5, 6], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.xlabel('Month/Year')
plt.ylabel('Growth Factor')
plt.title('ICO Growth Factors(USD) Since August 2017')

#ICO Growth Factors ETH
plt.boxplot([df_8_2017['ETH_ROI_fl'], df_9_2017['ETH_ROI_fl'], df_10_2017['ETH_ROI_fl'],
             df_11_2017['ETH_ROI_fl'], df_12_2017['ETH_ROI_fl'], df_1_2018['ETH_ROI_fl']])
plt.xticks([1, 2, 3, 4, 5, 6], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.xlabel('Month/Year')
plt.ylabel('Growth Factor')
plt.title('ICO Growth Factors(ETH) Since August 2017')

#ICO Growth Factors BTC
plt.boxplot([df_8_2017['BTC_ROI_fl'], df_9_2017['BTC_ROI_fl'], df_10_2017['BTC_ROI_fl'],
             df_11_2017['BTC_ROI_fl'], df_12_2017['BTC_ROI_fl'], df_1_2018['BTC_ROI_fl']])
plt.xticks([1, 2, 3, 4, 5, 6], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.xlabel('Month/Year')
plt.ylabel('Growth Factor')
plt.title('ICO Growth Factors(BTC) Since August 2017')

# Bar Graphs!

#Avg. Monthly Winner/Loser USD
n_groups = 6

#avg winner/loser usd, avg winner/loser btc, avg winner/loser eth
mean_winners_usd =(4.09, 7.75, 2.85, 3.64, 2.7, 1.97) 
mean_losers_usd = (-.4, -.38, -.41, -.35, -.32, -.38)

plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

rects1 = plt.bar(index, 
                 mean_winners_usd, 
                 color = 'Green',
                 label = 'Average Winners')

rects2 = plt.bar(index,
                mean_losers_usd,
                color = 'Red',
                label = 'Average Losers')

plt.xlabel('Month/Year')
plt.ylabel('Average Winner/Loser')
plt.title('Monthly Average Winners and Losers(USD)')
plt.xticks([0,1, 2, 3, 4, 5], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.legend()

plt.tight_layout()
plt.show()

#Avg. Monthly Winner/Loser ETH

n_groups = 6
#avg winner/loser usd, avg winner/loser btc, avg winner/loser eth
mean_winners_eth =(2.44, 3.18, 0.98, 1.4, 1.77, 1.56) 
mean_losers_eth = (-.59, -.57, -.59, -.49, -.43, -.32)

plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

rects1 = plt.bar(index, 
                 mean_winners_eth, 
                 color = 'Green',
                 label = 'Average Winners')

rects2 = plt.bar(index,
                mean_losers_eth,
                color = 'Red',
                label = 'Average Losers')

plt.xlabel('Month/Year')
plt.ylabel('Average Winner/Loser')
plt.title('Monthly Average Winners and Losers(ETH)')
plt.xticks([0,1, 2, 3, 4, 5], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.legend()

plt.tight_layout()
plt.show()

#Avg. Monthly Winner/Loser BTC

n_groups = 6
#avg winner/loser usd, avg winn
mean_winners_btc =(2.96, 3.85, 1.77, 3.07, 4.44, 2.43) 
mean_losers_btc = (-.5, -.52, -.53, -.42, -.31, -.26)

plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

rects1 = plt.bar(index, 
                 mean_winners_btc, 
                 color = 'Green',
                 label = 'Average Winners')

rects2 = plt.bar(index,
                mean_losers_btc,
                color = 'Red',
                label = 'Average Losers')

plt.xlabel('Month/Year')
plt.ylabel('Percentage Return')
plt.title('Monthly Average Winners and Losers(BTC)')
plt.xticks([0,1, 2, 3, 4, 5], ['8/17', '9/17', '10/17', '11/17', '12/17', '1/18'])
plt.legend()

plt.tight_layout()
plt.show()
























