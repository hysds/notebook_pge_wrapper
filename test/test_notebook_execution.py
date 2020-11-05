import os
import unittest

from notebook_pge_wrapper.execute_notebook import execute


class TestJobWorkerFuncs(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.notebook_dir = os.path.join(self.current_directory, "notebooks")

        self.stdout_file = '_alt_info.txt'
        self.stderr_file = '_alt_error.txt'

    def tearDown(self):
        stdout_file = os.path.join(os.curdir, self.stdout_file)
        stderr_file = os.path.join(os.curdir, self.stderr_file)

        if os.path.exists(stdout_file):
            os.remove(stdout_file)
        if os.path.exists(stderr_file):
            os.remove(stderr_file)

        for nb in os.listdir(self.notebook_dir):
            if nb.endswith('-output.ipynb'):
                output_file = os.path.join(self.notebook_dir, nb)
                os.remove(output_file)

    def test_notebook_execution(self):
        test_nb = os.path.join(self.notebook_dir, 'test.ipynb')
        test_context = os.path.join(self.current_directory, '_context.json')
        execute(test_nb, test_context)
