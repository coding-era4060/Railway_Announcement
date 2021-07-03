from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import pyodbc
import os
import datetime as dt

# pip install pyaudio
# pip install pydub
# pip install pyodbc
# pip install gTTS

# CHECK THE STATION NAME
open_file = open('station_name.txt', 'r')
station_name_ = open_file.read()
open_file.close()
if len(station_name_) == 0:
    station_name = input('ENTER YOUR STATION NAME : ')
    write_name = open('station_name.txt', 'w+')
    write_name.write(station_name)
    write_name.close()
    station_name_ = station_name


#  PLAY ANNOUNCEMENT
def play_announcement(announcement_audio):
    print('\nANNOUNCING..........')
    Play_Announcement = AudioSegment.from_mp3(announcement_audio)
    play(Play_Announcement)


# CONVERSION OF TIME - ADD 20_MIN IN YOUR SYSTEM TIME
def findTime(_time_24, _time_12, add_minute):
    # convert the given time in minutes
    minute = int(_time_12[:2]) * 60 + int(_time_12[3:])

    # Add minute to current minutes
    minute += int(add_minute)
    # Obtain the new hour
    # and new minutes from minutes
    hour = (int(minute / 60)) % 24

    new_min = minute % 60
    check_time_list = []
    # Print the hour in appropriate format
    if hour < 10:
        new_time = str(0) + str(hour) + ":"
        check_time_list.append(new_time)

    else:
        new_time = str(hour) + ":"
        check_time_list.append(new_time)
        # Print the minute in appropriate format
    if new_min < 10:
        new_time = str(0) + str(new_min)
        check_time_list.append(new_time)
    else:
        new_time = str(new_min)
        check_time_list.append(new_time)
    if int(_time_24) > 12:
        new_time = ' PM'
        check_time_list.append(new_time)
    else:
        new_time = ' AM'
        check_time_list.append(new_time)
    return "".join(check_time_list)


# THIS WILL MERGE THE ALL AUDIO
def final_audio():
    print('\nMERGE AUDIO ......... ')
    kripya_dhyan = AudioSegment.from_mp3("source_files/_1_Kripiya_dhyan_dijiye.mp3")

    source = AudioSegment.from_mp3("Train_announcements/origin.mp3")

    se_chalker = AudioSegment.from_mp3("source_files/_2_se_chalkar.mp3")

    via = AudioSegment.from_mp3("Train_announcements/Via.mp3")

    ke_raste = AudioSegment.from_mp3("source_files/_3_ke_raste(via).mp3")

    desti = AudioSegment.from_mp3("Train_announcements/destination.mp3")

    kojanewali = AudioSegment.from_mp3("source_files/_4_ko_jane_wali.mp3")

    train_no = AudioSegment.from_mp3("Train_announcements/gaddi_sankhiyan.mp3")

    train_name = AudioSegment.from_mp3("Train_announcements/gaadi_name.mp3")

    platform = AudioSegment.from_mp3('source_files/_5_Platform sankhiya.mp3')

    platform_no = AudioSegment.from_mp3('Train_announcements/platform_no.mp3')

    aarahih = AudioSegment.from_mp3('source_files/_6_pr aa rahi h.mp3')

    print('\nCREATING FINAL AUDIO ......... ')

    final_announcement_audio = kripya_dhyan + source + se_chalker + via + ke_raste + desti + kojanewali \
                               + train_no + train_name + platform + platform_no \
                               + aarahih

    # writing mp3 files is a one liner
    final_announcement_audio.export("Final_announcement.mp3")
    play_announcement('Final_announcement.mp3')


# THIS FUNCTION CREATE THE AUDIO
def create_audio(details):
    print('\nCREATING AUDIO ......... ')
    gaadi_sankhiyaan = details[0]

    gaadi_name = details[1]

    origin = details[2]

    destination = details[3]

    via = details[4]

    platform_no = str(details[5])

    file = gTTS(text=gaadi_sankhiyaan, lang='hi', slow=True)
    file.save('Train_announcements/gaddi_sankhiyan.mp3')

    file = gTTS(text=gaadi_name, lang='hi')
    file.save('Train_announcements/gaadi_name.mp3')

    file = gTTS(text=origin, lang='hi')
    file.save('Train_announcements/origin.mp3')

    file = gTTS(text=destination, lang='hi')
    file.save('Train_announcements/destination.mp3')

    file = gTTS(text=via, lang='hi')
    file.save('Train_announcements/Via.mp3')

    file = gTTS(text=platform_no, lang='hi', slow=True)
    file.save('Train_announcements/platform_no.mp3')

    final_audio()


# THIS FUNCTION RETRIEVE INFORMATION FROM MS-ACCESS DATABASE
def retrieve_data(os_time, add_time):
    print('\nRETRIEVE INFORMATION ......... ')
    abc = '''SELECT Train_no,Train_name,Origin,Destination,Via,Platform,Time from Announcement
            where Status = 'Not Arrived' 
            AND Time between '%s' and '%s' ''' % (os_time, add_time)
    cursor.execute(abc)
    Train_time = cursor.fetchall()
    if Train_time:
        for i in Train_time:
            inserting_data = list(i)
            if not check_repeatation:
                create_audio(inserting_data)
                check_repeatation.append(inserting_data)
            else:
                if check_repeatation[-1] != inserting_data:
                    create_audio(inserting_data)
                    check_repeatation.append(inserting_data)


# TAKE OS TIME AND ADD 20MIN
def proceed_programme():
    current_sys_time = dt.datetime.now()
    sys_time = current_sys_time.strftime('%I:%M %p')
    time_12 = current_sys_time.strftime('%I:%M')
    time_24 = current_sys_time.strftime('%H')
    minutes = '20'
    time_after_add = findTime(time_24, time_12, minutes)
    retrieve_data(sys_time, time_after_add)


if __name__ == '__main__':
    check_directory = os.path.isdir('Train_announcements')
    if not check_directory:
        os.makedirs('Train_announcements')

    check_repeatation = []
    db_file_location = os.path.abspath('Railway_announcement.accdb')
    conn = pyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' % (db_file_location,))
    cursor = conn.cursor()
    a = 1

    # when a=1 means your programme your programme start and welcomes

    while a == 1:
        tune = AudioSegment.from_mp3('source_files/start announcement tune.mp3')

        station_name_conversion = gTTS(text=station_name_, lang='hi')
        station_name_conversion.save('station_name.mp3')

        station_name_sound = AudioSegment.from_mp3('station_name.mp3')

        welcome = AudioSegment.from_mp3('source_files/passenger welcome.mp3')
        welcome_announement = tune + station_name_sound + welcome + tune

        welcome_announement.export('welcome_announcement.mp3')

        play_announcement('welcome_announcement.mp3')

        proceed_programme()
        a += 1
        print(a)
    while a >= 2:
        proceed_programme()
        a += 1
        print(a)
