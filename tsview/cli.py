from os import getenv
from threading import Thread
import socket
import webbrowser

import click

from tshistory.util import find_dburi
from tsview.app import kickoff


def tshclass(mode):
    assert mode in ('default', 'formula')
    if mode == 'default':
        from tshistory.tsio import timeseries as tshclass
        return tshclass
    from tshistory_formula.tsio import timeseries as tshclass
    return tshclass


def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]


@click.command()
@click.argument('db-uri')
@click.option('--handler',
              type=click.Choice(['default', 'formula']),
              default='default')
@click.option('--debug', is_flag=True, default=False)
def view(db_uri, handler, debug=False):
    """visualize time series through the web"""
    uri = find_dburi(db_uri)
    ipaddr = host()
    port = int(getenv('TSVIEW_PORT', 5678))

    serieshandler = tshclass(handler)
    if debug:
        kickoff(ipaddr, port, uri, serieshandler)
        return

    server = Thread(
        name='tsview.webapp', target=kickoff,
        kwargs={
            'host': ipaddr,
            'port': port,
            'dburi': uri,
            'handler': serieshandler
        }
    )
    server.daemon = True
    server.start()

    webbrowser.open('http://{ipaddr}:{port}/tsview'.format(ipaddr=ipaddr, port=port))
    input()
