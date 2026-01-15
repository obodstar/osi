import hashlib
import time
import calendar
import json
import requests
import re


class instagram:
    def __init__(self):
        self.ses = requests.Session()

    def logins(self, users, password):
        andro = "android-%s" % hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        current_GMT = time.gmtime(time.time())
        times = calendar.timegm(current_GMT)

        headers = {
            "Host": "i.instagram.com",
            "X-Ig-App-Locale": "in_ID",
            "X-Ig-Device-Locale": "in_ID",
            "X-Ig-Mapped-Locale": "id_ID",
            "X-Pigeon-Session-Id": "UFS-1426cbfe-c780-440c-8ddb-6a94f4fd42ba-2",
            "X-Pigeon-Rawclienttime": "1692350444.353",
            "X-Bloks-Version-Id": "4cf8328dae765ededd07d166b6774eeb1eb23c13979a715d6bd2ea9d06bb0560",
            "X-Ig-Www-Claim": "0",
            "X-Bloks-Is-Layout-Rtl": "false",
            "X-Ig-Device-Id": "1d8f57a3-4663-4426-95ff-6e9b2b0208a4",
            "X-Ig-Family-Device-Id": "90b2fcbe-bec9-4c90-ad54-d32f285041bf",
            "X-Ig-Android-Id": andro,
            "X-Ig-Capabilities": "3brTv10=",
            "X-Ig-App-Id": "567067343352427",
            "Priority": "u=3",
            "User-Agent": (
                "Instagram 294.0.0.33.87 Android "
                "(25/7.1.2; 320dpi; 900x1600; samsung; "
                "SM-G965N; star2lte; samsungexynos9810; in_ID; 500160599)"
            ),
            "Accept-Language": "id-ID, en-US",
            "Ig-Intended-User-Id": "0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Fb-Http-Engine": "Liger",
            "X-Fb-Client-Ip": "True",
            "X-Fb-Server-Cluster": "True",
        }

        data = {
            "params": (
                f'{{"client_input_params":{{'
                f'"password":"#PWD_INSTAGRAM:0:{times}:{password}",'
                f'"contact_point":"{users}",'
                f'"event_flow":"login_manual",'
                f'"login_attempt_count":1,'
                f'"device_id":"{andro}",'
                f'"auth_secure_device_id":""}},'
                f'"server_params":{{'
                f'"is_caa_perf_enabled":1,'
                f'"is_platform_login":0,'
                f'"qe_device_id":"1d8f57a3-4663-4426-95ff-6e9b2b0208a4",'
                f'"should_trigger_override_login_2fa_action":0,'
                f'"reg_flow_source":"aymh_single_profile_native_integration_point",'
                f'"credential_type":"password",'
                f'"username_text_input_id":"dqtoxa:47",'
                f'"password_text_input_id":"dqtoxa:48",'
                f'"INTERNAL_INFRA_THEME":"harm_f",'
                f'"device_id":"{andro}",'
                f'"server_login_source":"login",'
                f'"should_trigger_override_login_success_action":0}}}}'
            ),
            "bk_client_context": (
                '{"bloks_version":"4cf8328dae765ededd07d166b6774eeb1eb23c13979a715d6bd2ea9d06bb0560",'
                '"styles_id":"instagram"}'
            ),
            "bloks_versioning_id": "4cf8328dae765ededd07d166b6774eeb1eb23c13979a715d6bd2ea9d06bb0560",
        }

        response = self.ses.post(
            "https://i.instagram.com/api/v1/bloks/apps/"
            "com.bloks.www.bloks.caa.login.async.send_login_request/",
            headers=headers,
            data=data,
        ).text

        if "logged_in_user" in str(response):
            bearer = re.search('"Bearer (.*?)"', response).group(1).replace("\\", "")
            print("Bearer ", bearer)

        elif "redirect_checkpoint" in str(response):
            print(" [•] Akun Terkena Checkpoint....")
            time.sleep(2)
            exit()


if __name__ == "__main__":
    users = input("[+] Masukan Username : ")
    password = input("[+] Masukan Password : ")
    mo = instagram()
    mo.logins(users, password)
