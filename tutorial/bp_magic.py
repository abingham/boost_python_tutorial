"""This file contains "magic" implementations for IPython Notebook
that allow you to build Boost.Python programs and modules.
"""

import IPython.core.magic as ipym

# IMPORTANT: Adjust these flags to match your system.
#
# For the Python flags you can often use the ``python-config`` command.
# For boost.python, you just need to know.

PYTHON_COMPILE_FLAGS=' '.join([
    '-I/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/include/python2.7',
    '-fno-strict-aliasing',
    '-fno-common',
    '-dynamic',
    '-I/usr/local/include',
    '-I/usr/local/opt/sqlite/include',
    '-DNDEBUG',
    '-g',
    '-fwrapv',
    '-O3',
    '-Wall',
    '-Wstrict-prototypes',
])

PYTHON_LINK_FLAGS=' '.join([
    '-L/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/config',
    '-ldl',
    '-framework',
    'CoreFoundation',
    '-lpython2.7',
])

BP_COMPILE_FLAGS='-I/usr/local/include'

BP_LINK_FLAGS='-L/usr/local/lib -lboost_python'

# STOP EDITING
#
# Don't edit below this line unless you know what you're doing or are
# feeling adventurous (or perhaps are stuck.)

@ipym.magics_class
class BoostPythonMagics(ipym.Magics):
    @ipym.cell_magic
    def bp_program(self, line, cell=None):
        """Compile, execute C++ code, and return the standard output."""

        args = line.split()
        name = args[0]

        args = args[1:]
        debug = 'debug' in args

        # Define the source and executable filenames.
        source_filename = '{}.cpp'.format(name)
        program_filename = './{}.exe'.format(name)
        # Write the code contained in the cell to the C++ file.
        with open(source_filename, 'w') as f:
            f.write(cell)

        rslt = []

        # Compile the C++ code into an executable.
        cmd = "g++ {} {} {} {} {} -o {}".format(
            BP_COMPILE_FLAGS,
            BP_LINK_FLAGS,
            PYTHON_COMPILE_FLAGS,
            PYTHON_LINK_FLAGS,
            source_filename,
            program_filename)

        if debug:
            rslt.append(cmd)

        compile = self.shell.getoutput(cmd)
        rslt.append(compile)

        output = self.shell.getoutput(program_filename)
        rslt.append(output)

        if any(result):
            return '\n'.join(map(str, result))

    @ipym.cell_magic
    def bp_module(self, line, cell=None):
        """Compile a boost.python module."""
        args = line.split()
        module_name = args[0]

        args = args[1:]
        debug = 'debug' in args

        # Define the source and executable filenames.
        source_filename = '{}_temp.cpp'.format(module_name)
        lib_filename = './{}.so'.format(module_name)

        # Write the code contained in the cell to the C++ file.
        with open(source_filename, 'w') as f:
            f.write(cell)

        rslt = []

        # Compile the C++ code into a shared library.
        cmd = "g++ {} {} {} {} -shared {} -o {}".format(
            PYTHON_COMPILE_FLAGS,
            PYTHON_LINK_FLAGS,
            BP_COMPILE_FLAGS,
            BP_LINK_FLAGS,
            source_filename,
            lib_filename)

        if debug:
            rslt.append(cmd)

        # run the compiler
        compile = self.shell.getoutput(cmd)

        rslt.append(compile)

        # If we have no output to report, return None
        if any(rslt):
            return '\n'.join(map(str, rslt))

    @ipym.cell_magic
    def snippet(self, line, cell=None):
        "Ignore this code cell."
        pass

def load_ipython_extension(ipython):
    ipython.register_magics(BoostPythonMagics)