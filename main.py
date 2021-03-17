
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
from dash.dependencies import Input, Output
import datetime


app = dash.Dash(__name__)

image_path = "C:/Users/jvivekg/PycharmProjects/FaceMaskDetection/DetectedFaces/"

def generate_thumbnail(image,count):
    style = {'padding': '5px', 'fontSize': '16px', 'text-align': 'left'}
    return html.Div([
        html.Img(
            src='data:image/jpg;base64,{}'.format(image.decode()),
            style={
                'height': 70,
                'width': 50,
                'position': 'relative',
                'padding-top': 10,
                'padding-right': 10
            }
        ),
        html.Span("Detected: {}".format(count), style=style)
    ])


app.layout = html.Div(
    html.Div([
        html.H1(children="No Mask: Wall of Shame"),
        html.Div(id="date-update"),
        html.H3(children="Faces Detected Today"),
        html.H4(children="Policy for Image Update:"),
        html.P(children="The count of detected face increases if the face is detected without mask "
                        "for more than 5 min. The counts keeps on increasing every 5 min by default. "
                        "The default settings can be changed from options below."),
        html.Div(id="image-update"),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('image-update', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_image(n):
    images_div = []
    listOfPics = os.listdir(image_path)
    for i in listOfPics:
        count = int(i.split(" ")[2][:-4])
        encoded_image = base64.b64encode(open(image_path + i, 'rb').read())
        images_div.append(generate_thumbnail(encoded_image, count))
    return images_div


@app.callback(Output('date-update', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_image(n):
    now = datetime.datetime.now()
    return [html.H2(now.strftime("%Y-%m-%d %H:%M:%S"))]


if __name__ == '__main__':
    app.run_server(debug=True)