#  utils.py
#  Copyright (c) 25/02/2020, 03:18.
#  Fabrizio Augusto Poltronieri  (fabrizio@fabriziopoltronieri.com)
#  Craig Vear (cvear@dmu.ac.uk)
#  Thom Corah (tcorah@dmu.ac.uk)

# this is a module containing useful functions designed by us
# to be shared among our python scripts. most of them are very simple

import os
import os.path

from os import path


def check_slash(directory):
    if directory.endswith('/'):
        pass
    else:
        directory = directory + '/'
    print(directory)
    return directory


def check_file_folder(file_folder):
    return path.exists(file_folder)
