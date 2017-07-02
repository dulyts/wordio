import os
import sys
from eve import Eve
import settings
from src.user import register, login
from src.auth.auth import WordioAuth
from src.logger import LogService
import pymongo
SETTINGS_PATH = os.path.abspath(settings.__file__)

def enable_cors(app):
    try:
        from flask_cors import CORS
        CORS(app)
    except:
        pass

def main(logger, app):
    try:
        logger.debug("Starting")
        enable_cors(app)
        app.run()
    except:
        error = sys.exc_info()[0]
        print("Error in main %s" % error)
        if logger:
            logger.error(error)

app = Eve(auth = WordioAuth, settings=SETTINGS_PATH)

@app.route('/hello', methods=['GET'])
def hello():
    result = None
    try:
        helloCollection = app.data.driver.db['_hello']
        lookup = {'foo': 'bar'}
        find = helloCollection.find_one(lookup)
        if(find):
            helloCollection.delete_one(lookup)
        else:
            helloCollection.insert_one(lookup)
        result = "up&running"
    except (pymongo.errors.AutoReconnect, pymongo.errors.ServerSelectionTimeoutError):
        result = "db_not_available!"
    return '''{
"status": "%s"         
}''' % result

@app.route('/login', methods=['POST'])
def lgn():
    return login.login(app)

@app.route('/register', methods=['POST'])
def reg():
    return register.register(app)

if __name__ == '__main__':
    logger = LogService("log.txt")
    main(logger, app)
