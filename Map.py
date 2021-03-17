import plotly
import plotly.graph_objs as go
import pandas as pd
from plotly import offline

import us_state_abbrev


def get_map(data, method):
    data_vis = []
    for item in data:
        if len(item[0]) > 3:
            temp_state = us_state_abbrev.us_state_abbrev[item[0]]
        temp_val_one = item[3] / item[1]  # ratio of employee number / graduate number
        temp_val_two = item[2] / item[4]  # ratio of balance / 25 lower salary
        data_vis.append([temp_state, temp_val_one, temp_val_two])
    data_frame = pd.DataFrame.from_records(data_vis, columns=['State', 'Graduate Size', 'Declining Balance'])
    if method == 1:
        visual = dict(
            type='choropleth',
            colorscale='Viridis',
            locations=data_frame['State'],
            locationmode="USA-states",
            z=data_frame['Graduate Size'],
            text=data_frame['State'],
            colorbar=dict(title='Ratio of # Employees/# Grads')
        )
        layout = dict(title='Ratio # Employees / # College Graduates', geo=dict(projection={'type': 'mercator'}))
    else:
        visual = dict(
            type='choropleth',
            colorscale='Viridis',
            locations=data_frame['State'],
            locationmode="USA-states",
            z=data_frame['Declining Balance'],
            text=data_frame['State'],
            colorbar=dict(title='Ratio of DB/25%Salary')
        )
        layout = dict(title='Ratio of Declining Balance / Lower 25% Salary', geo=dict(projection={'type': 'mercator'}))
    choromap = go.Figure(data=[visual], layout=layout)
    choromap.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    return choromap.to_html(include_plotlyjs='cdn')
