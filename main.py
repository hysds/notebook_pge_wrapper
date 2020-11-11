import os

from notebook_pge_wrapper.spec_generator import generate_spec_files


if __name__ == '__main__':
    nb_directory = 'notebook_pges'

    # TODO:
    # specification values (time_limit, disk_usage, submission_type) are hard coded (for now)
    # opened a Github issue to allow for inspection of notebook cell that's tagged with something else (not parameters)
    # https://github.com/nteract/papermill/issues/547

    if not os.path.exists('docker'):
        print('docker directory should already exist, please check your repo')
        os.mkdir('docker')

    for nb in os.listdir(nb_directory):  # iterate through notebook_pges/ directory
        if not nb.endswith('.ipynb'):
            print('%s is not a notebook, skipping...' % nb)
            continue
        print('inspecting notebook: %s' % nb)
        generate_spec_files(nb)
