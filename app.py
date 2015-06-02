
import os
from livereload import Server


BUILD_DIR = 'build'

DOCTYPE = (
    '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '''
    '''"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'''
)

TEMPLATE_START = '''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>TITLE</title>
<style type="text/css">
{{css}}
</style>
</head>
'''


with open('_layouts/container.html', 'rb') as f:
    TEMPLATE_BODY = f.read()

TEMPLATE = DOCTYPE + TEMPLATE_START + TEMPLATE_BODY + '</html>'


def get_shared_css():
    names = ['basic']
    css = []

    for name in names:
        with open(os.path.join('_styles', name + '.css'), 'rb') as f:
            css.append(f.read())
    return '\n'.join(css)


def build(name, inline=False):
    with open(os.path.join(name, 'content.html')) as f:
        content = f.read()

    with open(os.path.join(name, 'style.css')) as f:
        style = f.read()

    rv = TEMPLATE.replace('{{css}}', '\n'.join([get_shared_css(), style]))
    rv = rv.replace('{{content}}', content)

    with open(os.path.join('_build', name + '.html'), 'wb') as f:
        f.write(rv)


def watch(name):
    build(name)

    def _build():
        build(name)

    server = Server()
    server.watch(name, _build)
    server.serve(root='_build')

watch('shipping')
