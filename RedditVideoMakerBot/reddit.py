import praw
import googletrans
from googletrans import Translator
from cleantext import clean 
import elevenlabs
import subprocess
import random
import autosrt
import os
import sys
print("--------------------------------reddit video creator---------------------------")
print("thank you for using my program it means alot, if you buy me a coffee i dont even like it but do cuz munz muhahaha")
print("note: supported languages now are german(de)english(en)arabic(ar)french(fr)spanish(es)")
print("by plexzer999")
print("on instagram")
print("on github")
slctd_subreddit =input("select subreddit: ")
comment_count =input("enter comment count: ")
top_date = str(input("is the top post weekly , monthly, daily (hour , day, week month,year, all) : "))
print("note : make sure to remove 3 min from the gamplay video length or 180s to not cause issues")
vid_length =int(input("input gameplay.mp4 length (in seconds)"))
lang =input("language ar for arabic,en for english ,fr for french,es for spanish ... check google translate api language code ")
file = open("translated_script.txt", "w+")
file = open("script.txt","w+")
elevenlabs.set_api_key("")
translator= Translator()

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)
subreddit = reddit.subreddit(slctd_subreddit)
topsubreddit= subreddit.top(time_filter=top_date, limit=1,)
if subreddit.over18:
      print("top post NSFW")
      sys.exit(1)
for post in topsubreddit:
    with open("script.txt" ,"a") as file:
             file.write(subreddit.title)
    with open("script.txt" ,"a") as file:
             file.write(post.title)
    with open("script.txt" ,"a") as file:
             file.write("\n")
    with open("script.txt" ,"a") as file:
             file.write(post.selftext)
    with open("script.txt" ,"a") as file:
             file.write("\n")
    print("score", post.score)
    print("id- ", post.id)
    comments = post.comments

    for comment in comments[:int(comment_count)]:
        cleaned_text = clean(comment.body, no_emoji=True, no_urls=True)
        with open("script.txt" ,"a") as file:
             file.write(clean(cleaned_text))
       
        with open("script.txt" ,"a") as file:
             file.write(".")
        with open("script.txt" ,"a") as file:
             file.write(".")
        with open("script.txt" ,"a") as file:
             file.write("\n")
        with open("script.txt" ,"a") as file:
             file.write("\n")
print("\n")

frmt_confrm = input("reset background ?[Y/N]")
if (frmt_confrm=="y"):
    subprocess.run(["ffmpeg","-i","gameplay.mp4","-filter:v","crop=9/16*ih:ih","background.mp4"])
elif (frmt_confrm =="n"):
      print("proceding")

print("make sure the script fits or is not correct")
confirm1= input("continue? [Y/N]")
if (confirm1=="n"):
      print("cancellling...")
      sys.exit(1)
      

with open ("script.txt","r",encoding='UTF-8') as file:
    english_text = file.read()
translated = translator.translate(english_text, dest=lang)
translated_text = translated.text
unwanted_text = '[Google Translate]'
cleaned_text = translated_text.replace(unwanted_text, '')
with open("translated_script.txt" ,"w",encoding='UTF-8') as file:
        file.write(str(cleaned_text))
print("make sure the script is what you want")
confirm2= input("continue? [Y/N]")
if (confirm2=="n"):
      print("cancellling...")
      sys.exit(1)

aud =input("generate audio? [Y/N]")
if (aud=="y"):
      audio = elevenlabs.generate(
     text=cleaned_text,
     voice="Adam",
     model="eleven_multilingual_v2")
      elevenlabs.save(audio,"audio.mp3")
      
    


command = ['ffmpeg', '-i', "audio.mp3"]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = result.stderr
duration_start = output.find('Duration: ') + len('Duration: ')
duration_end = output.find(',', duration_start)
duration = output[duration_start:duration_end].strip()

start_time = random.randint(0, vid_length) 
subprocess.run(
      ["ffmpeg", "-ss" , str(start_time), '-i', "background.mp4", "-vcodec", "copy", "-acodec", "copy", '-t', str(duration) , "wo_audio.mp4"])


def merge_audio_video(input_video_path, input_audio_path, output_path):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_video_path,  
        '-i', input_audio_path,  
        '-c:v', 'copy',         
        '-c:a', 'aac',           
        '-strict', 'experimental',
        '-map', '0:v:0',          
        '-map', '1:a:0',         
        output_path             
    ]
    subprocess.run(ffmpeg_cmd)

merge_audio_video("wo_audio.mp4","audio.mp3","w_audio.mp4")

subprocess.run(["autosrt","-S",lang,"-D",lang ,"-F" , "srt","audio.mp3"])
print("make sure the sub is correct")
confirm3 = input("continue? [Y/N]")
if (confirm3=="n"):
      print("cancellling...")
      sys.exit(1)
if lang=="es":
      subprocess.run([  "ffmpeg","-i", "w_audio.mp4","-vf",
                       "subtitles=audio.es.srt:force_style='Alignment=10,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=15,MarginL=10,MarginR=10,MarginV=10'","content.mp4"])
      os.remove("audio.es.srt")
elif lang =="en":
      subprocess.run([  "ffmpeg","-i", "w_audio.mp4","-vf",
                       "subtitles=audio.en.srt:force_style='Alignment=10,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=15,MarginL=10,MarginR=10,MarginV=10'","content.mp4"])
      os.remove("audio.en.srt")
elif lang =="ar":
      subprocess.run([  "ffmpeg","-i", "w_audio.mp4","-vf",
                       "subtitles=audio.ar.srt:force_style='Alignment=10,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=15,MarginL=10,MarginR=10,MarginV=10'","content.mp4"])
      os.remove("audio.ar.srt")
elif lang =="fr":
      subprocess.run([  "ffmpeg","-i", "w_audio.mp4","-vf",
                       "subtitles=audio.fr.srt:force_style='Alignment=10,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=15,MarginL=10,MarginR=10,MarginV=10'","content.mp4"])
      os.remove("audio.fr.srt")
elif lang =="de":
      subprocess.run([  "ffmpeg","-i", "w_audio.mp4","-vf",
                       "subtitles=audio.de.srt:force_style='Alignment=10,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=15,MarginL=10,MarginR=10,MarginV=10'","content.mp4"])
      os.remove("audio.de.srt")
os.remove("wo_audio.mp4")
os.remove("w_audio.mp4")
os.remove("script.txt")
os.remove("translated_script.txt")
print("SUCCESS !    yay")
