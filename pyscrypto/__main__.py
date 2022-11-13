import click

from pyscrypto import ecdsa, number, rsa, shanks


@click.group()
def cli():
    pass


cli.add_command(ecdsa.ecdsa)
cli.add_command(shanks.shanks)
cli.add_command(rsa.rsa)
cli.add_command(number.number)


def main():
    cli()


if __name__ == "__main__":
    main()
