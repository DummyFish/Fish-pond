import sqlite3


def check_service_num():
    database = sqlite3.connect('../logger.db')
    data = database.cursor()
    ssh = data.execute("select count(*) from FishPond where service == 'ssh'").fetchall()[0][0]
    ftp = data.execute("select count(*) from FishPond where service == 'ftp'").fetchall()[0][0]
    rdp = data.execute("select count(*) from FishPond where service == 'rdp'").fetchall()[0][0]
    redis = data.execute("select count(*) from FishPond where service == 'redis'").fetchall()[0][0]
    smtp = data.execute("select count(*) from FishPond where service == 'smtp'").fetchall()[0][0]
    telnet = data.execute("select count(*) from FishPond where service == 'telnet'").fetchall()[0][0]
    pop3 = data.execute("select count(*) from FishPond where service == 'pop3'").fetchall()[0][0]
    tftp = data.execute("select count(*) from FishPond where service == 'tftp'").fetchall()[0][0]
    count = {
        'ssh': {'id': 'ssh', 'count': ssh},
        'smtp': {'id': 'smtp', 'count': smtp},
        'ftp': {'id': 'ftp', 'count': ftp},
        'telnet': {'id': 'telnet', 'count': telnet},
        'rdp': {'id': 'rdp', 'count': rdp},
        'redis': {'id': 'redis', 'count': redis},
        'pop3': {'id': 'pop3', 'count': pop3},
        'tftp': {'id': 'tftp', 'count': tftp},
    }
    return count


def get_latest_log(date=None):
    if (date == None):
        database = sqlite3.connect('../logger.db')
        data = database.cursor()
        log = data.execute("select * from FishPond Order By exetime Desc limit 5").fetchall()
    else:
        database = sqlite3.connect('../logger.db')
        data = database.cursor()
        log = data.execute("select * from FishPond where exetime > ? Order By exetime Desc limit 5", (date,)).fetchall()
    return log
