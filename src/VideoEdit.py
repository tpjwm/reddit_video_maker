# This class will hold the class that edits the images into video
# TODO: Once complete, remove global import and only import required

from moviepy.editor import *  # movie editor
import os  # used for some file grabbing
import subprocess
import random


def has_audio(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=nb_streams", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return int(result.stdout) - 1


class VideoEditor:
    def __init__(self, video_name, num_replies=0):
        self.num_replies = num_replies
        self.video_name = video_name
        self.image_path = '../images/'
        self.audio_path = '../audio/'
        self.videos_path = '../videos/'
        self.save_path = '../edited_videos/'
        self.music_path = '../free_music/'
        self.reddit_image_path = '../reddit_images/'

        self.create_dir()  # Creates the edited videos dir if it doesnt exist

        print("Video editor initiated")

    def create_dir(self):
        """Creates the dir to hold the edited video if it doesnt already exist"""
        try:
            os.makedirs(self.save_path)
            print(f'directory: {self.save_path} created')
        except FileExistsError:
            pass

    def create_movie(self):
        """
        Creates a .mp4 file for every text to speech and post
        will then combine every mp4 file for entire video
        can add transitions this way
        """
        clips = []  # clips are mp4 clips to be combined to make entire movie
        clip_count = 0

        # Create audio file and image file, then combine and add to list of clips
        title_audio = AudioFileClip(self.audio_path + 'title.mp3')
        title_clip = ImageClip(self.image_path + 'title.jpeg').set_duration(title_audio.duration + 0.5)
        title_mp4 = concatenate([title_clip], method="compose")
        new_audioclip = CompositeAudioClip([title_audio])

        title_mp4.audio = new_audioclip
        clips.append(title_mp4)

        # Loop through the rest of posts doing same thing above
        for i in range(0, self.num_replies):
            tmp_audio = AudioFileClip(f'{self.audio_path}reply{i}.mp3')
            tmp_dur = tmp_audio.duration
            tmp_clip = ImageClip(f'{self.image_path}reply{i}.jpeg').set_duration(tmp_dur + 0.5)
            tmp_mp4 = concatenate([tmp_clip], method='compose')
            tmp_mp3 = CompositeAudioClip([tmp_audio])
            tmp_mp4.audio = tmp_mp3

            clips.append(tmp_mp4)

        # Combine all clips, and combine into master video
        final_vid = concatenate(clips, method='compose')

        final_vid.write_videofile(f'{self.save_path}{self.video_name}.mp4',
                                  fps=10,
                                  codec='libx264',
                                  audio_codec='aac',
                                  temp_audiofile='temp-audio.m4a',
                                  remove_temp=True
                                  )

    def create_compilation_of_videos(self):
        """
        Combines every mp4 file into one master video
        """
        clips = []  # clips are mp4 clips to be combined to make entire movie
        path, dirs, files = next(os.walk(self.videos_path))

        for file in files:
            if has_audio(self.videos_path + file):
                clips.append(VideoFileClip(self.videos_path + file))
            else:
                video_clip = VideoFileClip(self.videos_path + file)
                audio_clip = AudioFileClip(self.music_path + str(random.randint(1, 17)) + '.mp3').set_duration(
                    video_clip.duration)
                tmp_mp4 = concatenate([video_clip], method='compose')
                new_audio_clip = CompositeAudioClip([audio_clip])
                tmp_mp4.audio = new_audio_clip
                clips.append(tmp_mp4)

        final_vid = concatenate(clips, method='compose')

        final_vid.write_videofile(f'{self.save_path}{self.video_name}.mp4')

        # remove every file in videos folder after saving the compilation
        try:
            for f in os.listdir(self.videos_path):
                os.remove(os.path.join(self.videos_path, f))
        except Exception as err:
            print("Error deleting files: ", err)

    def create_compilation_of_images(self):
        clips = []  # clips are mp4 clips to be combined to make entire movie
        path, dirs, files = next(os.walk(self.reddit_image_path))

        for file in files:
            img_clip = ImageClip(self.reddit_image_path + file).set_duration(5)
            tmp_mp4 = concatenate([img_clip], method='compose')
            clips.append(tmp_mp4)

        # Combine all clips, and combine into master video

        final_vid = concatenate(clips, method='compose')

        final_vid.write_videofile(f'{self.save_path}{self.video_name}.mp4', fps=10)

        for f in os.listdir(self.reddit_image_path):
            os.remove(os.path.join(self.reddit_image_path, f))
