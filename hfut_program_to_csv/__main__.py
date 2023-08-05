import click

from hfut_program_to_csv.eams import EAMS


@click.command()
@click.option("-c", "--config", help="Config file path")
def run(config: str | None):
    EAMS(config).to_csv()


if __name__ == "__main__":
    run()
