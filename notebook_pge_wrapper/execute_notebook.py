import sys
import traceback
import json

import papermill


def exec_wrapper(func):
    """Execution wrapper to dump alternate errors and tracebacks."""

    def wrapper(*args, **kwargs):
        try:
            status = func(*args, **kwargs)
        except (Exception, SystemExit) as e:
            with open("_alt_error.txt", "w") as f:
                f.write("%s\n" % str(e))
            with open("_alt_traceback.txt", "w") as f:
                f.write("%s\n" % traceback.format_exc())
            raise
        sys.exit(status)
    return wrapper


def create_nb_output_file_name(nb):
    nb_split = nb.split('.')
    output_nb = nb_split
    output_nb[0] += '-output'
    output_nb[1] = '.' + output_nb[1]
    output_nb = ''.join(output_nb)
    return output_nb


def extract_params(ctx_file):
    """
    reads _context.json file and returns dictionary arguments
    :param ctx_file:
    :return: dict[Str, <any>]
    """
    with open(ctx_file, 'r') as f:
        ctx = json.loads(f)
        return ctx['params']


@exec_wrapper
def execute_notebook(nb, ctx_file):
    params = extract_params(ctx_file)

    output_nb = create_nb_output_file_name(nb)
    papermill.execute_notebook(nb, output_nb, parameters=params)


if __name__ == '__main__':
    notebook = sys.argv[1]
    execute_notebook(notebook, '_context.json')
