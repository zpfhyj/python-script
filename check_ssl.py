#!/usr/bin/env python3
from _datetime import datetime
from urllib3.contrib import pyopenssl
import sys
import os
def get_expire(domain):
    try:
        conn = pyopenssl.ssl.create_connection((domain, 443))
        sock = pyopenssl.ssl.SSLContext(pyopenssl.ssl.PROTOCOL_SSLv23).wrap_socket(conn, server_hostname=domain)

        certificate = pyopenssl.ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
        data = pyopenssl.OpenSSL.crypto.load_certificate(pyopenssl.OpenSSL.crypto.FILETYPE_PEM, certificate)

        expire_time = datetime.strptime(data.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')
        expire_days = (expire_time - datetime.now()).days

        return True, 200, {'expire_time': str(expire_time), 'expire_days': expire_days}
    except Exception as e:
        return False, 500, str(e)

#if __name__ == '__main__':
#    print(get_expire('ci.doushen-int.com'))
if __name__ == '__main__':
    for I in range(1,len(sys.argv)):
        #print(get_expire(sys.argv[I]))
        a=get_expire(sys.argv[I])
        d=(a[2])
        #print(type(d))
        if d['expire_days'] <10:
            info=sys.argv[I]+"证书剩余"+str(d['expire_days'])+",需要更新"
            os.system('echo %s | mail -s "证书到期" xxx@qq.com'  % (info))
            #print(sys.argv[I])
