#!/usr/bin/env python
# coding: utf-8

# Project: Macro Data Explorer
# 
# Author: Elom Kwamin, FRM
# 
# Date: 26.12.2023
# 

# ### step 1: import required packages and data

# ##### 1.0 import packages for frontend

# In[1]:


from jupyter_dash import JupyterDash
from dash import Dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash import dash_table


# ##### 1.1 packages for data analysis

# In[2]:


import pandas as pd
import numpy as np


# ##### 1.2 import packages for data visualization

# In[3]:


import plotly
import plotly.express as px
import plotly.graph_objects as go


# ##### 1.3 import for clustering analysis

# In[4]:



from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sklearn


# ##### 1.4 import lotties extensions and sources

# In[5]:


import dash_extensions as de
# lotties json
linkedin_lottie_url = "https://lottie.host/c57a06dc-0bbc-4f22-b345-3c0115030ea9/G0GQpemRva.json"
youtube_lottie_url = "https://lottie.host/8d1aa277-f7af-4087-ab07-4e6a6632791a/oaW50SV1n4.json"
instagram_lottie_url = "https://lottie.host/d9fb345b-ef36-474b-ae20-91e762682f60/e4UvyiK7NB.json"
gmail_lottie_url = "https://lottie.host/be5e90ad-1f51-4e23-a9b6-495d7b75e337/HedBu0QYP8.json"

lotties_options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# ##### 1.5 import pre-processed world bank data for visualization

# In[6]:


DF = pd.read_excel('data/macro_data_melted_df2.xlsx')


# In[ ]:





# In[ ]:





# ### step 2: instantiate app

# In[7]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Set the title of the app
app.title = 'Macro Data Explorer'

server = app.server # required line before upload to render


# In[ ]:





# In[ ]:





# ### step 3: app layout

# ##### 3.1 layout for web app header

# In[8]:


# header section
header_section =  html.Div([
        
        html.H1("Macro Data Explorer", className="text-center mt-2 mb-1"),
        
        html.H5("|| Peer Comparison Web App ||",className="text-center mb-0", style={'font-family': 'Calibri Light'}),
        
        html.Div(style={"border-bottom": "10px groove black", "padding": "5px", }), 
    ], 
        
    style={"border": "0px royal blue",  # 2px border with black color
                        'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                        "padding": "10px"  },
         
    className="header")  # Use the "header" class in css file for styling


# ##### 3.2 layout for data setup section

# In[9]:


# data setup collapse button

data_setup_collapse = html.Div(
    [
        dbc.Button(
            "Data",
            id="data-setup-collapse-button",
            className="button-collapse",
            color="primary",
            n_clicks=0,
            style={"margin": "5px"},  # Add a margin to the left
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown("""
                    Customize data for further exploration
                    - Select year range for analysis
                    - Select continents of interest
                    - Visualize a time series of top 20 countries based on indicators selected.
                    """)
                )
            ),
            id="data-setup-collapse",
            is_open=False,
        ),
    ],
     style={
        "border-top": "5px inset blue", # different border styles: double, solid, dashed, groove, outset, ridge, inset
        'box-shadow': '0px 0px 0px 0px rgba(0, 0, 0, 0.2)',
        "padding": "10px",
    }
)


# In[10]:


# data setup content    
data_setup_section = html.Div([

        ########################################## DATA SETUP SECTION ############################################
    data_setup_collapse,  
    
    html.Br(),
    
    dbc.Row([
            
            html.Br(),
            
            dbc.Col([
                html.Div([
            
                        html.H5('Data Setup', className='headings',), 
                        html.Hr(style={'borderWidth': "50vh", "width": "100%", "borderColor": 'black',"opacity": "unset"}),
                        html.H6('Select Year Range For Analysis:', style={'font-family': 'Calibri Light'}), 
                        dcc.RangeSlider(id='data-setup-range-slider',
                                        marks = {
                                        2000: '2000',
                                        2005: '2005',
                                        2010: '2010',
                                        2015: '2015',
                                        2020: '2020'
                                        },
                                        min=2000,
                                        max=2020,
                                        step= 1, 
                                        value=[2000, 2020],
                                        dots = True,
                        ),
                    
                        html.Br(),

                        html.H6('Select Continents:', style={'font-family': 'Calibri Light'}),

                        dcc.Dropdown(id='data-continents-select-dropdown',
                                     className='dropdown',
                                     options=[{'label': continent, 
                                               'value': continent} for continent in ['Africa', 'Asia', 'Australia', 
                                                                             'Europe','N. America', 'S. America']],
                                     multi=True,
                                     value=['Africa', 'Europe']
                        ),
                        
                        html.Br(),

                        dbc.Button('Submit', 
                                   id='submit-data-range-button', 
                                   n_clicks=0, outline=True, 
                                   color='primary',
                                   className='button',
                                    style={'display': 'block', 'margin': 'auto'}
                                  
                                  ),

                ], style={"border": "0px ridge silver", # different border styles: double, solid, dashed, groove, outset, ridge, inset
                          'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                          "padding": "10px"} # Add padding for spacing}
                ),
            
            ], lg={'size':3, 'offset':0}, sm=12, className='text-left'),
            
            dbc.Col([
                  html.Div([
                      dcc.Dropdown(id='data-chart-variable-dropdown',
                                  options=[],  # Initial empty options
                                  multi=False,
                                  value=[],  # Initial empty value
                            ),                  
                      dcc.Loading(
                          dcc.Graph(id="animated-data-chart"), 
                          type="cube"), 
                  ], style={"border": "0px ridge silver",  # 2px border with black color
                            'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                            "padding": "10px", 'background-color':'#E5ECF6' } # Add padding for spacing}
                  ),
                
            ], lg={'size':7, 'offset':0}, sm=12),
               
        ], justify='center', className='g-10'),
        
        dcc.Store(id="stored-data", storage_type="local", data={}),  # store updated data from user
        
    ], className="content") # Use the "content" class from css for styling 


# In[ ]:





# ##### 3.3 layout for cluster analysis section

# In[11]:


# collapse button for cluster analysis section

cluster_analysis_collapse = html.Div(
    [
        dbc.Button(
            "Cluster Analysis",
            id="cluster-analysis-collapse-button",
            className="button-collapse",
            color="primary",
            n_clicks=0,
            style={"margin-left": "5px"}, # Add a margin to the left
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown("""
                    - Perform clustering of countries based on selected indicators
                    - Select range of years for clustering
                    - Visualize countries clustered based on indicators selected.
                    """)
                )
            ),
            id="cluster-analysis-collapse",
            is_open=False,
        ),
    ],
     style={
        "border-top": "5px inset blue", # different border styles: double, solid, dashed, groove, outset, ridge, inset
        'box-shadow': '0px 0px 0px 0px rgba(0, 0, 0, 0.2)',
        "padding": "10px",
    }
)


