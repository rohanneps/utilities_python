activate_this = '/home/rohan/Desktop/rohan_backup/Research/Python/Flask_Restplus/RestAPI/Core/restvirt/bin/activate_this.py'
with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))


import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/rohan/Desktop/rohan_backup/Research/Python/Flask_Restplus/RestAPI/Core/")

from startService import app as application
application.secret_key = 'Add your secret key'
