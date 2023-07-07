import numpy as np
import PySimpleGUI as sg
import matplotlib as mpl
from matplotlib import figure
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def linear_regression(x_in: list, y_in: list):
    x = np.array(x_in).reshape((-1, 1))
    y = np.array(y_in)

    model = LinearRegression().fit(x, y)

    r_sq = model.score(x, y)

    # print(r_sq)
    # print(f"intercept: {model.intercept_}")
    # print(f"slope: {model.coef_}")

    # y_pred = model.predict(x)
    # print(f"predicted response:\n{y_pred}")

    return model, r_sq, model.coef_, model.intercept_


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def draw_linear_regression(window, x, y, name):
    result, r_sq, coef, intercept = linear_regression(x, y)

    fig = figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, max(x[0]), 1)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    ax1.plot(t, (coef * t) + intercept)
    ax2.scatter(x, y, color="red")

    mpl.use("TkAgg")

    layout = [
        # [sg.Image(filename=".\Assets\CParkerLogo.png", size=(100, 100), pad=(10, 10))],
        [sg.Text(name)],
        [sg.Canvas(key="-CANVAS-")],
        # [sg.Button("OK")],
        [
            sg.Text(
                "R^2: "
                + str(round(r_sq, 2))
                + " m: "
                + str(round(coef[0], 2))
                + " int: "
                + str(round(intercept, 2))
            )
        ],
        # [sg.Text("Use nodel to predict x: ")],
        # [sg.Input(key="-TESTX-")],
        # [sg.Text("Result: " + str(round((result.predict(values["-TESTX-"])), 2)))],
    ]

    window = sg.Window(
        "Regression Results",
        layout,
        location=(0, 0),
        finalize=True,
        element_justification="center",
        font="Helvetica 18",
    )

    # while True:
    #     event, values = window.read()

    #     if event == "OK" or event == sg.WIN_CLOSED:
    #         break

    # window.close()

    draw_figure(window["-CANVAS-"].TKCanvas, fig)


def check_not_empty(input):
    retval = False
    try:
        if input[-4:] == ".csv" or input[-4:] == ".CSV":
            retval = True
    finally:
        return retval


def read_clean_sort_data(raw_input):
    f = open(raw_input, "r", encoding="utf-8-sig")
    raw_input = f.read()
    raw_input = raw_input.split("\n")
    for i in range(len(raw_input)):
        if raw_input[i] == "":
            del raw_input[i]

    y = raw_input[-1].split(",")
    y_int = []
    x = []
    x_int = []

    for i in range(len(y)):
        y_int.append(int(y[i]))

    del raw_input[-1]

    for i in raw_input:
        x.append(i.split(","))

    for i in range(len(x)):
        x_temp = []
        for j in range(len(x[i])):
            x_temp.append(int(x[i][j]))
        x_int.append(x_temp)

    return (x_int, y_int)


def main():
    layout = [
        [
            sg.Text("Choose a file: "),
            sg.FileBrowse(key="-FILEIN-"),
            sg.Button("Run Regression"),
        ]
    ]

    window = sg.Window(
        "File Selector",
        layout,
        location=(0, 0),
        finalize=True,
        element_justification="center",
        font="Helvetica 18",
    )

    state = "input"

    while True:
        event, values = window.read()

        if event == "OK" or event == sg.WIN_CLOSED:
            break

        elif event == "Run Regression":
            # print(values["-FILEIN-"])
            if check_not_empty(values["-FILEIN-"]):
                x_in, y_in = read_clean_sort_data(values["-FILEIN-"])

                # print(x_in)
                # print(y_in)

                draw_linear_regression(window, x_in, y_in, values["-FILEIN-"])

            else:
                print("please select a valid .csv file")
                # add GUI popup

    window.close()


main()
