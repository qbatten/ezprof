from IPython.display import display, HTML

from .main import MemrayProfile


def display_html_file(file_path):
    """
    (For use in Jupyter Notebooks and Hex) Run this in a cell and it will display the
    HTML at the given path. Must be the last line in cell.
    """
    with open(file_path, 'r') as f:
        htmlfile = f.read()
    return display(HTML(htmlfile))


class MemrayProfileIPython(MemrayProfile):
    """
    This subclass of MemrayProfile automatically displays the results of a profiule run
    in the current notebook/cell.

    """
    def profile_and_render_flamegraph(self,
                                      python_file_to_profile,
                                      output_file_base=None,
                                      input_args=None):
        run_output_file, flamegraph_output_file = super().profile_and_render_flamegraph()

        print('Displaying file at "' + flamegraph_output_file)
        display_html_file(flamegraph_output_file)
