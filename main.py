import os
import json

from notebook_pge_wrapper.spec_generator import DockerBuildPGEParamsGenerator


if __name__ == '__main__':
    docker_pge_generator = DockerBuildPGEParamsGenerator()
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

        nb_split = nb.split('.')
        root_name = nb_split[0]

        nb_path = os.path.join('notebook_pges', nb)

        # extracting hysds_io and job_specs from notebook
        hysds_specs = docker_pge_generator.extract_hysds_specs(nb_path)

        time_limit = hysds_specs.get('time_limit')
        soft_time_limit = hysds_specs.get('soft_time_limit')
        disk_usage = hysds_specs.get('disk_usage')
        submission_type = hysds_specs.get('submission_type', 'individual')
        required_queue = hysds_specs.get('required_queue', 'factotum-job_worker-small')
        label = hysds_specs.get('label')

        # generate hysds_io
        # copying hysds_io.json to docker/
        hysdsio = docker_pge_generator.generate_hysdsio(nb_name=nb_path, sub_type=submission_type, job_label=label)
        hysdsio_file = 'hysds-io.json.%s' % root_name
        hysdsio_file_location = os.path.join('docker', hysdsio_file)

        with open(hysdsio_file_location, 'w+') as f:
            json.dump(hysdsio, f, indent=2)
        print('generated %s' % hysdsio_file_location)

        # generate job_specs
        # copying job_specs.json to docker/
        job_spec = docker_pge_generator.generate_job_spec(nb_name=nb_path, soft_time_limit=soft_time_limit,
                                                          time_limit=time_limit, required_queue=required_queue,
                                                          disk_usage=disk_usage)
        job_spec_file = 'job-spec.json.%s' % root_name
        job_spec_file_location = os.path.join('docker', job_spec_file)

        with open(job_spec_file_location, 'w+') as f:
            json.dump(job_spec, f, indent=2)
        print('generated %s' % job_spec_file_location)
