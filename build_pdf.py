#!/usr/bin/env python
import click
import subprocess

@click.command()
@click.option('--hw',
    prompt='Which assignment? (use {} to skip this dialogue)'.format('--hw'),
    help='assignment number')
@click.option('-o', help='output pdf file', default='witschey.pdf')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def build_pdf(files, hw, o):
    tmpfilename = '/tmp/hwgen.ps'
    title = '--center-title="csc710sbse: hw{hw}: Witschey"'.format(hw=hw)
    a2ps_cmd = [
        'a2ps',
        '-MLetter',
        title,
        '-1C',
        '--highlight-level=none',
        '-o',
        '-q',
        tmpfilename
    ]
    a2ps_cmd.extend(files)
    p1 = subprocess.call(a2ps_cmd)
    if p1 != 0:
        exit(p1)

    outfile = o
    ps2pdf_cmd = [
        'ps2pdf',
        tmpfilename,
        outfile
    ]
    p2 = subprocess.call(ps2pdf_cmd)


if __name__ == '__main__':
    build_pdf()

# dl listing.* ; a2ps --center-title="csc710sbse: hw1: Witschey" -2C -MLetter -o listing.ps *.py ; ps2pdf listing.ps listing.pdf

