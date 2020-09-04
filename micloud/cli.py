import click
import json
from micloud.micloud import MiCloud

@click.command()
@click.option('--username', '-u', prompt=True, help='Your Xiaomi username.')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--country', '-c', default='de', help='Language code of the server to query. Default: "de"')
@click.option('--pretty', is_flag=True, help='Pretty print json output.')
def get_devices(username, password, country, pretty):
    mc = MiCloud(username, password)
    mc.login()
    devices = mc.get_devices(country=country)
    if pretty:
        click.echo(json.dumps(devices, indent=2, sort_keys=True))
    else:
        click.echo(json.dumps(devices))
