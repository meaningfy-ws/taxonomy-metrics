import plotly.express as px
import pandas as pd

df = pd.read_csv("C://Users//USER//PycharmProjects//EuroStat//statSAI//jana csv//corporate-body-classification-skos-ap-act.json.csv")

df = df.sort_values(by=['avg'])
x = df['property'].values
y = df['avg'].values

fig = px.scatter(df, x='property', y='avg', hover_data=['subject_class'])
fig.show()