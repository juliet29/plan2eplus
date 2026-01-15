from cyclopts import App
from utils4plans.logconfig import logset
from replan2eplus.cli.studies import studies_app

app = App()
app.command(studies_app)


@app.command()
def welcome():
    print("Welcome to replan2eplus")


def main():
    logset()
    app()


if __name__ == "__main__":
    main()
