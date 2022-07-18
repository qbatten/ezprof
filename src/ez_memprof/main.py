import subprocess
import re


class MemrayProfile:

    def _call_cmd(self, cmd_string):
        """
        Takes a string and runs it using the appropriate args for subprocess.run in this context.
        Returns the CompletedProcess object when the subprocess completes.
        """
        print('Running cmd: ' + cmd_string)
        return subprocess.run(cmd_string.split(' '), capture_output=True, text=True)

    def _construct_run_cmd(self,
                           python_file_to_profile,
                           output_file=None,
                           input_args=None,
                           overwrite_file=True):
        """
        Constructs the correct string to run memray given the passed args.

        Args:
            python_file_to_profile (str): Path to the python file you'd like memray to run and profile for you
            output_file (str): Path to the file you'd like memray to put it's results in (MUST end in '.bin')
            input_args (str): Space-separated string with the args you'd like passed to the file being profiled.
                e.g. if you want to call 'myfile.py arg1 arg2', you'd pass 'arg1 arg2' to this kwarg.
            overwrite_file (bool): Whether to overwrite the destination file if it exists. If you aren't
                passing an output_file arg, memray will automatially generate a new output filename so this
                arg won't matter.

        Returns:
            A strings, to be passed to _call_cmd.
        """
        cmd = 'memray run'
        if overwrite_file:
            cmd += ' -f'
        if output_file:
            cmd += f' -o {output_file}'
        cmd += ' ' + str(python_file_to_profile)
        if input_args:
            cmd += ' ' + input_args
        return cmd

    def _parse_run_output(self, completed_process_object):
        """
        Takes the results of a memray run (run via _call_cmd) and parses the stdout to get useful info.

        Args:
            completed_process_object (CompletedProcess): A subprocess.CompletedProcess obj. Must have
                    been run with capture_output and text flags set to True.

        Returns:
            A tuple, with two values:
                - Whether or not memray successfully wrote results to the file
                - The output file string (mainly useful if you didn't pass a custom output file arg.)
        """
        printout = completed_process_object.stdout
        print("===== Printing RUN output ================= ")
        print(printout)
        if type(printout) != str:
            print("Error: Must run command with subprocess.run([...], capture_output=True, text=True)")
        output_file_match = re.search('Writing profile results into ([^\n]+)', printout)
        output_file = None if not output_file_match else output_file_match.group(1)
        # successfully_wrote_results = 1 if re.search('[memray] Successfully generated profile results.', printout) else 0
        # if not successfully_wrote_results:
        #     raise OSError('Error on memray run: ' + printout)
        return 1, output_file

    def _construct_flamegraph_cmd(self,
                                  memray_results_file,
                                  output_file=None):
        """
        Constructs the correct string to make a memray flamegraph given the passed args.

        Args:
            memray_results_file (str): Path to the memray output file you'd like to make a flamegraph for
            output_file (str): Path to the file you'd like memray to put it's results in (MUST end in '.bin')

        Returns:
            A string, to be passed to _call_cmd.
        """
        cmd = 'memray flamegraph -f'
        if output_file:
            cmd += f' -o {output_file}'
        cmd += ' ' + str(memray_results_file)
        return cmd

    def _parse_flamegraph_output(self, completed_process_object):
        """
        Takes the results of a memray flamegraph (run via _call_cmd) and parses the stdout to get useful info.
        Args:
            completed_process_object (CompletedProcess): A subprocess.CompletedProcess obj. Must have
                    been run with capture_output and text flags set to True.
        Returns:
            A tuple, with two values:
                - Whether or not memray successfully wrote results to the file
                - The output file string (mainly useful if you didn't pass a custom output file arg.)
        """
        printout = completed_process_object.stdout
        print("===== Printing FLAMEGRAPH output ================= ")
        print(printout)
        if type(printout) != str:
            print("Error: Must run command with subprocess.run([...], capture_output=True, text=True)")
        output_file_match = re.search('Wrote ([^\n]+)', printout)
        output_file = None if not output_file_match else output_file_match.group(1)
        return output_file is not None, output_file

    def do_memray_run(self,
                      python_file_to_profile,
                      output_file=None,
                      input_args=None):
        cmd_string = self._construct_run_cmd(python_file_to_profile,
                                             output_file=output_file,
                                             input_args=input_args)
        run_completed_process = self._call_cmd(cmd_string)
        successfully_wrote_results, run_output_file = self._parse_run_output(run_completed_process)
        if not successfully_wrote_results:
            raise Exception('Failed to profile program')
        print('Run complete. Runfile written to ' + run_output_file + '.')
        return successfully_wrote_results, run_output_file

    def do_memray_flamegraph(self, memray_results_file, output_file=None):
        cmd = self._construct_flamegraph_cmd(memray_results_file, output_file=output_file)
        print('Running flamegraph creation cmd: ' + cmd)
        completed_process = self._call_cmd(cmd)
        succeeded, output_file = self._parse_flamegraph_output(completed_process)
        if succeeded:
            print('Flamegraph generated for ' + memray_results_file + '. Flamegraph at ' + output_file)
        return succeeded, output_file

    def profile_and_render_flamegraph(self,
                                      python_file_to_profile,
                                      output_file_base=None,
                                      input_args=None):
        """
        Takes a python program plus cmdline args to pass to it; does a memray profile run, creates a
        flamegraph of the result, and displays the graph.

        Usage
        =====
        mr = MemrayProfile()
        mr.profile_program_and_display_flamegraph('file_to_profile.py', input_args='--output outputfile.txt')
        """
        if not output_file_base:
            output_file_base = python_file_to_profile.replace('.py', '') + '__' + re.sub('[-_ .]', '_', input_args)
        run_output_file = output_file_base + '_mr_output.bin'
        flamegraph_output_file = output_file_base + '_flamegraph.html'

        run_succeeded, _ = self.do_memray_run(python_file_to_profile,
                                              output_file=run_output_file,
                                              input_args=input_args)
        flamegraph_succeeded, flamegraph_output_file_parsed = self.do_memray_flamegraph(run_output_file,
                                                                                        output_file=flamegraph_output_file)
        print('Program ' + python_file_to_profile + ' profiled!')
        print('Memray output at ' + run_output_file + '; flamegraph at ' + flamegraph_output_file)
        return (run_output_file, flamegraph_output_file)
