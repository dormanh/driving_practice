import numpy as np
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

img_path = lambda spec: f"assets/{spec}.png"
audio_path = lambda spec: f"assets/{spec}.mp3"
n = 3
interval = 2000
freq = 0.5
time_since_last_flash = 0
min_dead_time = 2000
max_dead_time = 5000


def should_break(light_srcs: list) -> bool:
    """Determines if the player should break based on the lights that are currently on."""
    return any((("red" in s) or ("yellow" in s) for s in light_srcs))


app.layout = html.Div(
    [
        dcc.Interval(
            id="interval",
            interval=interval,
        ),
        html.Div(
            [
                *[
                    html.Img(
                        id=f"light_{i}",
                        src=img_path("off"),
                        width=300,
                        style=dict(marginRight=50),
                    )
                    for i in range(n)
                ],
                html.Audio(
                    id="feedback",
                    src=audio_path("incorrect"),
                    controls=True,
                    autoPlay=False,
                ),
            ],
            style=dict(marginLeft=50, marginTop=50, display="inline-block"),
        ),
    ]
)


@app.callback(
    *[Output(f"light_{i}", "src") for i in range(n)],
    Output("feedback", "src"),
    Input("interval", "n_intervals"),
)
def update_lights(n_intervals: int) -> list:
    global time_since_last_flash
    time_since_last_flash += interval
    if (
        (n_intervals is not None)
        & (min_dead_time < time_since_last_flash)
        & (np.random.binomial(1, freq) | (max_dead_time < time_since_last_flash))
    ):
        time_since_last_flash = 0
        light_on = np.random.choice(np.arange(3))
        color = np.random.choice(["red", "yellow", "green"])
        new_imgs = [
            img_path(color) if (i == light_on) else img_path("off") for i in range(n)
        ]
    else:
        new_imgs = [img_path("off") for _ in range(n)]
    return (
        *new_imgs,
        audio_path("correct" if should_break(new_imgs) else "incorrect"),
    )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
