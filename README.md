# Intro

This is a (slightly janky) Python wrapper around [memray](https://github.com/bloomberg/memray/)'s CLI interface.

Why is this better than a simple `subprocess.call(['memray', 'run', 'myfile.py']...)`? Well, it comes with a convenience function that lets you run a profile, generate a flamegraph, and (optionally) display the resulting flamegraph in your Jupyter cell, in a single Python function call. That's the main value-add right now.

# Installation



# Testing

## Docker implementation details

Based on [this article](https://pythonspeed.com/articles/conda-docker-image-size/).
