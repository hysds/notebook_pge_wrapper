import sys
import traceback
import json

import papermill


def exec_wrapper(func):
    """Execution wrapper to dump alternate errors and tracebacks."""

    def wrapper(*args, **kwargs):
        try:
            # status = func(*args, **kwargs)
            func(*args, **kwargs)
        except (Exception, SystemExit) as e:
            with open("_alt_error.txt", "w") as f:
                f.write("%s\n" % str(e))
            with open("_alt_traceback.txt", "w") as f:
                f.write("%s\n" % traceback.format_exc())
            raise
        # sys.exit(status)  # this breaks with papermill.execute
    return wrapper


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

        # if key is found in _context.json then populate params dict with value
        if ctx.get(k) is not None:
            params[k] = ctx[k]
    return params


@exec_wrapper
def execute_notebook(nb, ctx_file):
    ctx = read_context(ctx_file)
    params = build_notebook_params(nb, ctx)

    output_nb = create_nb_output_file_name(nb)
    papermill.execute_notebook(nb, output_nb, parameters=params, log_output=True)


if __name__ == '__main__':
    notebook = sys.argv[1]
    execute_notebook(notebook, '_context.json')
