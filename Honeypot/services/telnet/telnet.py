import sys
sys.path.append('..')
import logging
import telnetlib
import time


class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()

    def login_host(self,host_ip,username,password):
        try:
            self.tn.open(host_ip,port=23)
        except:
            logging.warning('%sfail'%host_ip)
            return False

        self.tn.read_until(b'login: ',timeout=20)
        self.tn.write(username.encode('ascii') + b'\n')

        self.tn.read_until(b'Password: ',timeout=20)
        self.tn.write(password.encode('ascii') + b'\n')

        time.sleep(2)
        
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logging.warning('%ssuccess'%host_ip)
            return True
        else:
            logging.warning('%sfail'%host_ip)
            return False

    def execute_some_command(self,command):
      
        self.tn.write(command.encode('ascii')+b'\n')
        time.sleep(2)
    
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.warning('result：\n%s' % command_result)


    def logout_host(self):
        self.tn.write(b"exit\n")


