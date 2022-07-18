from pathlib import Path
import pytest
import sys

from ez_memprof.main import MemrayProfile

path_to_example_scripts = Path('./example_functions')


class TestMemrayProfileUtils:
    m = MemrayProfile()

    def test_call_cmd(self):
        completed_process_object = self.m._call_cmd('echo test')
        assert completed_process_object.stdout == 'test\n'

    def test_construct_run_cmd_no_kwargs(self):
        input_filename = 'inputfile'
        cmd = self.m._construct_run_cmd(input_filename)
        assert cmd == 'memray run -f ' + input_filename

    def test_construct_run_cmd_output_kwarg(self):
        input_filename = 'inputfile'
        output_file = 'outputfile'
        cmd = self.m._construct_run_cmd(
            input_filename,
            output_file=output_file)
        assert cmd == 'memray run -f -o ' + output_file + ' ' + input_filename

    def test_construct_flamegraph_cmd_no_kwargs(self):
        input_filename = 'inputfile'
        cmd = self.m._construct_flamegraph_cmd(input_filename)
        assert cmd == 'memray flamegraph -f ' + input_filename

    def test_construct_flamegraph_cmd_output_kwarg(self):
        input_filename = 'inputfile'
        output_file = 'outputfile'
        cmd = self.m._construct_flamegraph_cmd(
            input_filename,
            output_file=output_file)
        assert cmd == 'memray flamegraph -f -o ' + output_file + ' ' + input_filename


@pytest.mark.skipif(
    sys.platform[:5] != "linux", reason="Only runs on Linux")
class TestMemrayProfileIntegration:
    m = MemrayProfile()

    def test_memray_run_creates_result_file(self, tmp_path):
        output_path = tmp_path / 'output_test_memray_run_creates_result_file__0.bin'
        file_to_profile = path_to_example_scripts / 'use_x_amount_of_mem.py'
        # print('output_path: ' + str(output_path))
        # print('file_to_profile: ' + str(file_to_profile))
        # assert 0 == str(output_path)
        # assert 0 == str(file_to_profile)
        self.m.do_memray_run(file_to_profile, output_file=output_path)
        Path(output_path).exists()