# In[12]:


# cluster analysis content 
   
cluster_section = html.Div([
 
      ########################################## CLUSTER SECTION ############################################
       dbc.Row([
           
           dbc.Col([
               
               html.Div([
                   
                   html.H5('Cluster setup:', className='headings',),
                   
                   html.H6('Select indicators for clustering (max 5):'),
                   
                   dcc.Dropdown(id='cluster-indicators-dropdown',
                                 options=[{'label': indicator, 'value': indicator} for indicator in DF['Series Name'].unique()],
                                 multi=True,
                                 className='dropdown',
                                 placeholder='Select indicators...',
                                 value = ['GDP growth (annual %)',
                                    'Unemployment, total (% of total labor force) (national estimate)'],   
                           ),
                   
                   html.Br(),
                   
                   html.H6('Select year for cluster analysis:'),
                   
                   dbc.Row([
                       html.H6('Cluster year:'),
                       dcc.Dropdown(id='cluster-indicators-year-dropdown',
                                 options = [],
                                 multi=False,
                                 className='dropdown',
                                 placeholder='Select year...',
                                 value=None,  # Make sure the value property is set to None
                               ),
                   ]),
                   
                   html.Br(),
                   
                   html.H6('Select no of clusters:'),
                   
                   dcc.Slider(1, 10, 1, 
                      value=5, 
                      marks=None,
                      id = 'cluster-number-slider',
                      tooltip={"placement": "bottom", "always_visible": True}),
                   
                   dbc.Button('Submit', 
                                  id='submit-cluster-settings-button', 
                                  n_clicks=0, outline=True, 
                                  color='primary',
                                  className='button',
                                   style={'display': 'block', 'margin': 'auto'}
                                 ),               
               
                   
               ], style={"border": "0px ridge silver",  # 2px border with black color
                         'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                         "padding": "10px"  }# Add padding for spacing}
               ),
               
           ], lg={'size':3, 'offset':0}, sm=12, className='text-left'),
           
           dbc.Col([
               
               html.Div([
                   
                   dcc.Loading(
                         dcc.Graph(id='cluster-chart'), 
                         type="cube"),
  
               ], style={"border": "0px ridge silver", # 2px border with black color
                         'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                         "padding": "10px", 'background-color':'#E5ECF6'} # Add padding for spacing}
               ),
               
               html.Br(),
               
               html.Br(),
               
               html.Div([
                   
                   html.H5('Explore clusters'),
                   
                   html.H6('Select cluster group:'),
                   
                   # derives from output of cluster analysis callback
                   dcc.Dropdown(id='cluster-group-dropdown',
                                 options=[],  # Initial empty options
                                 multi=False,
                                 value=[],  # Initial empty value
                           ),
                   
                   html.Br(),
                   
                   dbc.Row([
                       
                       dbc.Col([                           
                           # derives from main data (not cluster data where they appear in columns instead of rows!)
                           dcc.Dropdown(id='cluster-group-indicator-dropdown',
                             options=[],  # Initial empty options
                             multi=False,
                             value=[],  # Initial empty value
                           ),  
                       ]),
                       
                       dbc.Col([
                            dcc.Dropdown(id='cluster-group-year-dropdown',
                             options=[],  # Initial empty options
                             multi=False,
                             value=None,  # Make sure the value property is set to None
                             placeholder='Select year...', 
                           ),    
                       ]),
                   ]),
                   
                   html.Br(),
                   
                   dcc.Loading(
                        html.Div(id='datatable-container'),
                        type="cube"
                   ),
                   
                   dbc.Button('Download',
                              id='download-cluster-analysis-button', 
                              n_clicks=0, outline=True, 
                              color='primary',
                              className='button',
                              style={'display': 'block', 
                                     'margin': 'auto', 
                                     'width': '155px', 
                                     'position': 'relative', 
                                     'bottom': 0, 'right': 0}
                   ),
           
                   
               ], style={"border": "0px ridge white",  # 2px border with black color
                         'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                         "padding": "10px", 'background-color':'#E5ECF6' } # Add padding for spacing}
               ),    
               
           ], lg={'size':7, 'offset':0}, sm=12),
           
       ], justify='center', className='g-10'),
       
       
       dcc.Store(id="stored-cluster-data", storage_type="local", data={}),  # store updated data from user
       
       dcc.Download(id='download-cluster-dataset-component'), # download cluster analysis data set
         
   ], className="content")  # Use the "content" class from css for styling


# In[ ]:





# ##### 3.4 layout for peer analysis section

# In[13]:


# collapse button for peer analysis section

peer_analysis_collapse = html.Div(
    [
        dbc.Button(
            "Peer Analysis",
            id="peer-analysis-collapse-button",
            className="button-collapse",
            color="primary",
            n_clicks=0,
            style={"margin-left": "5px"},  # Add a margin to the left
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown("""
                    Perform a peer comparison using either cluster groupings derived in section above or selecting own benchmark
                    - Select country of focus and benchmark
                    - Select amongst various indicators available 
                    - Visualize peers selected on a map
                    """)
                )
            ),
            id="peer-analysis-collapse",
            is_open=False,
        ),
    ],
     style={
        "border-top": "5px inset blue", # different border styles: double, solid, dashed, groove, outset, ridge, inset
        'box-shadow': '0px 0px 0px 0px rgba(0, 0, 0, 0.2)',
        "padding": "10px",
    }
)


# In[14]:


# peer analysis content    

peer_analysis_section =  html.Div([
     
       ########################################## PEER ANALYSIS SECTION ############################################
        
        dbc.Row([
            
              dbc.Col([
                html.Div([
                    
                        html.H5('Peer Analysis', className='headings',), 
                        html.Hr(style={'borderWidth': "50vh", "width": "100%", "borderColor": 'black',"opacity": "unset"}),
                        html.H6('Select Country in Focus:'), 
                    
                        dcc.Dropdown(id ='country-focus-peer-analysis-dropdown',
                                     options=[],  # Initial empty options
                                     value=[],  # Initial empty value
                                     multi=False,
                                     className='dropdown',
                                     
                        ),
                    
                        html.Br(),

                        html.H6('Select Benchmark:'),
                    
                        dbc.RadioItems(id="benchmark-selected-radio",
                            options=[
                                {"label": "Select Cluster Group Countries", "value": 'cluster-benchmark'},
                                {"label": "Select Custom Countries", "value": 'custom-benchmark'},
                            ],
                            value='cluster-benchmark',
                            style={'font-family': "Calibri Light, sans-serif"}, 
                           
                        ),

                        dcc.Dropdown(id = 'custom-benchmark-dropdown',
                                     options=[],
                                     multi=True,
                                     disabled=False,  # Set the initial state
                                     className='dropdown',
                        ),
                        
                        html.Br(),

                        dbc.Button('Submit', 
                                   id='peer-settings-submit-button', 
                                   n_clicks=0, outline=True, 
                                   color='primary',
                                   className='button',
                                    style={'display': 'block', 'margin': 'auto'}
                                  
                                  ),
                    
                ], style={"border": "0px ridge acqua",  # 2px border with black color double, solid, dashed
                          'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                          "padding": "10px"  } # Add padding for spacing}
                ),
                  
            ], lg={'size':3, 'offset':0}, sm=12, className='text-left'),
            
            dbc.Col([
                  html.Div([
                      
                      html.H6('Select indicator'),
                      
                      dcc.Dropdown(id = 'peer-comparison-indicator-dropdown',
                                   multi=False,
                                   value ='GDP (current US$)',
                                   options=[],
                                   className='dropdown',
                                  ),                  
                
                      dcc.Loading(
                                dcc.Graph(id='peer-comparison-chart'), 
                                type="cube"), 
                         
                      
                      html.H6('Select Graph Type'),

                      dcc.Dropdown(
                            id='peer-analysis-graph-type-dropdown',
                            options=[
                                {'label': 'Line Chart', 'value': 'line'},
                                {'label': 'Heatmap', 'value': 'heat'},
                            ],
                            multi=False,
                            value='line',
                            className='dropdown',
                            style={'width': '155px', 'margin-top': '10px', 'font-family': "Calibri Light, sans-serif"},  # Adjust width and margin as needed
                        ),
                           
                  ], style={"border": "0px ridge mustard",  # 2px border with black color #groove
                            'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                          "padding": "10px", 'background-color':'#E5ECF6' } # Add padding for spacing}
                  ),
                
                html.Br(),
                
                html.Br(),
                
                html.Div([
                    
                    html.H6('Peer geographic location'),
                        
                    dcc.Loading(
                        dcc.Graph(id='peer-analysis-location-chart'), 
                         type="cube"),
                    
                    
                ], style={"border": "0px ridge white",  # 2px border with black color
                          'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                          "padding": "10px", 'background-color':'#E5ECF6'} # Add padding for spacing}
                ),
                    
            ], lg={'size':7, 'offset':0}, sm=12),
                       
        ], justify='center', className='g-10'),
        
        html.Div(id='hidden-trigger', style={'display': 'none'}),  # Hidden div to act as an input -- temporary
        
        dcc.Store(id="stored-peer-analysis-data", storage_type="local", data={}),  # store updated data from user
        
    ], className="content")


# In[ ]:





# ##### 3.5 layout for info section

# In[15]:


# Define the content for each info tab

# tab 1: key info tab
tab1_content = dbc.Card(
    dbc.CardBody([
            html.Ul([
                                
                html.Li('Number of Economies: 195'),
                html.Li('Temporal Coverage: 2000 - 2020'),
                html.Li('Update Frequency: Yearly'),
                html.Li('Source: World Bank Data'),
                html.Li('Database: World Development Indicators'),
                html.Li(['Link: ',
                   html.A('https://databank.worldbank.org/source/world-development-indicators/',
                         href='https://databank.worldbank.org/source/world-development-indicators/',
                         target="_blank", ),
                ]),
            ])
    ],style={"border": "0px ridge silver",  # outset, groove
             'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
             'background':'light grey',
             "padding": "10px"  } # Add padding for spacing}
    ),
    className="m-4 text-left border-0 bg-transparent", 
)

# tab 3: author info tab

tab3_content = dbc.Card( 
    
    dbc.CardBody([
        
        dbc.Row([
            
                dbc.Button(id='download-cv-button', 
                           n_clicks=0, outline=True, 
                           children = [html.I(className="fa fa-cloud-download mr-1"), "Download CV"],
                           color='primary',
                           className='button',
                           style={'width': '140px', 'margin-left': 'auto'}
                    ),
                
            ], justify='end', className='mt-1'),
            
            dbc.Row([
                dbc.Col([
                    html.I(className="bi bi-linkedin me-2 text-primary text-center"),
                    html.A("Elom Kwamin, FRM", 
                           href="http://linkedin.com/in/elom-tettey-kwamin-frm®-53029468",
                           target="_blank", 
                           style={'text-decoration':'none'},
                          ),
                ],className='text-center'),
            ]),
            
            html.Br(),
        
            
            
            dbc.Row([
                
                dbc.Col([
                dbc.CardImg(src="assets/passport_pic.jpeg", className='rounded-center"', 
                            style={"maxWidth": 180, "opacity": 0.8,},), 
                ],lg={'size':2, 'offset':1}, sm=12, className='text-left'),
                
                dbc.Col([
                
                html.A('I am a results-oriented finance analyst holding a dual Master degrees in Quantitative Finance '), 
                html.A('and Quantitative Economics from the University of Kiel.'),
                html.A(' I hold the esteemed FRM designation and have a strong passion for data analysis and machine learning.'),
                html.A(' I am adept at harnessing the power of data analysis and machine learning to drive informed decisions'),
                html.A(' and deliver exceptional outcomes.'),
                ], lg={'size':8, 'offset':0}, sm=12, className='text-left'),    

            ],justify='center'),
            
            
            html.Br(),
            html.Br(),
            
            html.I(className="bi bi-building  me-2 text-primary text-center"),
            html.A('Work Experience'),
        
            html.Hr(),
            html.Ul([           
                html.Li('June 2022 - Current: Specialist, Structured Finance - Scope Ratings GmbH'),
                html.Li('Dec 2020 - May 2022: Associate Analyst, Structured Finance - Scope Ratings GmbH'),
                html.Li('Mar 2018 - Apr 2019: Quantitative Analyst - TTMzero'),
            ]),
            
            html.Br(),
            html.Br(),
        
            html.I(className="bi bi-book me-2 text-primary text-center"),
            html.A('Education'),
        
            html.Hr(),
            html.Ul([           
                html.Li('2015 - 2017: MSc. Quantitative Economics, University of Kiel'),
                html.Li('2013 - 2016: MSc. Quantitative Finance, University of Kiel'),
                html.Li('2008 - 2012: BSc. Actuarial Science, Kwame Nkrumah University of Science & Technology'),
            ]),
            
            html.Br(),
            html.Br(),
        
   
            html.I(className="bi bi-tools me-2 text-primary text-center"),
            html.A('Skills', style={'font':'bold'}),
          
        
            html.Hr(),
            html.Ul([
                html.Li('Machine Learning'),
                html.Li('Data analysis & analytics'),
                html.Li('VBA'),
                html.Li('Tool development in Python'),
            ]),
              
        ],style={"border": "0px ridge silver",  # outset, groove
                  'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                  "padding": "10px"  } # Add padding for spacing}
    ),
    className="mt-4 w-80 border-0 bg-transparent",
)


# In[16]:


# tab 2: project info tab

tab2_content = dbc.Card(
    dbc.CardBody([
        
    html.Div([
        dcc.Markdown('''
            #### **App Overview**
            ''', style={'text-align': 'center', 
                        'font-size': '18px', 
                        'font-family': 'Calibri Light',
                        'padding': '15px',
                        'border-bottom': '2px ridge #007BFF'}),
    ]),
        
    dcc.Markdown('''
            Welcome to the Macro Data Explorer Web App! This interactive web application allows you to explore, analyze, and visualize data from the World Bank. This app provides a user-friendly interface for gaining valuable insights from raw data.
            
            ''', style={'font-family': 'Calibri Light', 'line-height': '1.6', 'margin': '20px', 'fontSize': '14px'}),    
    
    dcc.Markdown('''
            ##### **1. Data Setup**

            ###### 1.1 Selecting Options

            In the **Data Setup** section, you have the ability to filter preprocessed World Bank data according to your preferences:

            - Choose a specific year range.
            - Filter data by continents.
            - View time series visualizations across different indicators.

            ###### 1.2 Visualizing Data

            Explore and understand the dataset better with dynamic time series visualization. 
            Select indicators to gain deeper insights into global trends.

            ##### **2. Clustering Analysis**

            ###### 2.1 Customized Indicators

            Move on to the **Clustering Analysis** section to dive deeper into the data:

            - Cluster the filtered data based on your customized indicators.
            - Select a specific year period for analysis.

            ###### 2.2 Visual Results

            Witness the results through a choropleth map indicating cluster groups. A downloadable table is also provided for in-depth analysis.

            ##### **3. Peer Analysis**

            ###### 3.1 Performance Comparison

            The **Peer Analysis** section allows you to compare the performance of jurisdictions:

            - Select peer clusters for comparison.
            - Choose custom benchmark countries to compare time series data.

            ###### 3.2 Visualizations

            The web app generates comprehensive visualizations of selected peers:

            - Time series charts for easy trend analysis.
            - Choropleth maps to visually compare performance across regions.
            

            ##### **How to Use**

            1. Navigate through the three sections.
            2. In each section, follow the intuitive user interface to make selections and view visualizations.
            3. Download tables and charts for further analysis.

            *This web app transforms raw World Bank data into a user-friendly and insightful tool showcasing the power of python and dash
            as a tool for gaining actionable insights from complex datasets, making you a valuable asset in data-driven decision-making.*
            
    ''', style={'font-family': 'Calibri Light', 'line-height': '1.6', 'margin': '20px', 'fontSize': '15px', 'border-bottom': '2px solid #007BFF'}),
                
        
    ],style={"border": "0px ridge silver", # outset, groove
             'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
             'background':'light grey',
             "padding": "10px"  } # Add padding for spacing}
    ),
    className="m-4 text-left border-0 bg-transparent", 
)

# Create the tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Key Info", className="mt-10", activeTabClassName="fw-bold fst-italic"),
        dbc.Tab(tab2_content, label="Project Info", activeTabClassName="fw-bold fst-italic"),
        dbc.Tab(tab3_content, label="Author Info", activeTabClassName="fw-bold fst-italic"), 
    ]
)


# In[17]:


info_section = html.Div([
       
    dbc.Row([
        
        dbc.Col([tabs], lg={'size':8, 'offset':2}, sm=12),
        
    ]),
    
    dcc.Download(id='download-cv-component'),
      
])


# In[18]:


# Create footer with a fixed footer style

footer_section = dbc.Row([
    # YouTube
    dbc.Col([
        html.Div(de.Lottie(options=lotties_options, width="9%", height="9%", url=youtube_lottie_url)),
        html.I(className="bi bi-youtube me-1 text-danger text-center"),
        html.A('Data with Elom', 
               href="https://www.youtube.com/@DatawithElom", 
               target="_blank",
               style={'font':'bold', 'text-decoration':'none', 'color': 'white'},
               className="mb-5"
        ),
    ], className='text-center'),
    
    # Instagram
    dbc.Col([
        html.Div(de.Lottie(options=lotties_options, width="9%", height="9%", url=instagram_lottie_url)),
        html.I(className="bi bi-instagram me-1 text-danger text-center"),
        html.A('data.with.elom', 
               href="http://instagram.com/data.with.elom",
               target="_blank", 
               style={'font':'bold', 'text-decoration':'none', 'color': 'white'},
               className="mb-5" #"me-1"
        ),
    ], className='text-center'),
    
#     # Gmail
#     dbc.Col([
#         html.Div(de.Lottie(options=lotties_options, width="8%", height="8%", url=gmail_lottie_url)),
#         html.I(className="bi bi-envelope-fill me-2 text-danger text-center"),
#         html.A('contact: data.with.elom@gmail.com', 
#                style={'font':'bold', 'text-decoration':'none', 'color': 'white'},
#                className="mb-5" #"me-2",
#         ),     
#     ], className='text-center'),
    
    # LinkedIn
    dbc.Col([
        html.Div(de.Lottie(options=lotties_options, width="8%", height="8%", url=linkedin_lottie_url)),
        html.I(className="bi bi-linkedin me-2 text-primary text-center"),
        html.A("Elom Kwamin, FRM", 
               href="http://linkedin.com/in/elom-tettey-kwamin-frm®-53029468",
               target="_blank", 
               style={'text-decoration':'none', 'color': 'white'},
               className="mb-5",
              ),
    ],className='text-center'),

], className="footer justify-content-center",
   style={'width': '101%', 'background-color': '#6495ED', 'height': '100px',
          'display': 'flex', 'align-items': 'center', 'position': 'absolute', 'bottom': 0,
          "border": "4px ridge black", 'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0)', "padding": "3px"})


# In[ ]:





# ##### 3.6 final layout

# In[19]:


app.layout = html.Div([ 
    
    html.Div([
    
    header_section,
    
    html.Br(),
    
    html.Br(),
    
    html.Br(),
    
    html.Br(),
    
    data_setup_section,
    
    html.Br(),
    
    html.Br(),
    
    html.Br(),
    
    cluster_analysis_collapse,
    
    cluster_section,
    
    html.Br(),
    
    html.Br(),
    
    html.Br(),
    
    peer_analysis_collapse,
    
    peer_analysis_section,
    
    html.Br(),
    
    html.Br(), 
    
    html.Br(),
    
    html.Br(),
        
    info_section,
        
    html.Br(),
        
    html.Br(),
        
    html.Br(),
        
    html.Br(),
        
    html.Br(),
        
    ]),
    
    footer_section

], style={"position": "relative", "min-height": "100vh"} ) #, fluid=True,)


# In[ ]:





# In[ ]:





# ### step 4: callbacks 

# ##### 4.1 callbacks for data setup section

# In[20]:


@app.callback(
    Output("data-setup-collapse", "is_open"),
    [Input("data-setup-collapse-button", "n_clicks")],
    [State("data-setup-collapse", "is_open")],
)
def toggle_data_setup_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# In[21]:


# function used in creating dataframe from selected indicator
def create_data_frame_from_indicator(data_frame, indicator):
    df = data_frame[data_frame["Series Name"]==indicator]
    df.rename(columns={'year':'Year', 'value':indicator, 'Country Name':'Country'}, inplace=True)    
    return df


# In[22]:


# callback for updating data for user session
@app.callback(
    Output("stored-data", "data"),
    Input("submit-data-range-button", "n_clicks"),
    State("data-setup-range-slider", "value"),
    State("data-continents-select-dropdown", "value"),
)

def update_data(n_clicks, data_range_selected, continents_chosen):
    
    main_df = DF.copy()
    
    if n_clicks is None:
        return main_df.to_dict('records')
    
    else:
        start_year, end_year = data_range_selected
        
        # Filter the DataFrame based on the selected year range
        range_updated_dataframe = main_df[main_df['year'].between(start_year, end_year)]
        
        # Filter the DataFrame based on the selected continents
        if len(continents_chosen) == 0:
            
            return range_updated_dataframe.to_dict('records') # if no continents are specied, all are selected by default
        
        continents_updated_dataframe = range_updated_dataframe[range_updated_dataframe["Continent"].isin(continents_chosen)]
        
        return continents_updated_dataframe.to_dict('records')


# In[23]:


# callback for updating dropdown menu for data setup indicators
@app.callback(
    Output('data-chart-variable-dropdown', 'options'),
    Output('data-chart-variable-dropdown', 'value'),
    Input("stored-data", "data"),
)
def update_dropdown_options(stored_data):
    if stored_data is not None:
        # Convert stored data to a DataFrame
        df = pd.DataFrame(stored_data)

        # Get all unique entries from the 'label' column
        unique_labels = df['Series Name'].unique()

        # Create options for the Dropdown
        options = [{'label': label, 'value': label} for label in unique_labels]

        # Set initial selected value if needed
        initial_value = "Population, total" 

        return options, initial_value 
    else:
        return [], []


# In[24]:


# callback for updating data setup explore chart
@app.callback(
    Output('animated-data-chart', 'figure'),
    Input('animated-data-chart', 'relayoutData'),
    Input("stored-data", "data"),
    Input("data-chart-variable-dropdown", "value"),
)

def update_data_graph(relayout_data, stored_data, selected_variable):
    
    if stored_data is not None:
        # Convert stored data to a DataFrame
        macro_df = pd.DataFrame(stored_data)
        
    df_long = create_data_frame_from_indicator(macro_df, selected_variable)
        
    # Initial filtering to include only the top 20 countries
    df_initial = df_long.groupby('Year').apply(lambda group: group.nlargest(20, selected_variable)).reset_index(drop=True)
    
    # Sort DataFrame based on the current animation frame
    if 'xaxis.range[0]' in relayout_data:
        print('im after initial plot')
        start_year = int(relayout_data['xaxis.range[0]'])
        end_year = int(relayout_data['xaxis.range[1]'])
        df_filtered = df_long[df_long['Year'].between(start_year, end_year)]
        df_sorted = df_filtered.groupby('Country')[selected_variable].max().sort_values(ascending=False).index
        df_filtered['Country'] = pd.Categorical(df_filtered['Country'], categories=df_sorted, ordered=True)
        
        # Keep only the top 20 countries for each year
        dff = df_filtered.groupby('Year').apply(lambda group: group.nlargest(20, selected_variable)).reset_index(drop=True)
        
        # Stick to a list of the top 20 countries
        countries_to_keep = dff['Country'].unique()[:20]
        dff = dff[dff['Country'].isin(countries_to_keep)]
        
        fig = px.bar(dff, x=selected_variable, y='Country', color='Country', animation_frame='Year',
                     labels={selected_variable: selected_variable, 'Country': 'Country', 'Year': 'Year'},
                     height=850,
                     title=f'{selected_variable} over time by country - top 20')
        
        fig.layout.geo.bgcolor = '#E5ECF6'
        
        # Update y-axis based on the current top 20 countries
        fig.update_layout(yaxis=dict(categoryorder='total descending', categoryarray=countries_to_keep[::-1]))
        
        # Update x-axis range based on the maximum variable
        max_value = df_filtered[selected_variable].max()
        fig.update_xaxes(range=[0, max_value])
        
        # Set animation duration
        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                            method='animate', args=[None, dict(frame=dict(duration=1200, redraw=True),
                                                              fromcurrent=True)]),
                                                            dict(label='Pause',
                            method='animate', args=[[None], dict(frame=dict(duration=0, redraw=True),
                                                               mode='immediate')],
                            )])])
        
        # Add annotations for source and copyright
        fig.update_layout(
            annotations=[
                dict(
                        xref="paper", yref="paper",
                        x=1, y=-0.05,
                        xanchor="right", yanchor="bottom",
                        text="Source: World Bank Data",
                        showarrow=False,
                        font=dict(size=10)
                    ),
#                 dict(
#                     xref="paper", yref="paper",
#                     x=0.5, y=-0.15,
#                     xanchor="center", yanchor="bottom",
#                     text="Copyright © 2023 data-with-elom",
#                     showarrow=False,
#                     font=dict(size=10)
#                 )
            ]
        )
        return fig
    
    else:
                
        fig = px.bar(df_initial, x=selected_variable, y='Country', color='Country', animation_frame='Year',
                     labels={selected_variable: selected_variable, 'Country': 'Country', 'Year': 'Year'},
                     height=850,
                     title=f'{selected_variable} over time by country - top 20')
        
        # Set initial y-axis based on the initial top 20 countries
        fig.update_layout(yaxis=dict(categoryorder='total descending', categoryarray=df_initial['Country'].unique()[:20][::-1]))
        
        fig.layout.geo.bgcolor = '#E5ECF6'
        
        # Set initial x-axis range
        max_value_initial = df_initial[selected_variable].max()
        fig.update_xaxes(range=[0, max_value_initial])
        
        # Set initial animation duration
        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                            method='animate', args=[None, dict(frame=dict(duration=1200, redraw=True),
                                                              fromcurrent=True)]),
                                                            dict(label='Pause',
                            method='animate', args=[[None], dict(frame=dict(duration=0, redraw=True),
                                                               mode='immediate')],
                            )])])
        
        # Add annotations for source and copyright
        fig.update_layout(
            annotations=[
                    dict(
                        xref="paper", yref="paper",
                        x=1, y=-0.05,
                        xanchor="right", yanchor="bottom",
                        text="Source: World Bank Data",
                        showarrow=False,
                        font=dict(size=10)
                    ),
            ]
        )
        return fig


