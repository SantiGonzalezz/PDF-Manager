from dash import Dash, dcc, Input, html, Output, State
from dash import callback
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        # Title
        html.H1('PDF Manager'),
        # Section
        html.Section(
            children=[
                html.H2('Split PDF'),
                dcc.Upload(
                    html.Button('Upload File'),
                    id='upload-image',
                ),
                html.Div('')
            ]
        ),
        # Upload
        html.Div(),
        # Download
        html.Button(
            'Download File',
            id='download-file',
        ),
        dcc.Download(),

    ]
)


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        # html.Hr(),
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


@callback(Output('output-image-upload', 'children'),
          Input('upload-image', 'contents'),
          State('upload-image', 'filename'),
          State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run(debug=True)
