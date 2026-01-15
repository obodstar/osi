import re
import ast, shutil
import requests, numpy as np, json, random, hashlib, time, uuid, cv2, os, xml.etree.ElementTree as ET, html
from settingaudio import remove_audio, add_audio, CuttingMusic
from dotenv import load_dotenv
from PIL import Image
from pathlib import Path as Pth

DataMusicVideo = []
def Banner():
    print()
    print('    ____            __        __  __      __                __               ')
    print('   / __ \\___  ___  / /____   / / / /___  / /___  ____ _____/ /__  _____')
    print('  / /_/ / _ \\/ _ \\/ / ___/  / / / / __ \\/ / __ \\/ __ `/ __  / _ \\/ ___/ ')
    print(' / _, _/  __/  __/ (__  )  / /_/ / /_/ / / /_/ / /_/ / /_/ /  __/ /          ')
    print('/_/ |_|\\___/\\___/_/____/   \\____/ /___/_/\\____/\\__,_/\\__,_/\\___/_/    ')
    print('        Version 1.0            /_/      By Sidiq Brewstreet                                ')
    print()

def clear_console(): os.system('cls' if os.name == 'nt' else 'clear')

def image_to_video(image_path, output_path=False, basename='output.mp4', duration=15, fps=30):
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

def extract_audio_url_from_dash(dash_manifest: str) -> str | None:
    if not dash_manifest:
        return None
    dash_manifest = dash_manifest.replace('\\n', '\n').replace('\\"', '"')
    root = ET.fromstring(dash_manifest)
    ns = {"mpd": "urn:mpeg:dash:schema:mpd:2011"}
    base_url_el = root.find(".//mpd:AdaptationSet[@contentType='audio']//mpd:BaseURL", ns)
    if base_url_el is None:
        return None
    return html.unescape(base_url_el.text)

def generate_instagram_user_agent():
    ig_versions = ["275.0.0.27.98", "276.1.0.21.98", "277.0.0.19.115", "278.0.0.22.117", "279.0.0.17.109"]
    android_versions = [("25", "7.1.2"), ("26", "8.0.0"), ("27", "8.1.0"), ("28", "9"), ("29", "10")]
    resolutions = ["720x1280", "900x1600", "1080x1920", "1440x2560"]
    dpis = ["240dpi", "320dpi", "480dpi"]
    devices = [("Google", "google Pixel 2"), ("Google", "google Pixel 3"), ("Samsung", "samsung SM-G960F"), ("Samsung", "samsung SM-G973F"), ("Xiaomi", "xiaomi Redmi Note 8"), ("Xiaomi", "xiaomi Redmi Note 9")]
    architectures = [("arm64-v8a", "arm64-v8a"), ("armeabi-v7a", "armeabi-v7a"), ("x86", "android_x86")]
    locales = ["in_ID", "en_US", "en_GB", "id_ID"]

    ig_version = random.choice(ig_versions)
    sdk, android_ver = random.choice(android_versions)
    dpi = random.choice(dpis)
    resolution = random.choice(resolutions)
    brand, device = random.choice(devices)
    cpu, abi = random.choice(architectures)
    locale = random.choice(locales)
    build_id = random.randint(100000000, 999999999)

    useragent = f"Instagram {ig_version} Android ({sdk}/{android_ver}; {dpi}; {resolution}; {brand}/{brand.lower()}; {device}; {cpu}; {abi}; {locale}; {build_id})"
    
    return brand, device, sdk, android_ver, useragent