# In[ ]:





# ##### 4.2 callbacks for cluster analysis section

# In[25]:


@app.callback(
    Output("cluster-analysis-collapse", "is_open"),
    [Input("cluster-analysis-collapse-button", "n_clicks")],
    [State("cluster-analysis-collapse", "is_open")],
)
def toggle_cluster_analysis_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# In[26]:


def convert_to_group_name(num):
    return f'Group {num}'


# In[27]:


# callback for updating cluster chart
@app.callback(
    Output('cluster-chart', 'figure'),
    Output('cluster-group-dropdown', 'options'),
    Output('cluster-group-dropdown', 'value'),
    Output('cluster-group-indicator-dropdown', 'options'),
    Output('cluster-group-indicator-dropdown', 'value'),
    Output("stored-cluster-data", "data"),
    Input('submit-cluster-settings-button', 'n_clicks'),
    State("stored-data", "data"), 
    State("cluster-indicators-dropdown", "value"),
    State("cluster-indicators-year-dropdown", "value"),
    State("cluster-number-slider", "value"),
)
    
def update_cluster_graph(n_clicks, stored_data, indicators, 
                         cluster_year, n_clusters):
    
    if not n_clicks:
        raise PreventUpdate 
        
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    scaler = StandardScaler()
    kmeans = KMeans(n_clusters=n_clusters)

    # transform data frame
    data_frame = pd.DataFrame(stored_data).copy()

    # extract indicators to be used as dropdown in cluster table
    indicators_list = data_frame['Series Name'].tolist()
    indicators_options = [{'label': label, 'value': label} for label in indicators_list]
    indicator_value = indicators[0] # active indicator for table


    df_transformed = data_frame.pivot_table(index=['Country Name', 'Country Code', 'year', 'Capital','Continent'],
                                          columns='Series Name', values='value', aggfunc='first').reset_index()   
    
    # filter data between two dates provided
    filtered_df = df_transformed.loc[(df_transformed['year'] == cluster_year)]

    # impute missing values with the mean of each column
    filtered_df[indicators] = imp.fit_transform(filtered_df[indicators])

    data_no_na = filtered_df[indicators] 

    # scale DataFrame
    scaled_data = scaler.fit_transform(data_no_na)

    # use k-means clustering on the imputed DataFrame
    df_clusters = filtered_df.copy()
    df_clusters['Cluster'] = kmeans.fit_predict(scaled_data).astype(int) # kmeans.fit(scaled_data)

    # sort dataframe by group assignment
    df_clusters.sort_values(by='Cluster', ascending=True, inplace=True)

    # rename group
    df_clusters['Cluster'] = df_clusters['Cluster'].apply(convert_to_group_name)

    fig = px.choropleth(df_clusters,
                  locations='Country Name',
                  locationmode='country names',
                  color='Cluster', 
                  labels={'color': 'Cluster'},
                  hover_data=indicators,
                  height=700,
                  title=f'Country cluster period - {cluster_year}. Number of clusters: {n_clusters}<br>Inertia: {kmeans.inertia_:,.2f}',
                  color_discrete_sequence=px.colors.qualitative.T10)

    # Add annotations for indicators selected for clustering
    fig.add_annotation(x=0.5, y=-0.15, 
                       xref='paper', yref='paper',
                       text='Selected Cluster Indicators:<br>' + "<br>".join(indicators), 
                       showarrow=False)
    
