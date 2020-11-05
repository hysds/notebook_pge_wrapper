import sys
import json
import logging
import papermill

logging.basicConfig(level='INFO', format="%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')


def create_nb_output_file_name(nb):
    nb_split = nb.split('.')
    output_nb = nb_split
    output_nb[0] += '-output'
    output_nb[1] = '.' + output_nb[1]
    output_nb = ''.join(output_nb)
    return output_nb


def read_context(ctx_file):
    """
    reads _context.json file and returns dictionary arguments
    :param ctx_file:
    :return: dict[Str, <any>]
    """
    with open(ctx_file, 'r') as f:
        ctx = json.loads(f.read())
        return ctx


def build_notebook_params(nb, ctx):
    nb_params = papermill.inspect_notebook(nb)

    params = {}
    for k, p in nb_params.items():
        if k.startswith('hysds_'):
            continue

        if ctx.get(k) is not None:  # if key is found in _context.json then populate params dict with value
            params[k] = ctx[k]
    return params


STDOUT_FILE = '_alt_info.txt'
STDERR_FILE = '_alt_error.txt'


def execute(nb, ctx_file):
    ctx = read_context(ctx_file)
    params = build_notebook_params(nb, ctx)

    f_info = open(STDOUT_FILE, 'w+')
    f_err = open(STDERR_FILE, 'w+')

    output_nb = create_nb_output_file_name(nb)
    papermill.execute_notebook(nb, output_nb, parameters=params, log_output=True,
                               stdout_file=f_info, stderr_file=f_err)


if __name__ == '__main__':
    notebook = sys.argv[1]
    execute(notebook, '_context.json')
