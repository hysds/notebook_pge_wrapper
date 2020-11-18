import os
import unittest
from notebook_pge_wrapper.spec_generator import extract_hysds_specs, generate_job_spec, _get_hysdsio_param_type


class TestInspection(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.notebook_dir = os.path.join(self.current_directory, "notebook_pges")
        self.test_nb = "test.ipynb"

    def tearDown(self):
        pass

    def test_hysds_specs(self):
        nb_path = os.path.join(self.notebook_dir, self.test_nb)
        hysds_specs = extract_hysds_specs(nb_path)
        expected_hysds_specs = {
            'time_limit': 57389,
            'soft_time_limit': 4738,
            'disk_usage': '10GB',
            'submission_type': 'iteration',
            'required_queue': 'test_queue-worker',
            'label': 'TEST LABEL FOR HYSDS_IOS',
        }
        self.assertDictEqual(hysds_specs, expected_hysds_specs)

    def test_hysds_io_param_mapper(self):
        __TEXT = 'text'
        __NUMBER = 'number'
        __DATE = 'date'
        __DATETIME = 'datetime'
        __BOOLEAN = 'boolean'
        __EMAIL = 'email'
        __TEXT_AREA = 'textarea'
        __LIST = 'list'
        __DICT = 'dict'

        self.assertEqual(_get_hysdsio_param_type('str'), __TEXT)
        self.assertEqual(_get_hysdsio_param_type('string'), __TEXT)
        self.assertEqual(_get_hysdsio_param_type('text'), __TEXT)
        self.assertEqual(_get_hysdsio_param_type('float'), __NUMBER)
        self.assertEqual(_get_hysdsio_param_type('num'), __NUMBER)
        self.assertEqual(_get_hysdsio_param_type('int'), __NUMBER)
        self.assertEqual(_get_hysdsio_param_type('integer'), __NUMBER)
        self.assertEqual(_get_hysdsio_param_type('date'), __DATE)
        self.assertEqual(_get_hysdsio_param_type('date_time'), __DATETIME)
        self.assertEqual(_get_hysdsio_param_type('datetime'), __DATETIME)
        self.assertEqual(_get_hysdsio_param_type('bool'), __BOOLEAN)
        self.assertEqual(_get_hysdsio_param_type('boolean'), __BOOLEAN)
        self.assertEqual(_get_hysdsio_param_type('email'), __EMAIL)
        self.assertEqual(_get_hysdsio_param_type('textarea'), __TEXT_AREA)
        self.assertEqual(_get_hysdsio_param_type('list'), __LIST)
        self.assertEqual(_get_hysdsio_param_type('array'), __LIST)
        self.assertEqual(_get_hysdsio_param_type('arr'), __LIST)
        self.assertEqual(_get_hysdsio_param_type('dict'), __DICT)
        self.assertEqual(_get_hysdsio_param_type('obj'), __DICT)
        self.assertEqual(_get_hysdsio_param_type('object'), __DICT)
        self.assertEqual(_get_hysdsio_param_type('unknown_type'), __TEXT)

    def test_job_spec_generation(self):
        nb_path = os.path.join(self.notebook_dir, self.test_nb)

        expected_job_spec = {
            'command': 'notebook-pge-wrapper execute %s' % nb_path,
            'disk_usage': '10GB',
            'imported_worker_files': {'$HOME/.aws': '/home/ops/.aws'},
            'params': [
                {'destination': 'context', 'name': 'a'},
                {'destination': 'context', 'name': 'b'},
                {'destination': 'context', 'name': 'c'},
                {'destination': 'context', 'name': 'd'},
                {'destination': 'context', 'name': 'e'},
                {'destination': 'context', 'name': 'f'},
                {'destination': 'context', 'name': 'g'}
            ],
            'required_queues': ['test_queue-worker'],
            'soft_time_limit': 4738,
            'time_limit': 57389
        }

        hysds_specs = extract_hysds_specs(nb_path)

        time_limit = hysds_specs.get('time_limit')
        soft_time_limit = hysds_specs.get('soft_time_limit')
        disk_usage = hysds_specs.get('disk_usage')
        required_queue = hysds_specs.get('required_queue', 'factotum-job_worker-small')

        job_spec = generate_job_spec(nb=nb_path, soft_time_limit=soft_time_limit, time_limit=time_limit,
                                     required_queue=required_queue, disk_usage=disk_usage)
        self.assertDictEqual(job_spec, expected_job_spec)
