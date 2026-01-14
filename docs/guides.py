import marimo

__generated_with = "0.10.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import replan2eplus as rp
    return (rp,)


if __name__ == "__main__":
    app.run()
