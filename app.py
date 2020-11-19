import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import Dash 
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


p1text = ''' 

The source tells us that there are many different ways to measure the difference in income for men and women including looking at annual pay for full-time workers, hourly pay for full-time and part-time workers, and considering other factors such educational level and types of occupation. It also states that no matter how you examine the problem there is always evidence of a gap being present. It goes on to mention how "adjusted" calculations aren't as different as they may claim to be. It also debunks some common myths like "women can close the wage gap by getting more education". Overall this article is very firm on its stance that a wage gap between men and women is present.

Link to Source- [epi.org/publication/what-is-the-gender-pay-gap-and-is-it-real/](https://www.epi.org/publication/what-is-the-gender-pay-gap-and-is-it-real/)

The GSS (General Social Survey) is an organization that collects data on cultural trends, behavior, and attributies in the United States. The data is collected through surveys completed by American citizens facilitated by the GSS. The data contains demographic, behavioral, and attitudinal information on a wide range of subjects from crime to spending habits. The GSS claims to be "the single best source for sociological and attitudinal trend data covering the United States by allowing researchers to examine the structure and functioning of society in general."

Link to Source- [http://www.gss.norc.org/About-The-GSS](http://www.gss.norc.org/About-The-GSS) '''


gss_bar = gss_clean.groupby('sex', sort=False).agg({'income':'mean',
                                    'job_prestige':'mean',
                                    'socioeconomic_index':'mean',
                                    'education': 'mean'}).round(2)
gss_bar.reset_index(inplace= True)

gss_bar = gss_bar.rename({'sex': 'Sex','income' : 'Income', 'job_prestige': "Job Prestige",
                          'socioeconomic_index': 'Socioeconomic Index', 'education': 'Years of Education'}, axis=1)

p2table = ff.create_table(gss_bar)


gss_p3 = gss_clean.groupby(['sex', 'male_breadwinner']).size()
gss_p3 = gss_p3.reset_index()
gss_p3 = gss_p3.rename({0:'count'}, axis=1)

p3Barfig = px.bar(gss_p3, x='male_breadwinner', y='count', color='sex',
            labels={'male_breadwinner':'Level of Agreement', 'count':'Count'},
            text='count',
            barmode = 'group')
p3Barfig.update_layout(showlegend=True)
p3Barfig.update(layout=dict(title=dict(x=0.5)))


gss_scatter = gss_clean[~gss_clean.sex.isnull()]


p4Scatterfig = px.scatter(gss_scatter, x='job_prestige', y='income', 
                 color = 'sex', trendline = 'ols',
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
p4Scatterfig.update(layout=dict(title=dict(x=0.5)))


p5BoxfigInc = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''})
p5BoxfigInc.update(layout=dict(title=dict(x=0.5)))
p5BoxfigInc.update_layout(showlegend=False)


p5BoxfigPres = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''})
p5BoxfigPres.update(layout=dict(title=dict(x=0.5)))
p5BoxfigPres.update_layout(showlegend=False)


mycols = ['income', 'sex', 'job_prestige']

newdf = gss_clean[mycols]

newdf['job_cat'] = pd.cut(newdf.job_prestige, bins=6, labels=("1 Very Low", "2 Low", "3 Medium", "4 High", "5 Very High", "6 Super High"))
                                      
newdf = newdf.dropna()
newdf = newdf.sort_values('job_cat')

p6MultBoxfig = px.box(newdf, x='income', y = 'sex', color = 'sex', facet_col = 'job_cat', facet_col_wrap = 2,
                   labels={'income':'Income', 'sex':''})
p6MultBoxfig.update(layout=dict(title=dict(x=0.5)))
p6MultBoxfig.update_layout(showlegend=False)






bar_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']
group_columns = ['sex', 'region', 'education']

app2 = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#999999',
    'text': '#000000',
    'title' : '#ffebcc'
}

newp4 = p4Scatterfig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

newp5Inc = p5BoxfigInc.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

newp5Pres = p5BoxfigPres.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

newp6 = p6MultBoxfig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app2.layout = html.Div(style={'backgroundColor': colors['background']}, children=
    [
        html.H1(children = "Analytical Depiction Of the Gender Wage Gap", style= {
            'textAlign': 'center','color': colors['title'], 'font-family': 'monaco'}),
        
        dcc.Markdown(children = p1text, style = {'textAlign': 'center','color': colors['text']}), 
        
        html.H2(children = "Comparing Income, Prestige, Socioeconomic Index, and Education", style = {
            'textAlign': 'center','color': colors['title']}),
        dcc.Graph(figure=p2table),
        
        html.Div([

            html.H3(children ="Display Bars", style = {'font-size':45, 'color': colors['title']}),

            dcc.Dropdown(id='bars', options=[{'label': i, 'value': i} for i in bar_columns], value='male_breadwinner'),

            html.H3(children = "Grouping", style = {'font-size':45, 'color': colors['title']}),
            dcc.Dropdown(id='group',options=[{'label': i, 'value': i} for i in group_columns], value = 'sex')

        ], style={'width': '25%', 'float': 'left'}),
        
        html.Div([
            
          dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),
        
        html.Div([
            html.H2(children = "Income vs. Job Prestige", style = {'color': colors['title']}),
            dcc.Graph(figure=p4Scatterfig),
        ], style = {'margin-top': '500px', 'margin-left':'180px',}),

        
        html.Div([
            
            html.H2(children = "Distribution of Income", style = {'textAlign': 'center','color': colors['title']}),
            dcc.Graph(figure=p5BoxfigInc)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2(children = "Distribution of Prestige", style = {'textAlign': 'center','color': colors['title']}),
            dcc.Graph(figure=p5BoxfigPres)
            
        ], style = {'width':'48%', 'float':'right'}),
    
        
        html.H2(children= "Distribution of Income by Job Prestige Type", style = {'textAlign': 'center','color': colors['title']}),
        dcc.Graph(figure=p6MultBoxfig)
    
    ]
)   
@app2.callback(Output(component_id="graph",component_property="figure"), 
              [Input(component_id='bars',component_property="value"),
               Input(component_id='group',component_property="value")])

def make_figure(x, y):
    gss_tmp = gss_clean.groupby([y, x]).size()
    gss_tmp = gss_tmp.reset_index()
    gss_tmp = gss_tmp.rename({0:'count'}, axis=1)
    returnFig = px.bar(gss_tmp, x=x, y='count', color = y, barmode='group')
    
    newreturnFig = returnFig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    
    return newreturnFig


if __name__ == '__main__':
    app2.run_server(debug=True)