class ReelsUploader:
    def __init__(self, cookie: str = False, UserID: str = False):
        self.r = requests.Session()
        self.UserID = UserID
        self.cookie = cookie
        self.brand, self.device, self.sdk, self.android_ver, self.UserAgent = generate_instagram_user_agent()
        self.android = "android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16]
        self.timezone_offset = str(-time.timezone)
        self.DeviceID = str(uuid.uuid4())
        self.FamilyDeviceId = str(uuid.uuid4())
        self.Goods = 0
        self.ListAudio = []
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
            'User-Agent': self.UserAgent,
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

    def GetUserID(self):
        headers = {
            'Host': 'b.i.instagram.com',
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Ig-Device-Id': str(uuid.uuid4()),
            'X-Ig-Family-Device-Id': str(uuid.uuid4()),
            'X-Ig-Android-Id': str(self.android),
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 900x1600; samsung; SM-G977N; beyond1q; qcom; in_ID; 458229257)',
            'Accept-Language': 'id-ID, en-US',
            'Authorization': self.cookie,

        }
        self.UserID = self.r.get('https://b.i.instagram.com/api/v1/multiple_accounts/get_account_family/', headers=headers, allow_redirects=True).json().get('current_account').get('pk')

    def DataHeaders(self):
        self.Upload_ID = str(int(time.time()) * 1000)
        self.retry_context = json.dumps({"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0})
        self.X_Instagram_Rupload_Params = json.dumps({
                "upload_media_height":self.FrameHeight,
                "xsharing_user_ids":"[]",
                "upload_media_width":self.FrameWidth,
                "is_clips_video":"1",
                "upload_media_duration_ms":str(self.video_duration),
                "content_tags":"use_default_cover",
                "upload_id":self.Upload_ID,
                "retry_context":self.retry_context,
                "media_type":"2",
                "sticker_burnin_params":"[]"
            })

    def generate_thumbnail_current_time(self, video_path: str = False, output_path: str = False):
        # if video_path.endswith('.mp4'):
            time_seconds = 6 #now.hour * 3600 + now.minute * 60 + now.second
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.video_duration = int(frame_count / fps * 1000) + 21
            self.DurasiFloat = self.video_duration / 1000
            print(f"[•] Video duration: {self.video_duration} seconds", end='\n')
            frame_number = int(time_seconds * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = cap.read()

            self.FrameWidth  = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self.FrameHeight = str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            if success:
                cv2.imwrite(output_path, frame)
            else:
                print("[✗] Failed to generate thumbnail")
            cap.release()

        # elif video_path.endswith('.jpeg'):
        #     img = Image.open(video_path)
        #     self.VideoWidth, self.VideoHeight = img.size
        #     self.video_duration = os.path.getsize(video_path)
    
    def GetListMusic(self):
        response = self.r.get('https://i.instagram.com/api/v1/feed/saved/audio/', headers=self.headersGET, allow_redirects=True).json().get('items')
        for items in response:
            track = items["track"]
            ig_username = track.get('ig_username')
            audio_asset_id   = track.get('audio_asset_id')
            audio_cluster_id = track.get('audio_cluster_id')
            progressive_download_url = track.get('progressive_download_url')
            duration_in_ms = track.get('duration_in_ms')
            dash_manifest = track.get('dash_manifest').replace('\n', '\\n')
            highlight_start_times_in_ms = track.get('highlight_start_times_in_ms')
            title = track.get('title')
            display_artist = track.get('display_artist')
            cover_artwork_uri = track.get('cover_artwork_uri')
            cover_artwork_thumbnail_uri = track.get('cover_artwork_thumbnail_uri')
            is_explicit = track.get('is_explicit')
            has_lyrics = track.get('has_lyrics')
            allows_saving = track.get('allows_saving')
            is_bookmarked = items.get('metadata').get('is_bookmarked')
            self.ListAudio.append(f'{ig_username}|{audio_asset_id}|{audio_cluster_id}|{progressive_download_url}|{duration_in_ms}|{dash_manifest}|{highlight_start_times_in_ms}|{title}|{display_artist}|{cover_artwork_uri}|{cover_artwork_thumbnail_uri}|{is_explicit}|{has_lyrics}|{allows_saving}|{is_bookmarked}')
        
        return self.ListAudio
    
    def GetFrame(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.video_duration = int(frame_count / fps * 1000) + 21
        self.DurasiFloat = self.video_duration / 1000
        print(f"[•] Video duration: {self.video_duration} seconds", end='\n')
        self.FrameWidth  = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        self.FrameHeight = str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def OpenFiles(self, path):
        with open(path, 'rb') as f:
            self.data = f.read()
            self.file_size = len(self.data)
            self.md5hash = hashlib.md5(self.data).hexdigest()
        f.close()
        if self.Goods == 1:
            pass
        
        else:
            self.Goods +=1
            self.Upload_ID = str(int(time.time()) * 1000)
            self.Entity_name = '{}-0-{}-lessO-{}'.format(self.md5hash, self.file_size, self.Upload_ID)
    
    def GetOffset(self):
        headers = {
            'Host': 'i.instagram.com',
            'Segment-Start-Offset': '0',
            'X-Instagram-Rupload-Params': self.X_Instagram_Rupload_Params,
            'Segment-Type': '3',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': self.UserAgent,
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': self.UserID,
            'Ig-Intended-User-Id': self.UserID,
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

        response = self.r.get('https://i.instagram.com/rupload_igvideo/{}'.format(self.Entity_name), headers=headers, allow_redirects=True).json()
        self.offset = response.get('offset')
        if self.offset == 0:
            print('[✓] Get Offset video batch 1 selesai')
        elif self.offset > 0:
            print('[✓] Get Offset video batch 2 selesai')
        else:
            print('[✗] Gagal mendapatkan offset:', response)

    def RuploadIGVideo(self, types:int):
        headers = {
            'Host': 'i.instagram.com',
            'Segment-Start-Offset': '0',
            'Offset': '0',
            'X-Instagram-Rupload-Params': self.X_Instagram_Rupload_Params,
            'X-Entity-Name': self.Entity_name,
            'X-Entity-Length': str(self.file_size),
            'Segment-Type': '3',
            'X_fb_video_waterfall_id': f'{self.Upload_ID}_5F1E64013CE7_Mixed_0',
            'X-Entity-Type': 'video/mp4',
            'X-Ig-Salt-Ids': '51052545',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': self.UserAgent,
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': self.UserID,
            'Ig-Intended-User-Id': self.UserID,
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(self.file_size),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        if types == 1:
            response = self.r.post('https://i.instagram.com/rupload_igvideo/{}'.format(headers['X-Entity-Name']), headers=headers, data=self.data, allow_redirects=True).json()
            try:
                if response.get('status') == 'ok':
                    print('[✓] Upload video batch 1 selesai')
                else:
                    print('[✗] Upload video batch 1 gagal:', response)
            except AttributeError:
                print('[✗] Upload video batch 1 gagal:', response)

        elif types == 2:
            headers.update({'Offset': str(self.offset)})
            response = self.r.post('https://i.instagram.com/rupload_igvideo/{}'.format(headers['X-Entity-Name']), headers=headers, data=self.data, allow_redirects=True).json()
            try:
                if response.get('status') == 'ok':
                    print('[✓] Upload video batch 2 selesai')
                else:
                    print('[✗] Upload video batch 2 gagal:', response)
            except AttributeError:
                print('[✗] Upload video batch 2 gagal:', response)

    def RuploadIGPhoto(self):
        UploadID = f'{self.Upload_ID}_0_{random.randint(1000000000, 9999999999)}'
        headers = {
            'Host': 'i.instagram.com',
            'X_fb_photo_waterfall_id': str(uuid.uuid4()),
            'X-Entity-Type': 'image/jpeg',
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps({
                "retry_context":self.retry_context,
                "media_type":"2",
                "upload_id":self.Upload_ID,
                "sticker_burnin_params":"[]",
                "xsharing_user_ids":"[]",
                "image_compression":json.dumps({
                    "lib_name":"moz",
                    "lib_version":"3.1.m",
                    "quality":"0",
                    "original_width":1080,
                    "original_height":1920
                })
            }),
            'X-Entity-Name': f'{UploadID}',
            'X-Entity-Length': str(self.file_size),
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': self.UserAgent,
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': self.UserID,
            'Ig-Intended-User-Id': self.UserID,
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(self.file_size),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        response = self.r.post('https://i.instagram.com/rupload_igphoto/{}'.format(UploadID), headers=headers, data=self.data, allow_redirects=True).json()
        self.UploadId = response.get('upload_id')
        try:
            if response.get('status') == 'ok':
                print('[✓] Upload thumbnail selesai')
            else:
                print('[✗] Upload thumbnail gagal:', response)
        except AttributeError:
            print('[✗] Upload thumbnail gagal:', response)
    
    def UploadClips(
            self, 
            share_feed='0',
            audio_asset_id=None,
            audio_cluster_id=None,
            progressive_download_url=None,
            duration_in_ms=None,
            dash_manifest=None,
            highlight_start_times_in_ms=None,
            title=None,
            display_artist=None,
            cover_artwork_uri=None,
            cover_artwork_thumbnail_uri=None,
            is_explicit=False,
            has_lyrics=True,
            allows_saving=True,
            is_bookmarked=False,
            caption=None
        ):

        self.Device_Id = str(uuid.uuid4())
        self.Family_Device_Id = str(uuid.uuid4())
        self.browser_id = str(uuid.uuid4())
        self.android = "android-" + hashlib.md5(str(uuid.getnode()).encode('utf-8')).hexdigest()[:16]
        audio_asset_start_time_in_ms = ast.literal_eval(highlight_start_times_in_ms)[0]
        
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'in_ID',
            'X-Ig-Device-Locale': 'in_ID',
            'X-Ig-Mapped-Locale': 'id_ID',
            'X-Pigeon-Session-Id': f'UFS-{str(uuid.uuid4())}-0',
            'X-Pigeon-Rawclienttime': f"{time.time():.3f}",
            'X-Ig-Bandwidth-Totalbytes-B': str(self.offset),
            'X-Bloks-Version-Id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': self.Device_Id,
            'X-Ig-Family-Device-Id': self.Family_Device_Id,
            'X-Ig-Android-Id': self.android,
            'X-Ig-Timezone-Offset': self.timezone_offset,
            'Is_clips_video': '1',
            'Retry_context': self.retry_context,
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv/10=',
            'X-Ig-App-Id': '567067343352427',
            'User-Agent': self.UserAgent,
            'Accept-Language': 'id-ID, en-US',
            'Authorization': 'Bearer IGT:2:{}'.format(self.cookie),
            'Ig-U-Ds-User-Id': self.UserID,
            'Ig-Intended-User-Id': self.UserID,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(self.file_size),
            'Accept-Encoding': 'gzip, deflate',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }
        params = {'video': '1'}
        dat = {
            "clips_share_preview_to_feed":share_feed,
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
                "tag":str(uuid.uuid4()),
                "audio_asset_start_time_in_ms":audio_asset_start_time_in_ms,
                "audio_asset_suggested_start_time_in_ms":audio_asset_start_time_in_ms,
                "derived_content_start_time_in_ms":0,
                "overlap_duration_in_ms":15000,
                "browse_session_id":self.browser_id,
                "music_product":"clips_camera_format_v2",
                "audio_asset_id":audio_asset_id,
                "audio_cluster_id":audio_cluster_id,
                "progressive_download_url":progressive_download_url,
                "duration_in_ms":int(duration_in_ms),
                "dash_manifest":dash_manifest,
                "highlight_start_times_in_ms":list(highlight_start_times_in_ms),#,90500,28000],
                "title":title,
                "display_artist":display_artist,
                "cover_artwork_uri":cover_artwork_uri,
                "cover_artwork_thumbnail_uri":cover_artwork_thumbnail_uri,
                "is_explicit":is_explicit,
                "has_lyrics":has_lyrics,
                "is_original_sound":False,
                "is_local_audio":False,
                "allows_saving":allows_saving,
                "hide_remixing":False,
                "picked_in_post_capture":False,
                "is_bookmarked":is_bookmarked,
                "should_mute_audio":False,
                "product":"story_camera_clips_v2",
                "is_sticker":False,
                "display_type":"HIDDEN",
                "tap_state":0,
                "tap_state_str_id":""
            }]),
            "is_created_with_sound_sync":"0",
            "filter_type":"0",
            "camera_session_id":str(uuid.uuid4()),
            "disable_comments":"0",
            "clips_creation_entry_point":"clips",
            "timezone_offset":self.timezone_offset,
            "source_type":"4",
            "camera_position":"unknown",
            "video_result":"",
            "is_created_with_contextual_music_recs":"0",
            "_uid":self.UserID,
            "device_id":self.android,
            "_uuid":self.Device_Id,
            "caption":caption,
            "video_subtitles_enabled":"1",
            "capture_type":"clips_v2",
            "enable_smart_thumbnail":"0",
            "audience":"default",
            "upload_id":self.Upload_ID,
            "template_clips_media_id":"none",
            "is_creator_requesting_mashup":"0",
            "is_template_disabled":"0",
            "additional_audio_info":{"has_voiceover_attribution":"0"},
            "device":{
                "manufacturer":self.brand,
                "model":self.device,
                "android_version":int(self.sdk),
                "android_release":self.android_ver
            },
            "length":self.DurasiFloat,
            "clips":[{
                "length":self.DurasiFloat,
                "source_type":"4",
                "camera_position":"back"
            }],
            "extra":{
                "source_width":1080,
                "source_height":1920
            },
            "audio_muted":False,
            "poster_frame_index":0,
            "clips_segments_metadata":{
                "num_segments":1,
                "clips_segments":[{
                    "index":0,
                    "face_effect_id":None,
                    "speed":100,
                    "source_type":"0",
                    "duration_ms":int(self.video_duration),
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
                    "artist_name":display_artist,
                    "audio_asset_id":audio_asset_id,
                    "audio_cluster_id":audio_cluster_id,
                    "track_name":title,
                    "is_picked_precapture":"1"
                }
            },
            "music_params":{
                "audio_asset_id":audio_asset_id,
                "audio_cluster_id":audio_cluster_id,
                "audio_asset_start_time_in_ms":audio_asset_start_time_in_ms,
                "derived_content_start_time_in_ms":0,
                "overlap_duration_in_ms":15000,
                "browse_session_id":self.browser_id,
                "product":"story_camera_clips_v2",
                "song_name":title,
                "artist_name":display_artist,
                "alacorn_session_id":None
            }
        }
        data = {'signed_body': f'SIGNATURE.{json.dumps(dat)}'}
        response = self.r.post('https://i.instagram.com/api/v1/media/configure_to_clips/', params=params, headers=headers, data=data, allow_redirects=True).json()
        if response.get('status') == 'ok':
            link = response.get('media').get('code')
            if link is None:
                print(response)
                return False
            print('[✓] Link  : https://www.instagram.com/reel/{}/'.format(link))
            print('[✓] Audio :', response.get('media').get('has_audio'))
            print()
            return True
        else:
            print('[✗] Gagal mengunggah reels:', response, '\n')
            return False

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

def ScanningFiles(folder_akun: str):
    Results   = []
    listPath  = []
    caption   = []
    hashtag   = []
    log       = False

    # ==============================
    # VALIDASI FOLDER
    # ==============================

    folders_required = {
        'foto'   : {'.jpg', '.jpeg'},
        'video'  : {'.mp4'},
        'results': {'.mp4'},
    }

    for folder, valid_ext in folders_required.items():
        path = os.path.join(folder_akun, folder)

        if not os.path.isdir(path):
            print(f"[✗] Folder {folder} tidak tersedia.")
            Results.append(False)
            continue

        wrong_files = check_folder(path, valid_ext)

        if folder == 'results':
            if wrong_files:
                print("[✗] Berkas results harus dibersihkan:")
                for wf in wrong_files:
                    print(f"     - {wf}")
                Results.append(False)
            else:
                print("[✓] Folder results bersih.")
                Results.append(True)
        else:
            if wrong_files:
                print(f"[✓] Folder {folder} valid.")
                Results.append(True)
                listPath.append(wrong_files)
            else:
                print(f"[✗] File tidak valid di folder {folder}.")
                Results.append(False)

    # ==============================
    # VALIDASI FILE TXT
    # ==============================

    files_required = {
        'caption.txt': caption,
        'hashtag.txt': hashtag,
        'log.txt'    : 'log'
    }

    for file, target in files_required.items():
        path = os.path.join(folder_akun, file)

        if not os.path.isfile(path):
            print(f"[✗] File {file} tidak tersedia.")
            Results.append(False)
            continue

        content = OpenFiles(path=path)

        if file == 'log.txt':
            if not content:
                print("[✓] File log.txt telah dibersihkan.")
                log = True
                Results.append(True)
            else:
                print("[✗] File log.txt harus dibersihkan.")
                Results.append(False)
        else:
            if content:
                print(f"[✓] File {file} terisi.")
                target.append(content)
                Results.append(True)
            else:
                print(f"[✗] File {file} kosong.")
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
    
def OpenFolder(Path): return [os.path.abspath(os.path.join(Path, f)) for f in os.listdir(Path)]

def SortedGenerateFotoToVideo(Path):
    for Images in Path:
        folders = os.path.dirname(os.path.dirname(Images))
        name = os.path.splitext(os.path.basename(Images))[0] + '.mp4'
        image_to_video(image_path=Images, output_path=folders, basename=name, duration=30, fps=30)

def ProcessFiles(ListDAta: str, PathFFMPEG: str):
    for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
        lo = ReelsUploader(cookie=cookie)
        try:
            with open(f'{folder_akun}\\music\\music.txt', 'r', encoding='utf-8') as f:
                music = f.read().splitlines()
            f.close()
            
            if not music:
                print(f'[•] Mengambil daftar musik')
                music = lo.GetListMusic()
                for audio in music:
                    with open(f'{folder_akun}\\music\\music.txt', 'a+', encoding='utf-8') as f:
                        f.write(f'{audio}\n')
                    f.close()
                print(f'[✓] Daftar musik berhasil disimpan di Folder {folder_akun}\\music\\music.txt')
            else:
                print(f'[•] Mengambil daftar musik')
                print(f'[✓] Daftar musik sudah diambil sebelumnya, melewati proses ini.')
        except FileNotFoundError:
            print(f'[•] Mengambil daftar musik')
            music = lo.GetListMusic()
            for audio in music:
                with open(f'{folder_akun}\\music\\music.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'{audio}\n')
                f.close()
            print(f'[✓] Daftar musik berhasil disimpan di Folder {folder_akun}\\music\\music.txt')
            
        print()
        checkmusic = os.path.join(os.path.abspath(folder_akun), 'music')
        ressultsmusic = [os.path.abspath(os.path.join(checkmusic, f)) for f in os.listdir(checkmusic) if f.endswith('.mp4')]
        if not ressultsmusic:
            print('[•] Extract Music... ')
            for audio in music:
                ig_username, audio_asset_id, audio_cluster_id, progressive_download_url, duration_in_ms, dash_manifest, highlight_start_times_in_ms, title, display_artist, cover_artwork_uri, cover_artwork_thumbnail_uri, is_explicit, has_lyrics, allows_saving, is_bookmarked = audio.split('|')
                url_audio = extract_audio_url_from_dash(dash_manifest=dash_manifest)
                source_file = f"{folder_akun}\\music\\full_audio_{audio_asset_id}_{ig_username}.mp4"
                output = f"{folder_akun}\\music\\{audio_asset_id}_{ig_username}.mp4"
                CuttingMusic(r=requests, url_audio=url_audio, ffmpeg_path=PathFFMPEG, source_file=source_file, highlight_ms=ast.literal_eval(highlight_start_times_in_ms)[0], output=output, duration=30)
            print('[✓] Musik berhasil di ekstrak ke folder music.')
        else:
            print('[•] Extract Music... ')
            print('[✓] Musik sudah di ekstrak sebelumnya, melewati proses ini.')
        
        PathPhoto = OpenFolder(os.path.join(folder_akun, 'foto' ))
        PathVideo = OpenFolder(os.path.join(folder_akun, 'video'))
        video_uploads = OpenFolder(os.path.join(folder_akun, 'video_upload'))
        
        print()
        if video_uploads:
            print(f'[✓] Folder video_upload di Folder {folder_akun} sudah berisi, melewati proses ini.\n')
            print('='*50)
            continue
        else:
            print(f'[•] Proses Generate Foto ke Video Akun {idx} - Folder {folder_akun}\n')
            SortedGenerateFotoToVideo(Path=PathPhoto)
            print()
            print(f'[•] Menghapus Audio Akun {idx} - Folder {folder_akun}\\video')
            for vid in PathVideo:
                output_video = f'{folder_akun}\\results\\{os.path.basename(vid)}' # sudah .mp4
                remove_audio(ffmpeg_path=PathFFMPEG, video_file=vid, output_file=output_video)
            print(f'[✓] Selesai menghapus audio dari video - Folder {folder_akun}\\video')
            
            print()
            print(f'[•] Proses Menggabungkan Musik ke Video Akun {idx} - Folder {folder_akun}\\video_upload')
            listFileNameVideo = OpenFolder(os.path.join(folder_akun, 'results'))
            ressultsmusic = [os.path.abspath(os.path.join(checkmusic, f)) for f in os.listdir(checkmusic) if f.endswith('.mp4')]
            for video_file in listFileNameVideo:
                audio_file = random.choice(ressultsmusic)
                baseMusic = os.path.basename(audio_file).split('.')[0]
                videopath = os.path.basename(video_file).split('.')[0]
                output_file = f'{folder_akun}\\video_upload\\{videopath}_{baseMusic}.mp4'
                # DataMusicVideo.append(f'{audio_asset_id}|{output_file}')
                add_audio(ffmpeg_path=PathFFMPEG, video_file=video_file, audio_file=audio_file, output_file=output_file)
            print(f'[✓] Selesai menggabungkan musik ke video - Folder {folder_akun}\\video_upload\n')
        print('\n' + '='*50)

def jeda(waktu:int, sukses:int, gagal:int):
    for i in range(waktu, 0, -1):
        print(f"[•] Sukses = {sukses} Gagal = {gagal} <> Menunggu {i}s ", end='\r')
        time.sleep(1)
    print()

def Menu(PathFFMPEG:str, PAthcookie:str, checkingfolders:str, waktu_upload=20, waktu_jeda=0):
    listValid, sukses, gagal = [], 0, 0
    ListDAta = OpenFiles(path=PAthcookie)
    print('\n' + '='*50 )
    for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
        
        if checkingfolders == 'y':
            folders = ['foto', 'video', 'results', 'video_upload', 'music', 'log_thumbnail']

            # 1. Hapus folder yang ingin dikosongkan
            for f in ['results', 'video_upload', 'music']:
                path = os.path.join(folder_akun, f)
                shutil.rmtree(path, ignore_errors=True)

            # 2. Buat ulang SEMUA folder (pastikan kosong)
            for f in folders:
                os.makedirs(os.path.join(folder_akun, f), exist_ok=True)
            
            if not os.path.isdir(folder_akun):
                print(f'[✗] Folder tidak ditemukan: {folder_akun}\n')
                continue
            print(f'[•] Checking Akun {idx} - Folder {folder_akun}\n')
            RessScan, listPath, caption, hashtag, log = ScanningFiles(folder_akun=folder_akun)
            listValid.extend(RessScan)
            print()
            if False in RessScan:
                print(f'[✗] Status : Folder {folder_akun} tidak memenuhi syarat untuk upload.\n')
            else:
                print(f'[✓] Status : Folder {folder_akun} memenuhi syarat untuk upload.\n')
            print('='*50 + '\n')
        elif checkingfolders == 'n':
            print(f'[•] Melewati proses pengecekan folder untuk Akun {idx} - Folder {folder_akun}')
            listValid.append(True)
    if False in listValid:
        print('[✗] Beberapa folder tidak memenuhi syarat untuk upload. Silakan periksa kembali folder tersebut.\n')
        exit()

    print('='*50)
    print('[•] Proses Memproses File untuk Upload...\n')
    ProcessFiles(ListDAta=ListDAta, PathFFMPEG=PathFFMPEG)
    
    # PROSES UPLOAD TESTING
    # clear_console()
    for idx, (folder_akun, cookie) in enumerate(ListDAta, start=1):
        ListVideoUpload = OpenFolder(os.path.join(folder_akun, 'video_upload'))

        for video in ListVideoUpload:
            with open(f'{folder_akun}\\log.txt', 'r', encoding='utf-8') as f:
                pathlog = f.read().splitlines()
            f.close()
            basefilename = os.path.basename(video)
            audio_asset_id = str(basefilename).split('.')[0].split('_')[1]
            if basefilename in pathlog:
                print(f'[✓] Video {basefilename} sudah di upload sebelumnya, melewati proses ini.')
                continue
            else:
                with open(f'{folder_akun}\\music\\music.txt', 'r', encoding='utf-8') as f:
                    basemusic = f.read().splitlines()
                f.close()

                filemusic = next((i for i in basemusic if i.split('|')[1] == audio_asset_id), None)
                if not filemusic:
                    print(f'[✗] Video dengan audio_asset_id {audio_asset_id} tidak ditemukan di folder music, melewati proses upload video {basefilename}.\n')
                    continue
                else:
                    with open(f'{folder_akun}\\caption.txt', 'r', encoding='utf-8') as f:
                        basecaption = f.read().splitlines()
                    f.close()

                    with open(f'{folder_akun}\\hashtag.txt', 'r', encoding='utf-8') as f:
                        basehashtag = f.read().splitlines()
                    f.close()

                    str_dpn  = random.choice(basecaption)
                    str_blkg = random.choice(basehashtag)
                    caption  = f"{str_dpn}\n\n{str_blkg}"

                    ig_username, audio_asset_id, audio_cluster_id, progressive_download_url, duration_in_ms, dash_manifest, highlight_start_times_in_ms, title, display_artist, cover_artwork_uri, cover_artwork_thumbnail_uri, is_explicit, has_lyrics, allows_saving, is_bookmarked = filemusic.split('|')
                    print(f'[•] Proses Upload Video Akun {idx} - File {basefilename}\n')
                    output_video = f'{Pth(video).parents[1]}\\log_thumbnail\\output_{idx}.jpeg'
                    mt = ReelsUploader(cookie=cookie)
                    mt.generate_thumbnail_current_time(video_path=video, output_path=output_video)
                    mt.GetUserID()
                    mt.DataHeaders()

                    mt.OpenFiles(path=video)
                    mt.GetOffset()
                    mt.RuploadIGVideo(types=1)
                    mt.GetOffset()

                    mt.RuploadIGVideo(types=2)
                    mt.OpenFiles(path=output_video)
                    mt.RuploadIGPhoto()
                    print('[•] Mengunggah transcoding video ke Instagram Reels ')
                    time.sleep(int(waktu_upload))
                    if mt.UploadClips(
                            share_feed='0',
                            audio_asset_id=audio_asset_id,
                            audio_cluster_id=audio_cluster_id,
                            progressive_download_url=progressive_download_url,
                            duration_in_ms=duration_in_ms,
                            dash_manifest=dash_manifest,
                            highlight_start_times_in_ms=highlight_start_times_in_ms,
                            title=title,
                            display_artist=display_artist,
                            cover_artwork_uri=cover_artwork_uri,
                            cover_artwork_thumbnail_uri=cover_artwork_thumbnail_uri,
                            is_explicit=is_explicit,
                            has_lyrics=has_lyrics,
                            allows_saving=allows_saving,
                            is_bookmarked=is_bookmarked,
                            caption=caption
                        ):
                        with open(f'{folder_akun}\\log.txt', 'a+', encoding='utf-8') as f:
                            f.write(f'{basefilename}\n')
                        f.close()
                        sukses += 1
                        os.remove(output_video)
                    else:
                        gagal += 1
                    
            jeda(waktu=int(waktu_jeda), sukses=sukses, gagal=gagal)
            print('='*50)
        print(f'[✓] Selesai Upload Video Akun {idx} - Folder {folder_akun}\\video_upload\n')
        print('='*50)

if __name__ == '__main__':
    load_dotenv()
    clear_console()
    Banner()
    PathFFMPEG = os.getenv("Pathffmpeg")
    if PathFFMPEG is None:
        print('[✗] Harap atur Path ffmpeg di file .env')
        exit()
    try:
        PAthcookie = input('[+] File Data Akun (.txt) : ')
        if not PAthcookie.endswith('.txt'):
            print('[✗] File harus format .txt')
            exit()

        checkingfolders = input('[+] Apakah ingin mengecek folder? (y/n) : ').lower()
        if checkingfolders not in ['y', 'n']:
            print('[✗] Pilihan tidak valid, masukkan "y" atau "n".')
            exit()

        try:
            waktu_upload = input('[+] Waktu tunggu proses upload (detik, default 20s) : ')
        except ValueError:
            waktu_upload = 20

        try:
            waktu_jeda = input('[+] Waktu jeda antar video (detik, default 0s) : ')
        except ValueError:
            waktu_jeda = 0

        Menu(PathFFMPEG=PathFFMPEG, PAthcookie=PAthcookie, checkingfolders=checkingfolders, waktu_upload=waktu_upload, waktu_jeda=waktu_jeda)
    except KeyboardInterrupt:
        print('\n[✗] Program dihentikan.')
        exit()