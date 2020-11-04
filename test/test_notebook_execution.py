import os
import unittest

from notebook_pge_wrapper.execute_notebook import execute_notebook, create_nb_output_file_name


class TestJobWorkerFuncs(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.notebook_dir = os.path.join(self.current_directory, "notebooks")

    def test_notebook_execution(self):
        test_nb = os.path.join(self.notebook_dir, 'test.ipynb')
        test_context = os.path.join(self.current_directory, '_context.json')
        execute_notebook(test_nb, test_context)

        # clearing output notebook
        output_nb = create_nb_output_file_name(test_nb)
        if os.path.exists(output_nb):
            os.remove(output_nb)
