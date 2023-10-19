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
off_path = img_path("off")
n = 3
interval = 1000  # this milliseconds between two on / off switches

app.layout = html.Div(
    [
        dcc.Interval(
            id="interval",
            interval=interval,
        ),
        html.Div(
            [
                html.Img(
                    id=f"light_{i}",
                    width=300,
                    style=dict(marginRight=100),
                )
                for i in range(n)
            ],
            style=dict(marginLeft=100, marginTop=100, display="inline-block"),
        ),
    ]
)


@app.callback(
    *[Output(f"light_{i}", "src") for i in range(n)],
    Input("interval", "n_intervals"),
)
def update_metrics(n_intervals: int) -> list:
    if n_intervals:
        if n_intervals % 2 == 0:
            light_on = np.random.choice(np.arange(3))
            color = np.random.choice(["red", "yellow", "green"])
            return [img_path(color) if (i == light_on) else off_path for i in range(n)]
    return [off_path for _ in range(n)]


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
