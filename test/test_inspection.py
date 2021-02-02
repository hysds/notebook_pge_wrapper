import os
import unittest
from notebook_pge_wrapper.spec_generator import extract_hysds_specs, generate_job_spec, _get_hysdsio_param_type, \
    _generate_hysdsio_params


class TestInspection(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.notebook_dir = "test/notebook_pges"
        self.test_nb = "test.ipynb"
        self.test_nb_2 = "test2.ipynb"

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
        __LIST = 'object'
        __DICT = 'object'

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
            'command': 'notebook-pge-wrapper execute /home/ops/notebook_pge_wrapper/test/notebook_pges/test.ipynb',
            'disk_usage': '10GB',
            'imported_worker_files': {'$HOME/.aws': '/home/ops/.aws'},
            'params': [
                {'destination': 'context', 'name': 'a'},
                {'destination': 'context', 'name': 'b'},
                {'destination': 'context', 'name': 'c'},
                {'destination': 'context', 'name': 'd'},
                {'destination': 'context', 'name': 'e'},
                {'destination': 'context', 'name': 'f'},
                {'destination': 'context', 'name': 'g'},
                {'destination': 'context', 'name': 'h'},
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
        command = hysds_specs.get('command')

        job_spec = generate_job_spec(nb=nb_path, soft_time_limit=soft_time_limit, time_limit=time_limit,
                                     required_queue=required_queue, disk_usage=disk_usage, command=command)
        self.assertDictEqual(job_spec, expected_job_spec)

    def test_hysds_io_param_generation(self):
        nb_path = os.path.join(self.notebook_dir, self.test_nb)

        hysds_io_params = _generate_hysdsio_params(nb_path)
        expected_hysds_io_params = [
            {'default': '100', 'from': 'submitter', 'name': 'a', 'type': 'number'},
            {'default': 'jfksl', 'from': 'submitter', 'name': 'b', 'type': 'text'},
            {'default': '10.2553', 'from': 'submitter', 'name': 'c', 'type': 'number'},
            {'default': [1, 2, 3, 4, 5], 'from': 'submitter', 'name': 'd', 'type': 'object'},
            {
                'default': ['a', 'b', 'c'],
                'from': 'submitter',
                'name': 'e',
                'type': 'object'
            },
            {'default': 'fjskl', 'from': 'submitter', 'name': 'f', 'type': 'text'},
            {
                'default': 'yes',
                'enumerables': ["yes", "no", "maybe so"],
                'from': 'submitter',
                'name': 'g',
                'type': 'enum'
            },
            {
                'default': {'a': 1, "b": 2, 'c': 3},
                'from': 'submitter',
                'name': 'h',
                'type': 'object'
            }
        ]
        self.assertEqual(hysds_io_params, expected_hysds_io_params)

    def test_job_spec_command(self):
        nb_path = os.path.join(self.notebook_dir, self.test_nb_2)

        hysds_specs = extract_hysds_specs(nb_path)
        expected_command = 'python custom_wrapper_script.py'
        command = hysds_specs.get('command')

        self.assertEqual(expected_command, command)
