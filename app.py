import numpy as np
import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, State, dcc, html

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

n = 3

multiple_freq = 0.5
multiple_interval = 2000
min_dead_time_multiple = 2000
max_dead_time_multiple = 5000
time_since_last_flash_multiple = 0
sequence = ["red_yellow", "green", "yellow", "red"]
current_state = 0

single_freq = 0.1
single_interval = 5000
min_dead_time_single = 4000
max_dead_time_single = 20000
time_since_last_flash_single = 0

light_path = lambda spec: f"assets/{spec}.png"


app.layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        dcc.Interval(
                            id="multiple_interval",
                            interval=multiple_interval,
                        ),
                        dcc.Interval(
                            id="single_interval",
                            interval=single_interval,
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
    *[State(f"light_{i}", "src") for i in range(n)],
    Input("multiple_interval", "n_intervals"),
)
def update_lights(light1: str, light2: str, light3: str, _: int) -> list:
    global time_since_last_flash_multiple, current_state
    time_since_last_flash_multiple += multiple_interval
    do_change = np.random.binomial(1, multiple_freq)
    past_min_dead_time = min_dead_time_multiple < time_since_last_flash_multiple
    past_max_dead_time = max_dead_time_multiple < time_since_last_flash_multiple

    if past_min_dead_time and (do_change or past_max_dead_time):
        time_since_last_flash_multiple = 0
        which_lamp_on = np.random.choice(range(n))
        color = sequence[current_state % 4]
        current_state += 1
        return [
            light_path(color) if i == which_lamp_on else light_path("off")
            for i in range(n)
        ]
    else:
        return [light_path(light.split("/")[1].removesuffix(".png")) for light in [light1, light2, light3]]


@app.callback(
    Output("single_light", "src"),
    Input("single_interval", "n_intervals"),
)
def update_light(_: int) -> list:
    global time_since_last_flash_single
    time_since_last_flash_single += single_interval
    do_change = np.random.binomial(1, single_freq)
    past_min_dead_time = min_dead_time_single < time_since_last_flash_single
    past_max_dead_time = max_dead_time_single < time_since_last_flash_single

    if past_min_dead_time and (do_change or past_max_dead_time):
        time_since_last_flash_single = 0
        return light_path("single_on")
    else:
        return light_path("single_off")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
