# read database.ini file to load config parameters
#  after this program run readVcf to load variants
# from this tutorial: http://www.postgresqltutorial.com/postgresql-python/connect/

from configparser import ConfigParser

def loadDatabaseIni(databaseIniFile):
    parser = ConfigParser()
    parser.read(databaseIniFile)
    db = {}
    if parser.has_section('postgresql'):
        params = parser.items('postgresql')
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('postgresql section missing on database ini file')
    return db

if __name__ == '__main__':
    db = loadDatabaseIni('database.ini')
