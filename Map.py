import plotly.graph_objs as go
import pandas as pd
from us_state_abbrev import us_state_abbrev


def convert(data):
    dat = []
    for key, value in data.items():
        it = [us_state_abbrev[key], value[2] / value[0], value[3] / value[1]]
        dat.append(it)
    return make_map(dat)


def make_map(dat):
    html = []
    data_frame = pd.DataFrame.from_records(dat, columns=['State', 'Graduate Size', 'Declining Balance'])
    visual = dict(
        type='choropleth',
        colorscale='Viridis',
        locations=data_frame['State'],
        locationmode="USA-states",
        z=data_frame['Graduate Size'],
        text=data_frame['State'],
        colorbar=dict(title='Ratio of # Employees/# Grads')
    )
    layout = dict(title='# Employees / # College Grads', geo=dict(projection={'type': 'mercator'}))
    choromap = go.Figure(data=[visual], layout=layout)
    choromap.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    html.append(choromap.to_html(include_plotlyjs='cdn'))
    visual = dict(
        type='choropleth',
        colorscale='Viridis',
        locations=data_frame['State'],
        locationmode="USA-states",
        z=data_frame['Declining Balance'],
        text=data_frame['State'],
        colorbar=dict(title='Ratio of 25%Salary / DB')
    )
    layout = dict(title=' Lower 25% Salary / Declining Balance', geo=dict(projection={'type': 'mercator'}))
    choromap2 = go.Figure(data=[visual], layout=layout)
    choromap2.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    html.append(choromap2.to_html(include_plotlyjs='cdn'))
    print(html[0])
    return html
