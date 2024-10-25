import numpy as np
import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, dcc, html

app = Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
    ],
    external_scripts=[
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js",
    ],
    suppress_callback_exceptions=True,
)

light_path = lambda spec: f"assets/{spec}.png"
n = 3
light_interval = 2000
freq = 0.5
time_since_last_flash = 0
min_dead_time = 2000
max_dead_time = 5000


app.layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        dcc.Interval(
                            id="light_interval",
                            interval=light_interval,
                        ),
                    ]
                )
            ),
            *[
                dbc.Col(
                    html.Img(
                        id=f"light_{i}",
                        src=light_path("off"),
                        width=300,
                        style=dict(marginRight=50),
                    )
                )
                for i in range(n)
            ],
            dbc.Col(
                [
                    html.Div(
                        dbc.Button(
                            "fékezz!",
                            id="break",
                            color="danger",
                            size="lg",
                            outline=True,
                        ),
                        style=dict(marginBottom=100, marginRight=100),
                    ),
                    dbc.Row(
                        html.Img(
                            id="single_light",
                            src=light_path("single_off"),
                            width=200,
                        ),
                        style=dict(marginRight=20),
                    ),
                ]
            ),
        ]
    ),
    style=dict(marginTop=50),
)


@app.callback(
    *[Output(f"light_{i}", "src") for i in range(n)],
    Output("single_light", "src"),
    Input("light_interval", "n_intervals"),
)
def update_lights(n_intervals: int) -> list:
    global time_since_last_flash
    time_since_last_flash += light_interval
    if (
        (n_intervals is not None)
        & (min_dead_time < time_since_last_flash)
        & (np.random.binomial(1, freq) | (max_dead_time < time_since_last_flash))
    ):
        time_since_last_flash = 0
        light_on = np.random.choice(np.arange(3))
        color = np.random.choice(["red", "yellow", "green"])
        single_on = np.random.binomial(1, 0.4)
        new_imgs = [
            *[
                light_path(color) if (i == light_on) else light_path("off")
                for i in range(n)
            ],
            light_path("single_on" if single_on else "single_off"),
        ]
    else:
        new_imgs = [*[light_path("off") for _ in range(n)], light_path("single_off")]
    return new_imgs


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
