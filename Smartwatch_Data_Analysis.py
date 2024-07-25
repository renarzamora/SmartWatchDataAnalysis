import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os

class SmartWatchAnalyzer:
    def __init__(self):
        self.data = None
    
    def load_data(self, filepath):
        self.data = pd.read_csv(filepath)
        print('Data loaded successfully')
    
    def eda_process(self):
        print('Eda Process')
        print('Head of the dataset')
        print(self.data.head())

        # checking null values
        print(self.data.isnull())

        # We confirmed the dataset doesn't have null values
        # Let's have a look at the information about columns in the dataset
        print(self.data.info())

        # As we can see the column containing the date of the record is an object, 
        # so we need to convert this column into a datetime column

        # changing datatype of ActivityDate
        self.data['ActivityDate'] = pd.to_datetime(self.data['ActivityDate'], format="%m/%d/%Y")
        print(self.data.info())

        #Looking at all the columns; we see information about very active, fairly active, lightly active, and sedentary minutes in the dataset. 
        # Let’s combine all these columns as total minutes before moving forward:
        self.data['TotalMinutes'] = self.data['VeryActiveMinutes'] + self.data['FairlyActiveMinutes'] + self.data['LightlyActiveMinutes'] + self.data['SedentaryMinutes']

        # Now we can take a look at the descriptive statistics of the dataset
        print(self.data.describe())
        print('EDA process finished successfully')

    def analize_process(self):
        print('Dataset Analisis Process')

        # the dataset has a "Calories" column, it contains the data about the number of the calories burned in a day.
        # Let's have a look about at the relationship between calories burned and the total steps walked in a day
        figure = px.scatter(data_frame=self.data, x='Calories',
                            y='TotalSteps', size='VeryActiveMinutes',
                            trendline='ols',
                            title='Relationship between Calories and Total Steps')
        figure.show()

        # You can see that there is a linear relationship between the number of the steps and and the number of calories burned in a day
        label = ['Very Active Minutes', 'Fairly Active Minutes','Lightly Active Minutes','Inactive Minutes']
        counts = self.data[['VeryActiveMinutes', 'FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes']].mean()
        colors =['gold','lightgreen','pink','blue']

        fig = go.Figure(data=[go.Pie(labels = label, values = counts)])
        
        fig.update_layout(title_text = 'Total Active Minutes')
        fig.update_traces(hoverinfo = 'label + percent', textinfo = 'value', textfont_size = 30,
                          marker = dict(colors = colors, line = dict(color = 'black', width = 3)))
        fig.show()

        # Observations: 
        # 81.3% of Total inactive minutes in a day
        # 15.8% of Lightly active minutes in a day
        # On an average, only 21 minutes (1.74%) were very active
        # and 1.11% (13 minutes) of fairly active minutes in a day

        # We transformed the data type of the ActivityDate column to the datetime column above. 
        # Let’s use it to find the weekdays of the records and add a new column to this dataset as “Day”

        self.data['Day'] = self.data['ActivityDate'].dt.day_name()
        print(self.data['Day'].head())

        # Now let’s have a look at the very active, fairly active, and lightly active minutes on each day of the week
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = self.data['Day'],
            y = self.data['VeryActiveMinutes'],
            name = 'Very Active',
            marker_color = 'purple'
        ))

        fig.add_trace(go.Bar(
            x = self.data['Day'],
            y = self.data['FairlyActiveMinutes'],
            name = 'Fairly Active',
            marker_color = 'green'
        ))

        fig.add_trace(go.Bar(
            x = self.data['Day'],
            y = self.data['LightlyActiveMinutes'],
            name = 'Lightly Active',
            marker_color = 'pink'
        ))

        fig.update_layout(barmode='group', xaxis_tickangle = -45)
        fig.show()

        # Now, let's have a look at the number of inactive minutes on each day of the week
        day = self.data['Day'].value_counts()
        label = day.index
        counts = self.data['SedentaryMinutes']
        colors = ['gold', 'lightgreeen', 'pink', 'blue', 'skyblue', 'cyan', 'orange']
        
        fig = go.Figure(data=[go.Pie(labels = label, values = counts)])
        fig.update_layout(title_text = 'Inactive Minutes Daily')
        fig.update_traces(hoverinfo = 'label+percent', textinfo = 'value', textfont_size = 30,
                       marker = dict(colors = colors, line = dict(color = 'black', width = 3)))
        fig.show()
    
        # So Thursday is the most inactive day according to the lifestyle of all the individuals in the dataset.
        #  Now let's have a look at the number of the calories burned each day of the week

        calories = self.data['Day'].value_counts()
        label = calories.index
        counts = self.data['Calories']
        colors = ['gold', 'lightgree', 'pink', 'blue', 'skyblue', 'cyan', 'orange']
        fig = go.Figure(data = go.Pie(labels = label, values = counts))
        fig.update_layout(title_text = 'Calories Burned Daily')
        fig.update_traces(hoverinfo = 'label+percent', textinfo = 'value', textfont_size = 30,
                          marker = dict(colors = colors, line = dict(color = 'black', width = 3)))
        fig.show()

        # Tuesday is, therefore, one of the most active days for all individuals in the dataset, as the highest number of calories
        # were burned on Tuesdays.
        # So this is how you can analyze smartwatch data using the Python programming language. There is a lot more you can do with this dataset. 
1        # You can also use it for predicting the number of calories burned in a day.

# usage example
if __name__ == '__main__':
    analizer = SmartWatchAnalyzer()
    filepath = os.getcwd()+'\dailyActivity_merged.csv'
    analizer.load_data(filepath)
    analizer.eda_process()
    analizer.analize_process()


