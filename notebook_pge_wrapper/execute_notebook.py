import sys
import json
import logging
import traceback

import papermill

logging.basicConfig(level='INFO', format="%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S')


def exec_wrapper(func):
    """Execution wrapper to dump alternate errors and tracebacks."""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (Exception, SystemExit) as e:
            with open("_alt_error.txt", "w") as f:
                f.write("%s\n" % str(e))
            with open("_alt_traceback.txt", "w") as f:
                f.write("%s\n" % traceback.format_exc())
            raise
    return wrapper


def _create_nb_output_file_name(nb):
    nb_split = nb.split('.')
    output_nb = nb_split
    output_nb[0] += '-output'
    output_nb[1] = '.' + output_nb[1]
    output_nb = ''.join(output_nb)
    return output_nb


def _read_context(ctx_file):
    """
    reads _context.json file and returns dictionary arguments
    :param ctx_file: str, location of _context.json
    :return: dict[Str, <any>]
    """
    with open(ctx_file, 'r') as f:
        ctx = json.loads(f.read())
        return ctx


def _build_notebook_params(nb, ctx):
    nb_params = papermill.inspect_notebook(nb)

    params = {}
    for k, p in nb_params.items():
        if k.startswith('hysds_'):
            continue

        if ctx.get(k) is not None:  # if key is found in _context.json then populate params dict with value
            params[k] = ctx[k]
    return params


@exec_wrapper
def execute(nb, ctx_file):
    ctx = _read_context(ctx_file)
    params = _build_notebook_params(nb, ctx)

    f_info = open('_alt_info.txt', 'w')

    output_nb = _create_nb_output_file_name(nb)
    papermill.execute_notebook(nb, output_nb, parameters=params, log_output=True, stdout_file=f_info)


if __name__ == '__main__':
    notebook = sys.argv[1]
    execute(notebook, '_context.json')
