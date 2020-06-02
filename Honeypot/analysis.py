import sqlite3
import datetime


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
        log = data.execute(
            "select id, date(exetime), service, types, ip, username, password, command from FishPond Order By exetime "
            "Desc limit 5").fetchall()
    else:
        database = sqlite3.connect('../logger.db')
        data = database.cursor()
        log = data.execute(
            "select id, date(exetime), service, types, ip, username, password, command from FishPond where exetime > "
            "? Order By exetime Desc limit 5",
            (date,)).fetchall()
    return log


def get_ten_day():
    ten_day_list = []
    database = sqlite3.connect('../logger.db')
    data = database.cursor()
    for i in range(10):
        date = datetime.date.today() - datetime.timedelta(days=i)
        date_sum = {'date': str(date), 'ssh': 0, 'smtp': 0, 'ftp': 0, 'telnet': 0, 'rdp': 0, 'redis': 0, 'pop3': 0,
                    'tftp': 0}
        log = data.execute(
            "select date(exetime), service, count(*) from FishPond where date(exetime) = date('now', ?) GROUP "
            "BY service, date(exetime)", ('-' + str(i) + ' days',)).fetchall()
        for j in log:
            date_sum[j[1]] = j[2]
        ten_day_list.append(date_sum)
    return ten_day_list
