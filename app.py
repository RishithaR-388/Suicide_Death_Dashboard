from dash import Dash, dcc, html, Input, Output, callback
from pages import page1, page


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    else:
        return page.layout

if __name__ == '__main__':
    app.run(debug=True)
