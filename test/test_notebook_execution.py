import os
import unittest

from notebook_pge_wrapper.execute_notebook import execute, _create_nb_output_file_name


class TestJobWorkerFuncs(unittest.TestCase):
    def setUp(self):
        self.test_loc = os.path.dirname(os.path.abspath(__file__))
        self.notebook_dir = os.path.join(self.test_loc, "notebook_pges")

        self.stdout_file = '_alt_info.txt'
        self.stderr_file = '_alt_error.txt'

    def tearDown(self):
        stdout_file = os.path.join(os.curdir, self.stdout_file)
        stderr_file = os.path.join(os.curdir, self.stderr_file)

        if os.path.exists(stdout_file):
            os.remove(stdout_file)
        if os.path.exists(stderr_file):
            os.remove(stderr_file)

        for nb in os.listdir(os.getcwd()):
            if nb.endswith('-output.ipynb'):
                os.remove(nb)

    def test_notebook_execution(self):
        test_nb = os.path.join(self.notebook_dir, 'test.ipynb')
        test_context = os.path.join(self.test_loc, '_context.json')
        execute(test_nb, ctx_file=test_context)

    def test_output_nb_name_generation(self):
        test_nb = os.path.join(self.notebook_dir, 'test.ipynb')
        output_nb = _create_nb_output_file_name(test_nb)
        expected_output_nb = 'test-output.ipynb'
        self.assertEqual(output_nb, expected_output_nb)
