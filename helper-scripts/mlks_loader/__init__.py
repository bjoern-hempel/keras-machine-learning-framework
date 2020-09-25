import os,sys,inspect

# find out the root dir of this project
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

# load root libraries
sys.path.insert(0, root_dir)