#     # Add annotations for source and copyright
#     fig.update_layout(
#         annotations=[
#                 dict(
#                     xref="paper", yref="paper",
#                     x=1, y=-0.05,
#                     xanchor="right", yanchor="bottom",
#                     text="Source: World Bank Data",
#                     showarrow=False,
#                     font=dict(size=10)
#                 ),
#         ]
#     )

    fig.layout.geo.showframe = False
    fig.layout.geo.showcountries = True
    fig.layout.geo.projection.type = 'robinson' #'winkel tripel' 'mercator'  'equirectangular' , 'natural earth', 'hammer'
                
#     fig.update_layout(margin=dict(l=10, r=10, t=30, b=60))  # Update margins
#     fig.layout.geo.aspectmode = 'auto' 
    fig.layout.geo.lataxis.range = [-90, 90] #[-53, 76]
    fig.layout.geo.lonaxis.range = [-180, 180] #[-137, 168]
    fig.layout.geo.landcolor = 'white'
    fig.layout.geo.bgcolor = '#E5ECF6' ##F2F2F2

    fig.layout.paper_bgcolor = '#E5ECF6' #'#F2F2F2'
    fig.layout.geo.countrycolor = 'gray'
    fig.layout.geo.coastlinecolor = 'gray'

    # Get all unique entries from the 'label' column
    unique_clusters = df_clusters['Cluster'].unique()

    # Create options for the exploring cluster groups Dropdown
    options = [{'label': label, 'value': label} for label in unique_clusters]

    # Set initial selected value if needed
    initial_value = unique_clusters[0]

    merge_cols = ['Country Name', 'Country Code', 'Capital', 'Continent']
    df_clusters = df_clusters[['Country Name', 'Country Code', 'Capital', 'Continent', 'Cluster']]
    cluster_data = df_transformed.merge(df_clusters, left_on = merge_cols, right_on = merge_cols)            

    return fig, options, initial_value, indicators_options, indicator_value, cluster_data.to_dict('records')


