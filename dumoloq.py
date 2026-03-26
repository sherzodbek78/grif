import telebot as t,os,subprocess as s
from dotenv import load_dotenv as l
l()
b=t.TeleBot(os.getenv("8566156863:AAHRhEEQy8GPLLyG5NKXx2RldchLpZwDj48"))
os.makedirs("d",exist_ok=True)
@b.message_handler(content_types=['video'])
def h(m):
 try:f=b.get_file(m.video.file_id);i=f"d/{f.file_id}";o=i+"_c";open(i+".mp4",'wb').write(b.download_file(f.file_path));s.run(["ffmpeg","-i",i+".mp4","-vf","crop='min(in_w,in_h)':'min(in_w,in_h)',scale=240:240","-c:v","libx264","-preset","veryfast","-crf","28","-c:a","aac","-strict","-2",o+".mp4"],capture_output=1);b.send_video_note(m.chat.id,open(o+".mp4","rb"));[os.remove(x+".mp4")for x in[i,o]]
 except Exception as e:b.reply_to(m,f"❌ {e}")
b.infinity_polling()
