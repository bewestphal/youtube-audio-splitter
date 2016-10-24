from pydub import AudioSegment
import os
import youtube_dl

video_link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
download_file_name = 'Example Title'
save_path = os.getcwd() + '/' + download_file_name + '/' # Or Enter Desired Path
audio_split_length = 600 * 1000 #Seconds
preferred_codec = 'mp3'

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading')

def download_video_audio(youtube_link):

    ydl_opts = {
        'outtmpl': download_file_name + '.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': preferred_codec,
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.download([video_link])

        return video

def split_audio(audio_split_length):

    mp3_file = open(download_file_name + '.' + preferred_codec, 'rb')
    original_audio_segment = AudioSegment.from_mp3(mp3_file)

    print len(original_audio_segment)

    audio_file_list = list()
    x = 0
    while x < len(original_audio_segment):

        if x + audio_split_length > len(original_audio_segment):
            audio_segment = original_audio_segment[x:len(original_audio_segment)]
            break
        else:
            audio_segment = original_audio_segment[x:x+audio_split_length]
            x += audio_split_length

        audio_file_list.append(audio_segment)

    return audio_file_list

def save_audio_files(audio_file_list):

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for audio_file in audio_file_list:
        segment_file_name = download_file_name + '-' +str(audio_file_list.index(audio_file)) + '.' + preferred_codec
        audio_file.export(save_path + segment_file_name, format=preferred_codec)

def remove_downloaded_file():
    os.remove(download_file_name + '.' + preferred_codec)

if __name__=="__main__":

    download_video_audio(video_link)
    audio_file_list = split_audio(audio_split_length)
    save_audio_files = save_audio_files(audio_file_list)

    remove_downloaded_file()