# In[28]:


# callback to populate year dropdown menu in cluster analysis section

@app.callback(
    Output('cluster-indicators-year-dropdown', 'options'), # in cluster settings setup field
    Output('cluster-indicators-year-dropdown', 'value'), # in cluster settings setup field
    Output('cluster-group-year-dropdown', 'options'), # in explore table
    Input("data-setup-range-slider", "value"), # in explore table
)

def update_explore_cluster_year_dropdown(data_range_selected):
    # this is obtained from the slider range from the data setup section
    start_year, end_year = data_range_selected
    
    start_year = int(start_year)
    
    end_year = int(end_year)
    
    years_list_options = list(range(start_year, end_year + 1, 1))
    
    return years_list_options, start_year, years_list_options


# In[29]:


# callback for updating explore table

@app.callback(
    Output('datatable-container', 'children'),
    Output('stored-peer-analysis-data', 'data'), # merged cluster and original data
    State("stored-data", "data"),
    Input('cluster-group-dropdown', 'value'),
    Input('cluster-group-indicator-dropdown', 'value'),
    Input('stored-cluster-data', 'data'),
    Input('cluster-group-year-dropdown', 'value'),
)

def update_explore_cluster_table(stored_data, cluster_group, selected_table_indicator, stored_cluster_data, selected_year):
    # transform data frame
    data_frame = pd.DataFrame(stored_data).copy() # original data source
    
    df_stored_cluster = pd.DataFrame(stored_cluster_data)
    
    data_frame = data_frame[data_frame['Series Name']==selected_table_indicator]
    
    df_transformed = data_frame.pivot_table(index=['Country Name', 'Country Code', 'year', 'Capital','Continent'],
                                              columns='Series Name', values='value', aggfunc='first').reset_index()   
    
    merge_columns = ['Country Name', 'year']
    df_updated = df_transformed.merge(df_stored_cluster, how='left', 
                                      left_on=merge_columns, right_on=merge_columns, suffixes=('', '_right'))
    
    # Drop columns ending with '_right'
    columns_to_drop = [col for col in df_updated.columns if col.endswith('_right')]
    df_updated = df_updated.drop(columns=columns_to_drop)
    
    df_filter= df_updated[df_updated['Cluster'] == cluster_group]
    
    if selected_year is not None:
        df_filter = df_filter[df_filter['year']==selected_year]
    
    # Format 'value' column to one decimal place
    df_filter[selected_table_indicator] = df_filter[selected_table_indicator].round(1)
    df_filter = df_filter[['Country Name', 'year', 'Cluster', 'Capital', 'Continent', selected_table_indicator]]
    
    table_layout = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == "Country Name" or i == "year" 
            else {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in df_filter.columns
        ],
        
        data=df_filter.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=10,               # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Country Name', 'Country Code']
        ],
        
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        
        style_table={
                    'overflowX': 'auto',  # Enable horizontal scrolling if needed
                    'height': '400px',    # Set the desired height of the table
                    'width': '100%',      # Set the width of the table to 100% of the container
                },
    )
    return [table_layout], df_updated.to_dict('records')


