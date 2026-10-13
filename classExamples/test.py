import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    x = 10
    y = 25
    return x, y


@app.cell
def _(x, y):
    print (x+y)
    return


@app.cell
def _(x, y):
    print (y-x)
    return


if __name__ == "__main__":
    app.run()
