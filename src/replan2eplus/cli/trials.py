from cyclopts import App

studies_app = App(name="studies")


@studies_app.command()
def bar(n: int):
    print(f"BAR: {n}")
