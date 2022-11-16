import click
import json

import micloud.micloud
from micloud.micloud import MiCloud


pass_micloud = click.make_pass_decorator(MiCloud, ensure=True)

@click.group()
def cli():
    """Tool for fetching xiaomi cloud information."""


@cli.command()
@click.option('--username', '-u', prompt=True, help='Your Xiaomi username.')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--country', '-c', default='de', help='Language code of the server to query. Default: "de"')
@click.option('--pretty', is_flag=True, help='Pretty print json output.')
def get_devices(username, password, country, pretty):
    """Get device information, including tokens."""
    mc = MiCloud(username, password)
    mc.login()
    devices = mc.get_devices(country=country)
    if pretty:
        click.echo(json.dumps(devices, indent=2, sort_keys=True))
    else:
        click.echo(json.dumps(devices))


@cli.group()
def miot():
    """Commands for miotspec fetching."""

@miot.command(name="specs")
@click.option("--status", type=str, default="released")
@pass_micloud
def miot_specs(micloud: MiCloud, status):
    """Return all specs filtered by the given status."""
    click.echo(json.dumps(micloud.miot_get_specs(status=status)))


@miot.command(name="get-spec")
@click.argument("urn")
@pass_micloud
def miot_get_spec(micloud: MiCloud, urn):
    """Return a device spec for the given URN."""
    click.echo(json.dumps(micloud.miot_get_spec(urn)))


@miot.command("types")
@click.argument("type", type=click.Choice(micloud.micloud.MIOT_STANDARD_TYPES))
@pass_micloud
def miot_available_standard_types(micloud: MiCloud, type: str):
    """Return available standard URNs for type. """
    click.echo(json.dumps(micloud.miot_get_standard_types(type)))


@miot.command("get-type-spec")
@click.argument("urn")
@pass_micloud
def miot_get_standard_type_spec(micloud: MiCloud, urn: str):
    """Return a type spec for given type URN."""
    click.echo(json.dumps(micloud.miot_get_standard_type_spec(urn)))

if __name__ == "__main__":
    cli()
