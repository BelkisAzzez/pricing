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
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'columnCount': 2}, children=[

    html.H1(
        children='Option Pricer ~~ Master 203 ~~ Yiping Gou & Valentin Descloitre & Belkis Azzez',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Label('Option Strategy'),
    dcc.RadioItems(
        id='optionStrategy',
        options=[
            {'label': 'Call', 'value': 'Call'},
            {'label': u'Put', 'value': 'Put'},
            {'label': 'Straddle', 'value': 'STRD'},  # buy put and call at same strike and maturity
            {'label': 'Strangle', 'value': 'STRN'}  # buy put and call at same maturity but different strike
        ], value='Call'
    ),

    html.Div(children='Option parameters',
             style={'textAlign': 'center',
                    'color': colors['text']
                    }),

    html.Label('S0 Current underlying spot price'),
    dcc.Input(id='spot', type='float'),

    html.Label('Call strike'),
    dcc.Input(id='callStrike', type='float'),

    html.Label('Put strike'),
    dcc.Input(id='putStrike', type='float'),

    html.Label('Risk-free interest rate (%)'),
    dcc.Input(id='rate', type='float'),

    html.Label('Volatility (%)'),
    dcc.Input(id='vol', type='float'),

    html.Div(children='Simulation parameters [Monte Carlo and Heston]',
             style={'textAlign': 'center',
                    'color': colors['text']
                    }),

    html.Label('Correlation'),
    dcc.Input(id='corr', type='float'),

    html.Label('Kappa'),
    dcc.Input(id='kappa', type='float'),

    html.Label('Theta'),
    dcc.Input(id='theta', type='float'),

    html.Label('Vol of Vol'),
    dcc.Input(id='volOfVol', type='float'),

    html.Label('Number of cores'),
    dcc.Input(id='nbCores', type='float'),

    # maturity, nbsteps, nbpaths
    html.Label('Maturity in days'),
    dcc.Slider(
        id='maturity',
        min=0,
        max=365,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 365, 30)},
        value=30,
    ),

    html.Label('Number of simulations'),
    dcc.Slider(
        id='nbSims',
        min=1000,
        max=10000,
        marks={i: '{} sims'.format(i) if i == 1 else str(i) for i in range(1000, 10000, 1000)},
        value=1200,
    ),

    html.Button('Submit', id='button'),
    html.Div(id='container-button-basic',
             children='Enter your parameters and press submit')
])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
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
     dash.dependencies.State('nbSims', 'value'),

     ])
def Output(n_clicks, valueOptionStrategy, valueSpot, valueCallStrike, valuePutStrike, valueRate, valueVol,
           valueCorr, valueKappa, valueTheta, valueVolOfVol, valueNbCores, valueMaturity, valueNbSims):
    # TODO functions calculating the price
    # TODO how to output the price
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        valueSpot,
        valueCallStrike
    )


if __name__ == '__main__':
    app.run_server(debug=True)
