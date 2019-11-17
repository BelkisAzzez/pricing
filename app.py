# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# we have to install these libraries in the computer's terminal in order to make Dash work
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#021C1E',
    'text': '#7FDBFF', 'textGreen': '#6FB989', 'textDark': '#2C7873'}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'height': '500px'}, children=[

    html.H2(
        children='Option Pricer ~~ Master 203',
        style={'textAlign': 'center', 'color': colors['textDark']}
    ),

    html.H2(
        children='Yiping Gou & Valentin Descloitre & Belkis Azzez',
        style={'textAlign': 'center', 'color': colors['textDark']}
    ),

    html.Div(style={'textAlign': 'center', 'backgroundColor': colors['background'], 'columnCount': 2,
                    }, children=[
        html.H5(children='Option Strategy', style={'textAlign': 'center', 'color': colors['textDark']}),

        dcc.RadioItems(
            id='optionStrategy',
            options=[
                {'label': 'Call', 'value': 'Call'},
                {'label': u'Put', 'value': 'Put'},
                {'label': 'Straddle', 'value': 'STRD'},  # buy put and call at same strike and maturity
                {'label': 'Strangle', 'value': 'STRN'}  # buy put and call at same maturity but different strike
            ], value='Call',
            style={'columnCount': 2, 'color': colors['textGreen']}
        ),


        html.H5(children='Option parameters', style={'textAlign': 'center', 'color': colors['textDark']}),

        html.Div(style={'textAlign': 'center', 'columnCount': 2}, children=[

            html.Div(children=[
                html.Label(children='S0 Current underlying spot price', style={'color': colors['textGreen']}),
                dcc.Input(id='spot', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Call strike', style={'color': colors['textGreen']}),
                dcc.Input(id='callStrike', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Put strike', style={'color': colors['textGreen']}),
                dcc.Input(id='putStrike', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Risk-free interest rate (%)', style={'color': colors['textGreen']}),
                dcc.Input(id='rate', type='float'),
            ]),

            html.Div(children=[
                    html.Label(children='Volatility (%)', style={'color': colors['textGreen']}),
                    dcc.Input(id='vol', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Maturity in days', style={'color': colors['textGreen']}),
                dcc.Input(id='maturity', type='integer'),
            ]),
        ]),
        html.H5(children='Simulation parameters [Monte Carlo and Heston]', style={'textAlign': 'center',
                                                                                  'color': colors['textDark']}),
        html.Div(style={'textAlign': 'center', 'columnCount': 2}, children=[

            html.Div(children=[
                html.Label(children='Correlation', style={'color': colors['textGreen']}),
                dcc.Input(id='corr', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Kappa', style={'color': colors['textGreen']}),
                dcc.Input(id='kappa', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Theta', style={'color': colors['textGreen']}),
                dcc.Input(id='theta', type='float'),
            ]),

            html.Div(children=[
                html.Label(children='Vol of Vol', style={'color': colors['textGreen']}),
                dcc.Input(id='volOfVol', type='float'),
            ]),
        ]),
        html.Div(style={'textAlign': 'center', 'marginBottom': '1em'}, children=[
            html.Label(children='Number of cores', style={'color': colors['textGreen']}),
            dcc.Input(id='nbCores', type='float'),
        ]),

        html.Div(style={'textAlign': 'center', 'marginBottom': '1.5em', 'marginLeft': '1.5em', 'marginRight': '1.5em'},
                 children=[
            html.Label(children='Number of simulations', style={'color': colors['textGreen']}),
            dcc.Slider(
                id='nbSims',
                min=1000,
                max=10000,
                marks={i: '{} sims'.format(i) if i == 1 else str(i) for i in range(1000, 10000, 1000)},
                value=1200,
            ),
        ]),

        html.Button('Submit', id='button', style={'textAlign': 'center', 'marginBottom': '200px',
                                                  'background-color': '#FFFFFF'}),
        html.Div(id='container-button-basic',
                 children=[
                            html.H6(id='container-message', children=['Enter your parameters and press submit'], style={'color': colors['textGreen']}),
                            html.Div([
                                    dcc.Graph(id='graph',
                                              config={'showSendToCloud': True, 'plotlyServerURL': 'https://plot.ly'},
                                              style={'background-color': colors['background'],
                                                     'marginRight': '1.5em', 'marginTop': '1.5em'})
                            ])], style={'height': '800px'})
    ])

])


@app.callback(
    [dash.dependencies.Output('container-message', 'children'),
     dash.dependencies.Output('graph', 'figure')],
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('nbSims', 'value')],
    [dash.dependencies.State('optionStrategy', 'value'),
     dash.dependencies.State('spot', 'value'),
     dash.dependencies.State('callStrike', 'value'),
     dash.dependencies.State('putStrike', 'value'),
     dash.dependencies.State('rate', 'value'),
     dash.dependencies.State('vol', 'value'),
     dash.dependencies.State('corr', 'value'),
     dash.dependencies.State('kappa', 'value'),
     dash.dependencies.State('theta', 'value'),
     dash.dependencies.State('volOfVol', 'value'),
     dash.dependencies.State('nbCores', 'value'),
     dash.dependencies.State('maturity', 'value'),
     ])
def Output(n_clicks, valueNbSims, valueOptionStrategy, valueSpot, valueCallStrike, valuePutStrike, valueRate, valueVol,
           valueCorr, valueKappa, valueTheta, valueVolOfVol, valueNbCores, valueMaturity):

    global message
    if ((n_clicks is None) or (valueOptionStrategy is None) or (valueSpot is None) or (valueRate is None) or
            (valueVol is None) or (valueCorr is None) or (valueKappa is None) or (valueTheta is None) or
            (valueVolOfVol is None) or (valueNbCores is None) or (valueMaturity is None)):
        return 'Not enough inputs to price the option strategy' + valueNbSims
    price = 69.69 #TODO ici j'appelle la fonction qui calcule le price
    y_array_dict = {
        'P&L': [4, 2, 3],
    }
    #y_array_dict ['P&L'] = #TODO ici j'appelle la fonction qui retourne une liste de P&L en fonction du strike price
    message = 'Your option strategy price is ' + str(price)
    figure = {'data': [{'type': 'scatter', 'y': y_array_dict['P&L']}], 'layout': {'title': 'P&L of the option strategy'}}
    return message, figure


if __name__ == '__main__':
    app.run_server(debug=False)
