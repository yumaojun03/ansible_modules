#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2015, zhi chuanxiu
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.


DOCUMENTATION = '''
---
module: zabbix_myapi
short_description: set user language and config email
description:
    - This module uses the Zabbix API to set user language config and config email
version_added: '1.0'
requirements: [ ]
options:
    user_lang:
        description:
            - Set user language.
        required: false
        default: en_GB
        choices: [ 'zh_CN', 'en_GB' ]
    smtp_server:
        description:
            - The email Server IP or hostname.
        required: false
        default: localhost
    smtp_helo:
        description:
            - The helo server.
        required: false
        default: localhost
    smtp_email:
        description:
            - which email adress you use to send mail.
        required: false
        default: zabbix@localhost.localdomain
    server_url:
        description:
            - Url of Zabbix server, with protocol (http or https) e.g.
              https://monitoring.example.com/zabbix. C(url) is an alias
              for C(server_url). If not set environment variable
              C(ZABBIX_SERVER_URL) is used.
        required: true
        default: null
        aliases: [ 'url' ]
    login_user:
        description:
            - Zabbix user name. If not set environment variable
              C(ZABBIX_LOGIN_USER) is used.
        required: true
        default: null
    login_password:
        description:
            - Zabbix user password. If not set environment variable
              C(ZABBIX_LOGIN_PASSWORD) is used.
        required: true
notes:
    - The module has been tested with Zabbix Server 2.4.
author: Zhi Chuanxiu
'''

EXAMPLES = '''
---
# Set the Admin user language: zh_CN
- name: set zabbix language to chinese and set email
  local_action:
     module: zabbix_myapi
     login_user: 'Admin'
     login_password: 'zabbix'
     server_url: 'http://192.168.10.134/zabbix/api_jsonrpc.php'
     set_user_lang: 'yes'

# Set email
- name: set zabbix language to chinese and set email
  local_action:
     module: zabbix_myapi
     login_user: 'Admin'
     login_password: 'zabbix'
     server_url: 'http://192.168.10.134/zabbix/api_jsonrpc.php'
     set_email: 'yes
'''


__author__ = 'chuanxiu'

from ansible.module_utils.basic import *

import json
import urllib2


class zabbix(object):
    ''' call zabbix api '''

    def __init__(self,user,passwd,url):
        self.zabbix_user = user
        self.zabbix_pass = passwd
        self.url = url
        self.header = {"Content-Type" : "application/json"}

    def auth(self):
        ''' auth'''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.zabbix_user,
                    "password": self.zabbix_pass
                },
                "id": 0,
            }
        )

        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])

        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "Auth Failed,Please Check You Name And Password: %s" %(str(e))
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']

    def logout(self,authid):
        '''logout'''
        data = json.dumps(
            {
                "jsonrpc" : "2.0",
                "method" : "user.logout",
                "params" : [],
                "id" : 0,
                "auth" : authid
            }
        )

        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])

        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "Logout Failed: %s" %(str(e))
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']

    def get_log_user_id(self, authid, ):
        ''' update user lang to chinese'''
        data = json.dumps(
            {
                "jsonrpc" : "2.0",
                "method" : "user.get",
                "params" : {
                    "output" : ["surname", "alias", "userid"],
                },
                "auth" : authid,
                "id" : 7,
            }
        )
        request = urllib2.Request(self.url,data)
        for key in  self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "Update user failed: %s" % (str(e))
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']

    def update_user_lang(self, authid, userid, lang):
        ''' get user id form user group'''
        data = json.dumps(
            {
                "jsonrpc" : "2.0",
                "method" : "user.update",
                "params" : {
                    "userid" : userid,
                    "lang" : lang
                },
                "auth" : authid,
                "id" : 7,
            }
        )
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "get user infomation failed: %s" % ( str(e) )
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']


    def get_media_type_id(self, authid, ):
        ''' update user lang to chinese'''
        data = json.dumps(
            {
                "jsonrpc" : "2.0",
                "method" : "mediatype.get",
                "params" : {
                    "output" : ["mediatypeid", "description"]
                },
                "auth" : authid,
                "id" : 8,
            }
        )
        request = urllib2.Request(self.url,data)
        for key in  self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "Update user failed: %s" % (str(e))
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']

    def update_media_email(self, authid, emailtypeid, smtp_server, smtp_helo, smtp_email ):
        ''' update user lang to chinese'''
        data = json.dumps(
            {
                "jsonrpc" : "2.0",
                "method" : "mediatype.update",
                "params" : {
                     "mediatypeid" : emailtypeid,
                     "smtp_server" : smtp_server,
                     "smtp_helo" : smtp_helo,
                     "smtp_email" : smtp_email,
                     "status" : 0
                },
                "auth" : authid,
                "id" : 8,
            }
        )
        request = urllib2.Request(self.url,data)
        for key in  self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception,e:
            print "Update user failed: %s" % (str(e))
        else:
            response = json.loads(result.read())
            result.close()
        return response['result']


def update_lang(user, password, url, username, lang):
    zbx = zabbix(user, password, url)
    authid = zbx.auth()
    print "Auth Successful. The Auth ID IS: %s" %(authid)

    for i in  zbx.get_log_user_id(authid):
        if i['alias'] == username:
            userid = i['userid']
    print "the %s userid is: %s." % ( username, userid)
    response = zbx.update_user_lang(authid, userid, lang)
    if response['userids']:
        print "success!"
    else:
        print "Failed!"

    print "Logout : %s" %(zbx.logout(authid))

def update_email(user, password, url, smtp_server, smtp_helo, smtp_email):
    zbx = zabbix(user, password, url)
    authid = zbx.auth()
    print "Auth Successful. The Auth ID IS: %s" %(authid)    

    for i in zbx.get_media_type_id(authid):
        if i["description"] == "Email":
            emailtypeid = i["mediatypeid"]
    print "the Email typeid is: %s." % ( emailtypeid )    
    response = zbx.update_media_email(authid, emailtypeid, smtp_server, smtp_helo,smtp_email)
    if response['mediatypeids']:
        print "success!"
    else:
        print "Failed!"

    print "Logout : %s" %(zbx.logout(authid))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            server_url=dict(required=True, aliases=['url']),
            login_user=dict(required=True),
            login_password=dict(required=True),

            set_user_lang=dict(required=False,default='no'),
            user_name=dict(required=False,default='Admin'),
            user_lang=dict(required=False, default='zh_CN'),

            set_email=dict(required=False,default='no'),
            smtp_server=dict(required=False, default='localhost'),
            smtp_helo=dict(required=False, default='localhost'),
            smtp_email=dict(required=False, default='zabbix@localhost.localdomain'),
        ),
        supports_check_mode=True
    )


    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']

    set_user_lang = module.params['set_user_lang']
    user_name = module.params['user_name']
    user_lang = module.params['user_lang']
    
    set_email = module.params['set_email']
    smtp_server = module.params['smtp_server']
    smtp_helo = module.params['smtp_helo']
    smtp_email = module.params['smtp_email']

    if set_user_lang == 'yes':
        update_lang(login_user, login_password, server_url, user_name, user_lang)
    else:
         module.exit_json(changed=False)

    if set_email == 'yes':
        update_email(login_user, login_password, server_url, smtp_server, smtp_helo, smtp_email)
    else:
         module.exit_json(changed=False)
    module.exit_json(changed=True, result="Successfully user: %s, language: %s.\n Successfully mail_server: %s, mail_helo: %s, mail_addr: %s." % (user_name, user_lang,smtp_server, smtp_helo, smtp_email))
        
main()
