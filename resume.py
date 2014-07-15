#!/usr/bin/env python
# -- coding: utf-8 --

"""
Generate a PDF resume from markdown and customize stylesheets.
"""

import codecs
import os

from jinja2 import Environment, PackageLoader, Markup
from markdown2 import markdown
from optparse import OptionParser
from subprocess import call, check_output


def parse_options():
    """
    Parse options from the command line.

    Currently we can specify path for markdown file.
    """
    usage = "%prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-l',
        '--less',
        dest='less',
        default='src/less/default.less',
        help='specify the path of the LESS file used to generate the css'
    )
    parser.add_option(
        '-m',
        '--markdown',
        dest='markdown',
        default='src/md/yesh.md',
        help=('specify the path of the MARKDOWN used to generate the content '
              'of the html')
    )

    (options, args) = parser.parse_args()
    return options


def generate_markdown(mdfile):
    """
    Generate html from a markdown file at the specified path.
    """
    # Grab file
    f = codecs.open(mdfile, encoding='utf-8')

    # Convert markdown
    html = Markup(markdown(f.read()))

    # Close file
    f.close()

    return html


def create_template(content, css):
    """
    Plug the html content into the body of the template.
    """
    env = Environment(loader=PackageLoader('resume', 'src'))

    template = env.get_template('base.html')

    return template.render(content=content, css=css)


def main():
    options = parse_options()

    # First, generate the content of the resume from its markdown
    content = generate_markdown(options.markdown)

    # Then, compile the less into css
    css = check_output(['lessc', options.less])

    # Next, plug that into the template and save the html
    template = create_template(content, css)

    if not os.path.exists('build/html'):
        os.makedirs('build/html')

    f = codecs.open('build/html/yesh.html', 'w', encoding='utf-8')
    f.write(template)
    f.close()

    # And finally, use that generated html to produce a pdf
    if not os.path.exists('build/pdf'):
        os.makedirs('build/pdf')

    call(['wkhtmltopdf', '-B', '0.0', '-L', '0.0', '-R', '0.0', '-T', '0.0',
          '-s', 'A4', './build/html/yesh.html',
          './build/pdf/yesh.pdf'])


if __name__ == '__main__':
    main()