# In[30]:


# callback for downloading cluster data

@app.callback(
    Output('download-cluster-dataset-component', 'data'),
    State('stored-peer-analysis-data', 'data'),
    State("cluster-indicators-dropdown", "value"),
    Input('download-cluster-analysis-button', 'n_clicks'),
    prevent_initial_call = True,
)

def download_cluster_analysis(stored_cluster_data, slected_cluster_indicators, n_clicks):
    
    if not n_clicks:
        
        raise PreventUpdate 
        
    # Create a new data frame with selected indicators
    df_selected_indicators = pd.DataFrame({'Indicators': slected_cluster_indicators})
    
    df_final = pd.DataFrame(stored_cluster_data) # original data source
    
    dict_df_download = {'Indicators':df_selected_indicators, 'ClusterData': df_final}
    
    writer = pd.ExcelWriter("cluster_analysis_export.xlsx", engine='xlsxwriter')
    
    workbook = writer.book  
    
    for df_name , df in dict_df_download.items():
        
        df.to_excel(writer, sheet_name=df_name, index=False)
        
        worksheet = writer.sheets[df_name]

    writer.save()
            
    return dcc.send_file("cluster_analysis_export.xlsx")   


# In[ ]:





# ##### 4.3 callbacks for peer analysis section

# In[31]:


