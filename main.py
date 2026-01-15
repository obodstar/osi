import os, requests, numpy as np, json, random, hashlib, time, uuid, cv2
from PIL import Image

def image_to_video(image_path, output_path=False, basename='output.mp4', duration=5, fps=30):
    if output_path and basename.endswith('.mp4'):
        img = Image.open(image_path)
        frame = np.array(img)
        height, width, _ = frame.shape

        folders = output_path + '\\results\\' + basename
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename=folders, fourcc=fourcc, fps=fps, frameSize=(width, height))

        frame_count = int(duration * fps)
        for _ in range(frame_count):
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        print(f"[✓] Video created: {output_path}")
    else:
        print("[✗] Please provide a valid folder path to save the video.")
    
class PostBeranda:
    def __init__(self):
        self.r = requests.Session()
        self.timezone_offset = str(-time.timezone)
        self.android = "android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16]
        self.DeviceID = str(uuid.uuid4())
        self.FamilyDeviceId = str(uuid.uuid4())
        self.ListAudio = []
        self.headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'in_ID',
            'X-Ig-Device-Locale': 'in_ID',
            'X-Ig-Mapped-Locale': 'id_ID',
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': self.DeviceID, #'46cc076a-a663-4755-8ac2-dbf8dbf56787',
            'X-Ig-Family-Device-Id': self.FamilyDeviceId, #'db8b380b-8758-4fcb-bd2c-7a848be6a14e',
            'X-Ig-Android-Id': self.android,
            'X-Ig-Timezone-Offset': self.timezone_offset,
            'Retry_context': json.dumps({"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}),
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:eyJkc191c2VyX2lkIjoiNzQ2NzA0MDIyNTUiLCJzZXNzaW9uaWQiOiI3NDY3MDQwMjI1NSUzQVVMVVpibHBmMDd1S2hhJTNBNCUzQUFZaXAyNDZTQy0yemlhYXN5YzNNM093OHRYOHdWdzkwWTJNdC1kOVFVdyJ9',
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        self.headersGET = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'in_ID',
            'X-Ig-Device-Locale': 'in_ID',
            'X-Ig-Mapped-Locale': 'id_ID',
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': self.DeviceID,
            'X-Ig-Family-Device-Id': self.FamilyDeviceId,
            'X-Ig-Android-Id': self.android,
            'X-Ig-Timezone-Offset': self.timezone_offset,
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:eyJkc191c2VyX2lkIjoiNzQ2NzA0MDIyNTUiLCJzZXNzaW9uaWQiOiI3NDY3MDQwMjI1NSUzQVVMVVpibHBmMDd1S2hhJTNBNCUzQUFZaXAyNDZTQy0yemlhYXN5YzNNM093OHRYOHdWdzkwWTJNdC1kOVFVdyJ9',
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

    def GetListMusic(self):
        response = self.r.get('https://i.instagram.com/api/v1/feed/saved/audio/', headers=self.headersGET, allow_redirects=True).json().get('items')
        for items in response:
            track = items["track"]
            audio_cluster_id = track.get('audio_cluster_id')
            audio_asset_id   = track.get('audio_asset_id')
            self.ListAudio.append(f'{audio_cluster_id}|{audio_asset_id}')

    def UploadPicture(self, LocationPath: str = False):
        with open(LocationPath, 'rb') as f:
            data_photo = f.read()
            self.file_size  = str(len(data_photo))
        f.close()

        img = Image.open(LocationPath)
        self.width, self.height = img.size

        self.upload_id = str(int(time.time() * 1000))
        UploadID = f'{self.upload_id}_0_{random.randint(1000000000, 9999999999)}'
        
        Rupload = {
            "retry_context": json.dumps({
                "num_step_auto_retry":0,
                "num_reupload":0,
                "num_step_manual_retry":0
            }),
            "media_type":"1",
            "upload_id":self.upload_id,
            "sticker_burnin_params":"[]",
            "xsharing_user_ids":"[]",
            "image_compression": json.dumps({
                "lib_name": "moz",
                "lib_version": "3.1.m",
                "quality": "80"
            })
        }
        headers = {
            'Host': 'i.instagram.com',
            'X_fb_photo_waterfall_id': str(uuid.uuid4()), #'8c18e3e8-4931-4bf7-9085-9236b0e39ac8',
            'X-Entity-Type': 'image/jpeg',
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps(Rupload),
            'X-Entity-Name': UploadID,
            'X-Entity-Length': '41332',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:eyJkc191c2VyX2lkIjoiNzQ2NzA0MDIyNTUiLCJzZXNzaW9uaWQiOiI3NDY3MDQwMjI1NSUzQVVMVVpibHBmMDd1S2hhJTNBNCUzQUFZaXAyNDZTQy0yemlhYXN5YzNNM093OHRYOHdWdzkwWTJNdC1kOVFVdyJ9',
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Content-Type': 'application/octet-stream',
            'Content-Length': self.file_size,
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        response = self.r.post('https://i.instagram.com/rupload_igphoto/{}'.format(UploadID), headers=headers, data=data_photo, allow_redirects=True).json()
        self.UploadId = response.get('upload_id')
        print(self.UploadId)
        if self.UploadId:
            return True
    
    def UploadPhotoPost(self, caption: str = False):
        audio_cluster_id, audio_asset_id = str(random.choice(self.ListAudio)).split('|')
        head = self.headers.copy()
        head.update({'Content-Length': str(self.file_size)})
        json_data = {
            "camera_entry_point": "360",
            "camera_session_id": str(uuid.uuid4()),#"22111cd2-730d-4437-924e-fb5ed204d399",
            "scene_capture_type": "",
            "timezone_offset": self.timezone_offset,
            "source_type": "4",
            'upload_id': str(self.upload_id),
            "_uid": "74670402255",
            "device_id": self.android,
            "_uuid": self.DeviceID, #"46cc076a-a663-4755-8ac2-dbf8dbf56787",
            "caption": caption,
            "device": {
                "manufacturer": "Google",
                "model": "google Pixel 2",
                "android_version": 25,
                "android_release": "7.1.2"
            },
            "edits": {
                "crop_original_size": [float(self.width), float(self.height)],
                "crop_center": [0.0, -0.0],
                "crop_zoom": 1.0
            },
            "extra": {
                "source_width" : int(self.width),
                "source_height": int(self.height)
            },
            "music_params": {
                "audio_cluster_id": audio_cluster_id,
                "audio_asset_id": audio_asset_id,
                "audio_asset_start_time_in_ms": 56000,
                "derived_content_start_time_in_ms": 0,
                "overlap_duration_in_ms": 30000,
                "browse_session_id": str(uuid.uuid4()), #"8c18e3e8-4931-4bf7-9085-9236b0e39ac8",
                "product": "music_in_feed"
            }
        }
        data = {'signed_body': f'SIGNATURE.{json.dumps(json_data)}'}
        print(data)
        print()
        response = self.r.post('https://i.instagram.com/api/v1/media/configure/', headers=head, data=data, allow_redirects=True).text.replace('\\', '')
        print(response)

class PostReels:
    def __init__(self, cookie):
        self.r = requests.Session()
        self.cookie = cookie
        self.ListAudio = []
        self.timezone_offset = str(-time.timezone)
        self.android = "android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16]
        self.DeviceID = str(uuid.uuid4())
        self.FamilyDeviceId = str(uuid.uuid4())
        self.headersGET = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'in_ID',
            'X-Ig-Device-Locale': 'in_ID',
            'X-Ig-Mapped-Locale': 'id_ID',
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': self.DeviceID,
            'X-Ig-Family-Device-Id': self.FamilyDeviceId,
            'X-Ig-Android-Id': self.android,
            'X-Ig-Timezone-Offset': self.timezone_offset,
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

    def generate_thumbnail_current_time(self, video_path: str = False, output_path: str = False):
        if video_path.endswith('.mp4'):
            time_seconds = 6 #now.hour * 3600 + now.minute * 60 + now.second
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.video_duration = frame_count / fps
            print(f"[•] Video duration: {self.video_duration} seconds", end='\n')
            if time_seconds > self.video_duration:
                time_seconds = time_seconds % self.video_duration
            frame_number = int(time_seconds * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = cap.read()

            self.VideoWidth  = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self.VideoHeight = str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            if success:
                cv2.imwrite(output_path, frame)
            else:
                print("[✗] Failed to generate thumbnail")
            cap.release()
        elif video_path.endswith('.jpeg'):
            img = Image.open(video_path)
            self.VideoWidth, self.VideoHeight = img.size
            self.video_duration = os.path.getsize(video_path)

    def GetListMusic(self):
        resp = self.r.get('https://i.instagram.com/api/v1/feed/saved/audio/', headers=self.headersGET, allow_redirects=True).json()
        response = resp.get('items')
        for items in response:
            track = items["track"]
            audio_asset_id   = track.get('audio_asset_id')
            audio_cluster_id = track.get('audio_cluster_id')
            progressive_download_url = track.get('progressive_download_url')
            duration_in_ms = track.get('duration_in_ms')
            dash_manifest = track.get('dash_manifest')
            highlight_start_times_in_ms = track.get('highlight_start_times_in_ms')
            title = track.get('title')
            display_artist = track.get('display_artist')
            cover_artwork_uri = track.get('cover_artwork_uri')
            cover_artwork_thumbnail_uri = track.get('cover_artwork_thumbnail_uri')
            is_explicit = track.get('is_explicit')
            has_lyrics = track.get('has_lyrics')
            allows_saving = track.get('allows_saving')
            is_bookmarked = track.get('metadata').get('is_bookmarked')
            self.ListAudio.append(f'{audio_asset_id}|{audio_cluster_id}|{progressive_download_url}|{duration_in_ms}|{dash_manifest}|{highlight_start_times_in_ms}|{title}|{display_artist}|{cover_artwork_uri}|{cover_artwork_thumbnail_uri}|{is_explicit}|{has_lyrics}|{allows_saving}|{is_bookmarked}')
        
    def OpenFiles(self, path):
        with open(path, 'rb') as f:
            self.data = f.read()
            self.file_size = len(self.data)
            self.md5hash = hashlib.md5(self.data).hexdigest()
        f.close()
        
    def SendVideo(self):
        self.Upload_ID = str(int(time.time()) * 1000)
        Rupload = {
            "upload_media_height":self.VideoHeight,
            "xsharing_user_ids":"[]",
            "upload_media_width":self.VideoWidth,
            "is_clips_video":"1",
            "upload_media_duration_ms":str(int(self.video_duration * 1000)),
            "content_tags":"use_default_cover",
            "upload_id":self.Upload_ID,
            "retry_context":json.dumps({"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}),
            "media_type":"2",
            "sticker_burnin_params":"[]"
        }
        headers = {
            'Host': 'i.instagram.com',
            'Segment-Start-Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps(Rupload),
            'Offset': '0',
            'X-Entity-Name': '{}-0-{}-lessO-{}'.format(self.md5hash, self.file_size, self.Upload_ID),
            'X-Entity-Length': str(self.file_size),
            'Segment-Type': '3',
            'X-Entity-Type': 'video/mp4',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(self.file_size),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        response = self.r.post('https://i.instagram.com/rupload_igvideo/{}'.format(headers['X-Entity-Name']), headers=headers, data=self.data, allow_redirects=True).json()
        print(response)
        print()
        
    def UploadPicture(self, LocationPath: str = False):
        # self.OpenFiles(path=LocationPath)
        img = Image.open(LocationPath)
        self.width, self.height = img.size
        self.file_size = os.path.getsize(LocationPath)

        UploadID = f'{self.Upload_ID}_0_{random.randint(1000000000, 9999999999)}'
        
        Rupload = {
            "retry_context": json.dumps({"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}),
            "media_type":"2",
            "upload_id":self.Upload_ID,
            "sticker_burnin_params":"[]",
            "xsharing_user_ids":"[]",
            "image_compression": json.dumps({
                "lib_name": "moz",
                "lib_version": "3.1.m",
                "quality": "80",
                "original_width":1080,
                "original_height":1920
            })
        }
        headers = {
            'Host': 'i.instagram.com',
            'X_fb_photo_waterfall_id': str(uuid.uuid4()), #'8c18e3e8-4931-4bf7-9085-9236b0e39ac8',
            'X-Entity-Type': 'image/jpeg',
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps(Rupload),
            'X-Entity-Name': UploadID,
            'X-Entity-Length': str(self.file_size),
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(self.file_size),
            'X-Fb-Http-Engine': 'Liger',
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        response = self.r.post('https://i.instagram.com/rupload_igphoto/{}'.format(UploadID), headers=headers, data=self.data, allow_redirects=True).json()
        self.UploadId = response.get('upload_id')
        print(response)
        print()

    def UploadVideos(self):
        self._uuid = str(uuid.uuid4())
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'in_ID',
            'X-Ig-Device-Locale': 'in_ID',
            'X-Ig-Mapped-Locale': 'id_ID',
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': self._uuid,
            'X-Ig-Family-Device-Id': str(uuid.uuid4()),
            'X-Ig-Android-Id': "android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16],
            'X-Ig-Timezone-Offset': self.timezone_offset,
            'Is_clips_video': '1',
            'Retry_context': '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; Google/google; google Pixel 2; x86; android_x86; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': '74670402255',
            'Ig-Intended-User-Id': '74670402255',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(self.file_size),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

        params = {'video': '1'}
        dat  = {
            "clips_share_preview_to_feed":"0", # Share To Feed 1 no 2 not Share
            "is_clips_edited":"0",
            "like_and_view_counts_disabled":"0",
            "camera_entry_point":"360",
            "tap_models":json.dumps([{
                "x":0.0,
                "y":0.0,
                "z":0,
                "width":0.0,
                "height":0.0,
                "rotation":0.0,
                "type":"music",
                "tag":str(uuid.uuid4()), #"f1a79777-ce78-4cd3-baca-d22e325c833b",
                "audio_asset_start_time_in_ms":43000,
                "audio_asset_suggested_start_time_in_ms":43000,
                "derived_content_start_time_in_ms":0,
                "overlap_duration_in_ms":15000,
                "browse_session_id":str(uuid.uuid4()), #"19dd27ad-4d36-44d8-9c32-537507d30b58",
                "music_product":"clips_camera_format_v2",
                "audio_asset_id":"1259893491830958",
                "audio_cluster_id":"438044872418006",
                "progressive_download_url":"https://instagram.fcgk38-1.fna.fbcdn.net/o1/v/t2/f2/m69/AQOmnm0OXcb8sfANip3_zXdXxIX86bTRXxxS6HhiHv4KsqKB-zw7vb4eYBAbUkeHjVyf8hSxgBe2QlXorit1rNTq.mp4?strext=1&_nc_cat=1&_nc_oc=AdkvIO8g79dPQ9as5jSFp7ssThEl7vAu8bA00XcOzJfysRr6A-qnKX7TDoUukXZCpOs&_nc_sid=5e9851&_nc_ht=instagram.fcgk38-1.fna.fbcdn.net&_nc_ohc=StVW05Yi33IQ7kNvwE9QHR5&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5BVURJT19PTkxZLi5DMy4wLmRhc2hfbG5faGVhYWNfdmJyM19tcHhfYXVkaW8iLCJ4cHZfYXNzZXRfaWQiOjU1MDk5MTgyMDk4Nzc2MiwiYXNzZXRfYWdlX2RheXMiOjM1MCwidmlfdXNlY2FzZV9pZCI6MTA1NjgsImR1cmF0aW9uX3MiOjIxNiwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=17-1&vs=ce5b6616be103b17&_nc_vs=HBkcFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HSXBZSXlDVFdJakxPcm9DQU5oVE9JS0NfNnNNYm1FeUFBQUYVAgLIARIAKAAYABsCiAd1c2Vfb2lsATEScHJvZ3Jlc3NpdmVfcmVjaXBlATEVAAAm5PWc_PjH-gEVAigCQzMsF0BrGi0OVgQZGBxkYXNoX2xuX2hlYWFjX3ZicjNfbXB4X2F1ZGlvEQB1AGWQpQEA&_nc_zt=28&oh=00_Afdq4u521saryQyhz8moXzRLqNAV0RBXPsg0kBTedX-E_Q&oe=690AB50C",
                "duration_in_ms":216818,
                "dash_manifest":dash_manifest,
                "highlight_start_times_in_ms":[43000,90500,28000],
                "title":"Semanis Kamu",
                "display_artist":"Willy Anggawinata",
                "cover_artwork_uri":"https://instagram.fcgk38-1.fna.fbcdn.net/v/t39.30808-6/468903375_90029297306055_7984991829688613211_n.jpg?stp=dst-jpg_s168x128_tt6&_nc_cat=1&ccb=1-7&_nc_sid=2f2557&_nc_ohc=FGOm3J6ArV0Q7kNvwEDB6cb&_nc_oc=AdlWllwgm4g1VF4Vt3swv-FT5z_V4s_NejmEfQOrc_Y53VPd_fgFR2BMSMs6_DDNkM0&_nc_ad=z-m&_nc_cid=1225&_nc_zt=23&_nc_ht=instagram.fcgk38-1.fna&_nc_gid=HGT_ncwusKeTCnNWd-cf-g&oh=00_Aff6GvgRvfpUYHlef7sF_LrgReJxZYh0r_lYoACwrjz8JA&oe=690AB229",
                "cover_artwork_thumbnail_uri":"https://instagram.fcgk38-1.fna.fbcdn.net/v/t39.30808-6/468903375_90029297306055_7984991829688613211_n.jpg?stp=dst-jpg_s168x128_tt6&_nc_cat=1&ccb=1-7&_nc_sid=2f2557&_nc_ohc=FGOm3J6ArV0Q7kNvwEDB6cb&_nc_oc=AdlWllwgm4g1VF4Vt3swv-FT5z_V4s_NejmEfQOrc_Y53VPd_fgFR2BMSMs6_DDNkM0&_nc_ad=z-m&_nc_cid=1225&_nc_zt=23&_nc_ht=instagram.fcgk38-1.fna&_nc_gid=HGT_ncwusKeTCnNWd-cf-g&oh=00_Aff6GvgRvfpUYHlef7sF_LrgReJxZYh0r_lYoACwrjz8JA&oe=690AB229",
                "is_explicit":False,
                "has_lyrics":True,
                "is_original_sound":False,
                "is_local_audio":False,
                "allows_saving":True,
                "hide_remixing":False,
                "picked_in_post_capture":False,
                "is_bookmarked":False,
                "should_mute_audio":False,
                "product":"story_camera_clips_v2",
                "is_sticker":False,
                "display_type":"HIDDEN",
                "tap_state":0,
                "tap_state_str_id":""
            }]),
            "is_created_with_sound_sync":"0",
            "filter_type":"0",
            "camera_session_id":str(uuid.uuid4()), #"8498fa0d-887a-4201-8e57-d4f7ae2779c7",
            "disable_comments":"0",
            "clips_creation_entry_point":"clips",
            "timezone_offset":self.timezone_offset,
            "source_type":"4",
            "camera_position":"unknown",
            "video_result":"",
            "is_created_with_contextual_music_recs":"0",
            "_uid":"74670402255",
            "device_id":"android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16],
            "_uuid":self._uuid,
            "caption":caption,
            "video_subtitles_enabled":"1",
            "capture_type":"clips_v2",
            "enable_smart_thumbnail":"0",
            "audience":"default",
            "upload_id":self.UploadId,
            "template_clips_media_id":"None",
            "is_creator_requesting_mashup":"0",
            "is_template_disabled":"0",
            "additional_audio_info":{
                "has_voiceover_attribution":"0"
            },
            "device":{
                "manufacturer":"Google",
                "model":"google Pixel 2",
                "android_version":25,
                "android_release":"7.1.2"
            },
            "length":self.video_duration,
            "clips":[{
                "length":self.video_duration,
                "source_type":"4",
                "camera_position":"back"
            }],
            "extra":{
                "source_width":1080,
                "source_height":1920
            },
            "audio_muted":True,
            "poster_frame_index":0,
            "clips_segments_metadata":{
                "num_segments":1,
                "clips_segments":[{
                    "index":0,
                    "face_effect_id":None,
                    "speed":100,
                    "source_type":"0",
                    "duration_ms":int(self.video_duration * 1000),
                    "audio_type":"music_selection",
                    "from_draft":"0",
                    "camera_position":-1,
                    "media_folder":None,
                    "media_type":"video",
                    "original_media_type":2
                }]
            },
            "clips_audio_metadata":{
                "original":{"volume_level":0.0},
                "song":{
                    "volume_level":1.0,
                    "is_saved":"0",
                    "artist_name":"Willy Anggawinata",
                    "audio_asset_id":"1259893491830958",
                    "audio_cluster_id":"438044872418006",
                    "track_name":"Semanis Kamu",
                    "is_picked_precapture":"1"
                }
            },
            "music_params":{
                "audio_asset_id":"1259893491830958",
                "audio_cluster_id":"438044872418006",
                "audio_asset_start_time_in_ms":43000,
                "derived_content_start_time_in_ms":0,
                "overlap_duration_in_ms":15000,
                "browse_session_id":str(uuid.uuid4()), #"19dd27ad-4d36-44d8-9c32-537507d30b58",
                "product":"story_camera_clips_v2",
                "song_name":"Semanis Kamu",
                "artist_name":"Willy Anggawinata",
                "alacorn_session_id":None
            }
        }
        data = {'signed_body': f'SIGNATURE.{json.dumps(dat)}'}
        print(json.dumps(dat, indent=4))
        response = self.r.post('https://i.instagram.com/api/v1/media/configure_to_clips/', params=params, headers=headers, data=data, allow_redirects=True).json()
        print(response)
        if 'Anda Sudah Logout' in str(response) or 'login_required' in str(response):
            print('[✗] Session Expired!')
        elif 'VideoSourceBitrateCheckException' in str(response) or 'Transcode not finished yet.' in str(response):
            exit()
        else:
            link = response.get('media').get('code')
            print('https://www.instagram.com/reel/{}/'.format(link))

def check_folder(path, valid_ext):
    wrong_files = []

    if not os.path.isdir(path):
        print(f"Folder tidak ditemukan: {path}")
        return [], []

    for root, dirs, files in os.walk(path):  # scan sampai ke dalam subfolder
        for file in files:
            fullpath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()  # ambil ekstensi
            if ext in valid_ext:
                wrong_files.append(fullpath)

    return wrong_files

def OpenFiles(path):
    with open(path, 'r') as f:
        data = f.read().splitlines()
    f.close()
    list_filename_cookie = []
    for line in data:
        if '|' in line:
            filename, cookie = line.split('|')
            list_filename_cookie.append((filename, cookie))
        else: pass
    
    if not list_filename_cookie:
        return data
    else: return list_filename_cookie

def ScanningFiles(folder_akun:list):
    Results, listPath, caption, hashtag, log = [], [], [], [], False

    for item in os.listdir(folder_akun):
        fullpath = os.path.join(folder_akun, item)
        
        if os.path.isdir(fullpath):
            if item == 'foto':
                valid_extensions = {'.jpg', '.jpeg'}
                wrong_files = check_folder(fullpath, valid_extensions)                    
                if wrong_files:
                    print("[✓] Semua file memiliki ekstensi yang valid.")
                    Results.append(True)
                    listPath.append(wrong_files)

                else:
                    print("[✗] File dengan ekstensi tidak valid ditemukan:")
                    Results.append(False)
                    
            elif item == 'video':
                valid_extensions = {'.mp4'}
                wrong_files = check_folder(fullpath, valid_extensions)
                if wrong_files:
                    print("[✓] Semua file memiliki ekstensi yang valid.")
                    Results.append(True)
                    listPath.append(wrong_files)

                else:
                    print("[✗] File dengan ekstensi tidak valid ditemukan:")
                    Results.append(False)

            elif item == 'results':
                valid_extensions = {'.mp4'}
                wrong_files = check_folder(fullpath, valid_extensions)
                if wrong_files:
                    print("[✗] Berkas harus dibersihkan:")
                    for wf in wrong_files:
                        print(f"         - {wf}")
                    print()
                    Results.append(False)
                    
                else:
                    print("[✓] Berkas telah dibersihkan.")
                    Results.append(True)
                    listPath.append(wrong_files)
            else:
                print("[✗] Folder tidak dikenali di dalam direktori utama.")
                Results.append(False)

        elif os.path.isfile(fullpath):
            if item == 'caption.txt':
                Checkcaption = OpenFiles(path=fullpath)
                if not Checkcaption:
                    Results.append(False)
                    print("[✗] File caption.txt kosong.")
                else:
                    Results.append(True)
                    caption.append(Checkcaption)
                    print("[✓] File caption.txt terisi.")
            elif item == 'hashtag.txt':
                Checkhastag = OpenFiles(path=fullpath)
                if not Checkhastag:
                    Results.append(False)
                    print("[✗] File hashtag.txt kosong.")
                else:
                    Results.append(True)
                    hashtag.append(Checkhastag)
                    print("[✓] File hashtag.txt terisi.")
            elif item == 'log.txt':
                CheckLog = OpenFiles(path=fullpath)
                if not CheckLog:
                    Results.append(True)
                    log = True
                    print("[✓] File log.txt telah dibersihkan.")
                else:
                    Results.append(False)
                    print("[✗] File log.txt harus dibersihkan.")
            else:
                print("[✗] Folder tidak dikenali di dalam direktori utama.")
                Results.append(False)

    return Results, listPath, caption, hashtag, log

def CheckingFolder(ListDAta: str):
    for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
        if not os.path.isdir(folder_akun):
            print(f'[✗] Folder tidak ditemukan: {folder_akun}\n')
            continue

        print(f'[•] Checking Akun {idx} - Folder {folder_akun}\n')
        RessScan, listPath, caption, hashtag, log = ScanningFiles(folder_akun=folder_akun)
        return RessScan, listPath, caption, hashtag, log
    
def OpenFolder(Path):
    return [os.path.abspath(os.path.join(Path, f)) for f in os.listdir(Path)]

def SortedGenerateFotoToVideo(Path):
    for Images in Path:
        folders = os.path.dirname(os.path.dirname(Images))
        name = os.path.splitext(os.path.basename(Images))[0] + '.mp4'
        image_to_video(image_path=Images, output_path=folders, basename=name, duration=30, fps=30)


if __name__ == '__main__':
    lo = PostReels(cookie='eyJkc191c2VyX2lkIjoiNzQ2NzA0MDIyNTUiLCJzZXNzaW9uaWQiOiI3NDY3MDQwMjI1NSUzQVIwVWxtbW1MSmdyU3dnJTNBMCUzQUFZaDlPMjFFcC1QRElESGFFNlcwdGJvNDlFVENabnBNX2x3b1ZnNFVpQSJ9')
    lo.GetListMusic()
    # listValid, listPath = [], []
    # PAthcookie = input('[+] File Data Akun (.txt) : ')
    # if not PAthcookie.endswith('.txt'):
    #     print('[✗] File harus berekstensi .txt')
    #     exit()

    # ListDAta = OpenFiles(path=PAthcookie)
    # print('\n' + '='*50 )
    # for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
    #     if not os.path.isdir(folder_akun):
    #         print(f'[✗] Folder tidak ditemukan: {folder_akun}\n')
    #         continue

    #     print(f'[•] Checking Akun {idx} - Folder {folder_akun}\n')
    #     # print('='*50)
    #     RessScan, listPath, caption, hashtag, log = ScanningFiles(folder_akun=folder_akun)
    #     listValid.extend(RessScan)
    #     print()
    #     if False in RessScan:
    #         print(f'[✗] Status : Folder {folder_akun} tidak memenuhi syarat untuk upload.\n')
    #     else:
    #         print(f'[✓] Status : Folder {folder_akun} memenuhi syarat untuk upload.\n')
    #     print('='*50 + '\n')

    # if False in listValid:
    #     print('[✗] Beberapa folder tidak memenuhi syarat untuk upload. Silakan periksa kembali folder tersebut.\n')
    #     exit()

    # for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
    #     PathPhoto = OpenFolder(os.path.join(folder_akun, 'foto'))
    #     PathVideo = OpenFolder(os.path.join(folder_akun, 'video'))
    #     SortedGenerateFotoToVideo(Path=PathPhoto)

        # basefile = []
        # for item in os.listdir(folder_akun):
        #     full = os.path.join(folder_akun, item)
            
        #     if os.path.isdir(full):
        #         LIstFile = OpenFolder(full)
        #         basefile.extend(LIstFile)
            
        #     # elif os.path.isfile(full):
        #     #     basefile.append(os.path.abspath(full))
        # print(basefile)
    # image_to_video(image_path='x.jpeg')
    # mt = PostReels(cookie=None)
    # mt.generate_thumbnail_current_time(video_path='x.jpeg')
    # mt.OpenFiles(path='output.mp4')
    # mt.SendVideo()
    # # mt.OpenFiles(path='x.jpeg')
    # mt.UploadPicture(LocationPath='x.jpeg')
    # mt.UploadVideos()
