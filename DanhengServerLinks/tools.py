import requests
from datetime import datetime
import json
import urllib3
import traceback
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64

class Tools:
    base_url = 'https://localhost'
    exec_url = base_url + '/muip/exec_cmd'  # GET POST
    create_session_url = base_url + '/muip/create_session'  # POST
    auth_url = base_url + '/muip/auth_admin'  # POST
    server_info_url = base_url + '/muip/server_information'  # GET POST
    player_info_url = base_url + '/muip/player_information'  # GET POST

    memory_session_id = ''
    memory_expire_time = ''
    memory_rsa_public_key = ''

    def __init__(self, baseUrl: str):
        self.base_url = baseUrl
        self.exec_url = baseUrl + '/muip/exec_cmd'
        self.create_session_url = baseUrl + '/muip/create_session'
        self.auth_url = baseUrl + '/muip/auth_admin'
        self.server_info_url = baseUrl + '/muip/server_information'
        self.player_info_url = baseUrl + '/muip/player_information'

    # 发送Get请求
    def send_get_request(self, url, data=None, headers=None):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, json=data, headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.text
        except requests.exceptions.RequestException as e:
            return str(e)


    # 发送Post请求
    def send_post_request(self, url, data=None, headers=None):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.text
        except requests.exceptions.RequestException as e:
            return str(e)


    def login(self, token: str) -> str:
        send_session_data = {'key_type': 'PEM'}
        session_data = json.loads(self.send_post_request(self.create_session_url, send_session_data))
        if session_data['code'] != 0:
            return session_data['message']
        self.memory_session_id = session_data['data']['sessionId']
        self.memory_expire_time = session_data['data']['expireTimeStamp']
        self.memory_rsa_public_key = session_data['data']['rsaPublicKey']

        send_data = {'admin_key': self.rsa_encrypt(token, self.memory_rsa_public_key), 'session_id': self.memory_session_id}
        data = json.loads(self.send_post_request(self.auth_url, send_data))
        if data['code'] != 0:
            return data['message']
        return data['message']

    def exec(self, cmd: str, target: int, token: str) -> str:
        try:
            if self.memory_session_id == '' or self.memory_expire_time == '' or self.memory_rsa_public_key == '':
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            if datetime.now().timestamp() > int(self.memory_expire_time):
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            send_data = {
                'sessionId': self.memory_session_id,
                'command': self.rsa_encrypt(cmd, self.memory_rsa_public_key),
                'targetUid': target
            }
            data = json.loads(self.send_post_request(self.exec_url, send_data))
            if data['code'] != 0:
                return data['message']
            return base64.b64decode(data['data']['message']).decode('utf-8').strip()
        except Exception as e:
            return '出现错误: ' + str(e) + '\n堆栈：' + str(traceback.format_exc())

    def info(self, token: str):
        try:
            if self.memory_session_id == '' or self.memory_expire_time == '' or self.memory_rsa_public_key == '':
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            if datetime.now().timestamp() > int(self.memory_expire_time):
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            send_data = {
                'sessionId': self.memory_session_id
            }
            data = json.loads(self.send_post_request(self.server_info_url, send_data))
            return data
        except Exception as e:
            return '出现错误: ' + str(e) + '\n堆栈：' + str(traceback.format_exc())

    def player_info(self, uid: int, token: str):
        try:
            if self.memory_session_id == '' or self.memory_expire_time == '' or self.memory_rsa_public_key == '':
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            if datetime.now().timestamp() > int(self.memory_expire_time):
                login_result = self.login(token)
                if login_result != 'Authorized admin key successfully!':
                    return login_result
            send_data = {
                'sessionId': self.memory_session_id,
                'uid': uid
            }
            data = json.loads(self.send_post_request(self.player_info_url, send_data))
            return data
        except Exception as e:
            return '出现错误: ' + str(e) + '\n堆栈：' + str(traceback.format_exc())


    def rsa_encrypt(self, text, public_key_xml):
        pub_key = RSA.importKey(str(public_key_xml))
        cipher = PKCS1_cipher.new(pub_key)
        rsa_text = base64.b64encode(cipher.encrypt(bytes(text.encode("utf8"))))
        return rsa_text.decode('utf-8')