@app.callback(
    Output("peer-analysis-collapse", "is_open"),
    [Input("peer-analysis-collapse-button", "n_clicks")],
    [State("peer-analysis-collapse", "is_open")],
)
def toggle_peer_analysis_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# In[32]:


# update country focus dropdown list

@app.callback(
    Output('country-focus-peer-analysis-dropdown', 'options'),
    Input("stored-peer-analysis-data", "data"),
)

def update_country_focus_dropdown(stored_peer_data):
    
    df_stored_peer_data = pd.DataFrame(stored_peer_data)
    
    # Get all unique ectries
    country_list = df_stored_peer_data['Country Name'].unique().tolist()
    
    # Create options for the Dropdown
    options = [{'label': label, 'value': label} for label in country_list]
    
    return options


# In[33]:


# update custom benchmark multiple dropdown list

@app.callback(
    Output('custom-benchmark-dropdown', 'disabled'),
    Output('custom-benchmark-dropdown', 'options'),
    Input('benchmark-selected-radio', 'value'),
    Input('stored-peer-analysis-data', 'data')
)

def update_custom_dropdown_state(selected_radio_value, stored_peer_data):
    # Disable the dropdown if 'disable' radio button is selected, otherwise enable
    
    if selected_radio_value == "cluster-benchmark":
        return selected_radio_value == 'cluster-benchmark', []
    
    else:
        df_stored_peer_data = pd.DataFrame(stored_peer_data)
        
        # Get all unique entries from the 'label' column
        unique_countries = df_stored_peer_data['Country Name'].unique()

        # Create options for the exploring cluster groups Dropdown
        options = [{'label': label, 'value': label} for label in unique_countries]
        
        return False, options


# In[34]:


# update peer indicator

@app.callback(
    Output('peer-comparison-indicator-dropdown', 'options'),
    Input('stored-data', 'data')
)

def update_peer_indicator_list_dropdown(stored_data):

    df_stored_data = pd.DataFrame(stored_data)

    # Get all unique entries from the 'label' column
    unique_indicators = df_stored_data['Series Name'].unique()

    # Create options for the exploring cluster groups Dropdown
    options = [{'label': label, 'value': label} for label in unique_indicators]

    return options


