# -----------------------------------------------------------
# Library to login to xiaomi cloud and get device info.
#
# (C) 2020 Sammy Svensson
# Released under MIT License
# email sammy@ssvensson.se
# -----------------------------------------------------------

import http.client, http.cookies
import json
import hashlib
import logging
import time, locale, datetime
import tzlocal
import requests

from micloud import miutils
from micloud.micloudexception import MiCloudException


class MiCloud():

    def __init__(self, username, password):
        super().__init__()
        self.user_id =       None
        self.service_token = None
        self.session =       None
        self.ssecurity =     None
        self.cuser_id =      None
        self.pass_token =    None

        self.failed_logins = 0 

        self.agent_id = miutils.get_random_agent_id()
        self.useragent = "Android-7.1.1-1.0.0-ONEPLUS A3010-136-" + self.agent_id + " APP/xiaomi.smarthome APPV/62830"
        self.locale = locale.getdefaultlocale()[0]

        timezone = datetime.datetime.now(tzlocal.get_localzone()).strftime('%z')
        timezone = "GMT{0}:{1}".format(timezone[:-2], timezone[-2:])
        self.timezone = timezone

        self.default_server = 'de' # Sets default server to Europe.
        self.username = username
        self.password = password
        if not self._check_credentials():
            raise MiCloudException("username or password can't be empty")

        self.client_id = miutils.get_random_string(6)


    def get_token(self):
        """Return the servie token if you have successfully logged in."""
        return self.service_token

    def _check_credentials(self):
        return (self.username and self.password)

    
    def login(self):
        """Login in to Xiaomi cloud.

        :return: True if login successful, False otherwise.
        """
        if not self._check_credentials():
            return False

        if self.user_id and self.service_token:
            return True

        logging.debug("Xiaomi logging in with userid %s", self.username)
        try:
            if self._login_request():
                self.failed_logins = 0
            else:
                self.failed_logins += 1
                logging.debug("Xiaomi cloud login attempt %s", self.failed_logins)
        except MiCloudException as e:
            logging.info("Error logging on to Xiaomi cloud (%s): %s", self.failed_logins, str(e))
            self.failed_logins += 1
            self.service_token = None
            if self.failed_logins > 10:
                logging.info("Repeated errors logging on to Xiaomi cloud. Cleaning stored cookies")
                self.self._init_session(reset=True)
            return False
        except:
            logging.exception("Unknown exception occurred!")
            return False

        return True


    def _login_request(self):
        try:
            self._init_session()
            sign = self._login_step1()
            if not sign.startswith('http'):
                location = self._login_step2(sign)
            else:
                location = sign # we already have login location

            response3 = self._login_step3(location)
            if response3.status_code == 403:
                raise MiCloudException("Access denied. Did you set the correct api key and/or username?")
            elif response3.status_code == 200:
                logging.debug("Your service token: %s", self.service_token)
                return True
            else:
                logging.debug("request returned status '%s', reason: %s, content: %s", response3.status_code,
                    response3.reason, response3.text)
                raise MiCloudException(response3.status_code + response3.reason)
        except Exception as e:
            raise MiCloudException("Cannot logon to Xiaomi cloud: " + str(e))


    def _init_session(self, reset=False):
        if not self.session or reset:
            self.session = requests.Session()
            self.session.headers.update({'User-Agent': self.useragent})
            self.session.cookies.update({
                'sdkVersion': '3.8.6',
                'deviceId': self.client_id
            })
    

    def _login_step1(self):
        logging.debug("Xiaomi login step 1")

        url = "https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true"
        self.session.cookies.update({'userId': self.user_id if self.user_id else self.username})
        response = self.session.get(url)
        response_json = json.loads(response.text.replace("&&&START&&&", ""))

        logging.debug("Xiaomi login step 1 response code: %s", response.status_code)
        logging.debug("Xiaomi login step 1 response: %s", json.dumps(response_json))

        try:
            if "_sign" in response_json:
                sign = response_json["_sign"]
                logging.debug("Xiaomi login step 1 sign: %s", sign)
                return sign
            else:
                logging.debug("Xiaomi login _sign missing. Maybe still has login cookie.")
                return ""

        except Exception as e:
            raise MiCloudException("Error getting logon sign. Cannot parse response.", e)


    def _login_step2(self, sign):
        logging.debug("Xiaomi login step 2")

        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        post_data = {
            'sid': "xiaomiio",
            'hash': hashlib.md5(self.password.encode()).hexdigest().upper(),
            'callback': "https://sts.api.io.mi.com/sts",
            'qs': '%3Fsid%3Dxiaomiio%26_json%3Dtrue',
            'user': self.username,
            '_json': 'true'
        }
        if sign:
            post_data['_sign'] = sign

        response = self.session.post(url, data = post_data)
        response_json = json.loads(response.text.replace("&&&START&&&", ""))

        logging.debug("Xiaomi login step 2 response code: %s", response.status_code)
        logging.debug("Xiaomi login step 2 response: %s", json.dumps(response_json))

        self.user_id = response_json['userId']
        self.ssecurity = response_json['ssecurity']
        self.cuser_id = response_json['cUserId']
        self.pass_token = response_json['passToken']

        location = response_json['location']
        code = response_json['code']

        logging.debug("Xiaomi login ssecurity: %s", self.ssecurity)
        logging.debug("Xiaomi login userId: %s", self.user_id)
        logging.debug("Xiaomi login cUserId: %s", self.cuser_id)
        logging.debug("Xiaomi login passToken: %s", self.pass_token)
        logging.debug("Xiaomi login location: %s", location)
        logging.debug("Xiaomi login code: %s", code)

        if location:
            return location
        else:
            raise MiCloudException("Error getting logon location URL. Return code: " + code)


    def _login_step3(self, location):
        logging.debug("Xiaomi login step 3 @ %s", location)

        self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        response = self.session.get(location)

        logging.debug("Xiaomi login step 3 content: %s", response.text)
        logging.debug("Xiaomi login step 3 status code: %s", response.status_code)

        service_token = response.cookies['serviceToken']
        if service_token:
            self.service_token = service_token
        
        return response


    def get_devices(self, country=None, raw=False, save=False, file="devices.json"):
        """Get a list with information about all devices.

        :param country: country code for the server. Default: "de" (Europe)
        :param raw: Return raw result from server instead of a python list.
        :param save: Save information to json file. Default: False
        :param file: json file to save to.
        :return: List of devices
        :rtype: list
        """

        if not country:
            country = self.default_server
        
        response = self._get_device_string(country)
        if not response:
            return None

        devicesList = {}
        try:
            json_resp = json.loads(response)
            logging.debug('Devices data: %s', response)

            if save:
                f = open("devices.json", "w")
                f.write(json.dumps(json_resp['result'], indent=4, sort_keys=True))
                f.close()

            if raw:
                return response
            else:
                return json_resp['result']['list']
        except ValueError as e:
            logging.info("Error while parsing devices: %s", str(e))


    def download_vacuum_map(self, country=None, map_id=None):

         if not country:
                 country = self.default_server

         url = self._get_api_url(country) + "/home/getmapfileurl"
         params = {'data': "{\"obj_name\":\"" + map_id + "\"}"}
         try:
            resp = self.request(url, params)
            print("Get vacuumMap response: %s", resp)
            if len(resp) > 2:
                json_resp = json.loads(resp)
                if not json_resp['result'] is None:
                  self._download_map(json_resp['result']['url'])
                  return resp
                else:
                  logging.error("%s", str(json_resp))
         except MiCloudException as e:
            logging.error("%s", str(e))
         return None

    def _download_map(self, url=None):
         try:
            logging.debug("Try download map")
            resp = requests.get(url, auth=(self.username, self.password))

            logging.debug("Get vacuumMap response: %s", resp)
            if (resp.status_code == 200):

               open("map.rrmap", 'wb').write(resp.content)
               logging.debug('RRMap file %s successfully Downloaded: ',"map.rrmap")
               return resp
         except MiCloudException as e:
            logging.error("%s", str(e))
         return None

    def _get_device_string(self, country):
        if not country:
            country = self.default_server
        
        url = self._get_api_url(country) + "/home/device_list"
        params = {'data': "{\"getVirtualModel\":false,\"getHuamiDevices\":0}"}
        try:
            resp = self.request(url, params)
            logging.debug("Get devices response: %s", resp)
            if len(resp) > 2:
                return resp
        except MiCloudException as e:
            logging.error("%s", str(e))
        return None


    def _get_api_url(self, country):
        return "https://" + ("" if country.strip().lower() ==  "cn" else country.strip().lower() + ".") + "api.io.mi.com/app"


    def request_country(self, url_part, country, params):        
        url = self._get_api_url(country) + url_part
        response = self.request(url, params)
        logging.debug("Request to %s server %s. Response: %s", country, url_part, response)
        return response


    def request(self, url, params):
        if not self.service_token or not self.user_id:
            raise MiCloudException("Cannot execute request. service token or userId missing. Make sure to login.")

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.useragent})

        logging.debug("Send request: %s to %s", params['data'], url)
        self.session.headers.update({
            'x-xiaomi-protocal-flag-cli': 'PROTOCAL-HTTP2',
            'content-type': 'application/x-www-form-urlencoded'
        })
        self.session.cookies.update({
            'userId': str(self.user_id),
            'yetAnotherServiceToken': self.service_token,
            'serviceToken': self.service_token,
            'locale': str(self.locale),
            'timezone': str(self.timezone),
            'is_daylight': str(time.daylight),
            'dst_offset': str(time.localtime().tm_isdst*60*60*1000),
            'channel': 'MI_APP_STORE'
        })
        for c in self.session.cookies:
            logging.debug('Cookie: %s', c)

        try:
            nonce = miutils.gen_nonce()
            signed_nonce = miutils.signed_nonce(self.ssecurity, nonce)
            signature = miutils.gen_signature(url.replace("/app", ""), signed_nonce, nonce, params)

            post_data = {
                'signature': signature,
                '_nonce': nonce,
                'data': params['data']
            }
            
            response = self.session.post(url, data = post_data)
            if response.status_code == 403:
                self.service_token = None

            return response.text
        except requests.exceptions.HTTPError as e:
            self.service_token = None
            logging.exception("Error while executing request to %s :%s", url, str(e))
        except MiCloudException as e:
            logging.exception("Error while decrypting response of request to %s :%s", url, str(e))
        except Exception as e:
            logging.exception("Error while executing request to %s :%s", url, str(e))
