import click

from pyscrypto import ecdsa, shanks


@click.group()
def cli():
    pass


cli.add_command(ecdsa.ecdsa)
cli.add_command(shanks.shanks)


def main():
    cli()


if __name__ == "__main__":
    main()