# In[35]:


# update peer comparison chart (server-side callback)

@app.callback(
    Output('peer-comparison-chart', 'figure'),
    Input('peer-settings-submit-button', 'n_clicks'),
    State('stored-peer-analysis-data', 'data'),
    State('country-focus-peer-analysis-dropdown', 'value'),
    State('benchmark-selected-radio', 'value'),
    Input('custom-benchmark-dropdown', 'value'),
    Input('peer-comparison-indicator-dropdown', 'value'),
    Input('peer-analysis-graph-type-dropdown', 'value'),
    
    prevent_initial_call=True,  
)

def update_peer_graph (n_clicks, 
                       stored_peer_data, 
                       selected_country, 
                       selected_benchmark, 
                       selected_custom_benchmark,
                       indicator,
                       selected_graph_type):   
    if not n_clicks:
        raise PreventUpdate
        
    else:
        df = pd.DataFrame(stored_peer_data)
        
        if selected_benchmark == "cluster-benchmark":
            
            cluster_group = df[df['Country Name']==selected_country]['Cluster'].tolist()[0]
            
            cluster_countries = df[df['Cluster']==cluster_group]['Country Name'].unique().tolist()
            
            df_country_filter = df[df["Country Name"].isin(cluster_countries)]
        
        if selected_benchmark == "custom-benchmark":
            
            custom_countries = selected_custom_benchmark
            custom_countries.extend([selected_country])
            
            df_country_filter = df[df["Country Name"].isin(custom_countries)]
            
        df_filter = df_country_filter.copy()
        
        if selected_graph_type == 'line':   
        
            fig = px.line(df_filter, 
                      x='year', 
                      y=indicator, 
                      color='Country Name', 
                      line_dash='Country Name',
                      title=f'Peer comparison for {selected_country} based on {indicator}',
                      template='gridon', #plotly_dark, plotly_white, seaborn, presentation, ggplot2, gridon
                      )

            # Set mode for all traces to 'lines+markers'
            fig.update_traces(mode='lines+markers')

            # Set line_dash for the selected country
            fig.for_each_trace(lambda t: t.update(line=dict(dash='dashdot', width=2)) if t.name == selected_country else t.update(line=dict(dash='solid', width=2)))

            # Update y-axis label
            fig.update_layout(yaxis_title=indicator)

            # Update x-axis label
            fig.update_layout(xaxis_title='Year')
            
            # Update margins
#             fig.update_layout(margin=dict(l=10, r=10, t=20, b=20))
            
            fig.layout.geo.bgcolor = '#E5ECF6'
            
            fig.layout.paper_bgcolor = '#E5ECF6'
            
            return fig
        else:
        
            fig = go.Figure(data=go.Heatmap(
                x=df_filter['year'],
                y=df_filter['Country Name'],
                z=df_filter[indicator],
                colorscale='Cividis',  # Specify a color scale: Cividis, Blues, Greys, Viridis, 
                colorbar=dict(title=indicator,),
            ))
            
            fig.layout.geo.bgcolor = '#E5ECF6'
            fig.layout.paper_bgcolor = '#E5ECF6'

        fig.update_layout(title=f'Peer comparison for {selected_country} based on {indicator}')
        
        # Add annotations for source and copyright
        fig.update_layout(
            annotations=[
                    dict(
                        xref="paper", yref="paper",
                        x=1, y=-0.10,
                        xanchor="right", yanchor="bottom",
                        text="Source: World Bank Data",
                        showarrow=False,
                        font=dict(size=10)
                    ),
            ]
        )
        
        # Update y-axis label
        fig.update_layout(yaxis_title=indicator)

        # Update x-axis label
        fig.update_layout(xaxis_title='Year')
        
        # Update layout with the 'plotly_dark' template
        fig.update_layout(
            template='seaborn',  # Set the template: seaborn, plotly_dark, ggplot2, plotly
        )
        
    return fig


# In[36]:


# update peer comparison choropleth chart (server-side callback)

@app.callback(
    Output('peer-analysis-location-chart', 'figure'),
    Input('country-focus-peer-analysis-dropdown', 'value'),
    Input('benchmark-selected-radio', 'value'),
    Input('stored-peer-analysis-data', 'data'),
    Input('custom-benchmark-dropdown', 'value'),
    Input('peer-comparison-indicator-dropdown', 'value'),
)
def update_peer_choropleth_graph(selected_country, selected_radio_value, 
                                 stored_peer_data, selected_custom_benchmark, indicator):
    
    df = pd.DataFrame(stored_peer_data)

    df_filter = df.copy()
    
    cluster_group = df[df['Country Name']==selected_country]['Cluster'].tolist()[0]
            
    cluster_countries = df[df['Cluster']==cluster_group]['Country Name'].unique().tolist()
    
    # Initialize selected_countries as an empty list
    selected_countries = []
    
    if selected_radio_value == 'cluster-benchmark':
        selected_countries.extend(cluster_countries)
    else:
        selected_countries.extend(selected_custom_benchmark)
        selected_countries.extend([selected_country])
    
    # Create a column to store border width
    df_filter['border_width'] = df_filter['Country Name'].apply(lambda country: 7 if country in selected_countries else 1)

    fig = px.choropleth(
        df_filter,
        locations='Country Name',
        locationmode='country names',
        template='plotly',
        color='border_width',  # Use border_width as a color scale
        color_continuous_scale='Viridis',  # Customize the color scale
        projection='robinson',  # Set the projection type
    )

    fig.update_geos(
        bgcolor='#E5ECF6',
        showland=True,
        landcolor='white',
        subunitcolor='black',  # Color of country borders
        subunitwidth=1.5,  # Width of country borders
        showcoastlines=True,
    )

    fig.update_layout(
        coloraxis_showscale=False,  # Hide the color axis
        paper_bgcolor='#E5ECF6', # light blueish
        showlegend=False,
        title=dict(font=dict(size=28), x=0.5, xanchor='center'),

    )
    
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))  # Update margins

    return fig


# In[ ]:





# ##### 4.4 callbacks for info section

# In[37]:


# callback for downloading resume

@app.callback(
    Output('download-cv-component', 'data'),
    Input('download-cv-button', 'n_clicks'),
    prevent_initial_call = True,
)

def download_resume(n_clicks):

    return dcc.send_file('./assets/elom_kwamin_resume.pdf')


# In[ ]:





# In[ ]:





# ### step 5: run app

# In[38]:


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




