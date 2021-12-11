import PySimpleGUI as sg
import os
import subprocess

from utils.fileUtils import get_files_in_folder
from utils.ffmpegFilters import get_setpts, get_fade_in, get_fade_out, get_filters

sg.theme('DarkAmber')   # Add a touch of color

# Change this to your FFmpeg install location
FFMPEG_EXE_PATH = "C:/Users/Chuan/Videos/MrSnorlax808/ffmpeg-4.3.2-2021-02-27-essentials_build/bin/ffmpeg.exe"
#DEFAULT_INPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/Full-4K"
#DEFAULT_OUTPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/Timelapsed-4K"
DEFAULT_INPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/TestInput"
DEFAULT_OUTPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/TestOutput"

timelapse_options = ['None', 'x30', 'x60', 'x90']
# All the stuff inside your window.
layout = [  [sg.Text("FFmpeg executable: ")], 
            [sg.Input(key="ffmpeg", default_text=FFMPEG_EXE_PATH, change_submits=True), sg.FileBrowse()],
            [sg.Text("Input Folder: (location of the videos to convert)")],
            [sg.Input(key="inputFolder" ,default_text=DEFAULT_INPUT_FOLDER, change_submits=True), sg.FolderBrowse()],
            [sg.Text("Output Folder: (location of the converted videos)")],
            [sg.Input(key="outputFolder", default_text=DEFAULT_OUTPUT_FOLDER, change_submits=True), sg.FolderBrowse()],
            [sg.HorizontalSeparator()],
            [sg.Text('Timelapse Speedup'), sg.DropDown(key='speedup', values=timelapse_options, default_value='x30')],
            [sg.Checkbox('Audio', default=False, key='audio')],
            [sg.Checkbox('Fade In:', default=True, key='fadeIn')],
            [sg.Text("Start    "), sg.Input(key="fadeInStart", default_text=0)],
            [sg.Text("Duration"), sg.Input(key="fadeInDuration", default_text=0.5)],
            #[sg.HorizontalSeparator()],
            [sg.Checkbox('Fade Out:', default=True, key='fadeOut')],
            [sg.Text("Start    "), sg.Input(key="fadeOutStart", default_text=0)],
            [sg.Text("Duration"), sg.Input(key="fadeOutDuration", default_text=0.5)],
            #[sg.HorizontalSeparator()],
            [sg.Multiline(key='status', default_text='', size=(60, 5))],
            [sg.Button('Process'), sg.Button('Quit')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        break
    #print(values['speedup'])
    #print(values['inputFolder'])
    #print(get_files_in_folder(values['inputFolder']))

    inputFile = DEFAULT_INPUT_FOLDER + '/' + get_files_in_folder(values['inputFolder'])[0]
    outputFile = DEFAULT_OUTPUT_FOLDER + '/' + values['speedup'] + get_files_in_folder(values['inputFolder'])[0]
    setptsFiler = get_setpts(values['speedup'])
    fadeInFilter = get_fade_in(values['fadeIn'], values['fadeInStart'], values['fadeInDuration'])
    fadeOutFilter = get_fade_out(values['fadeOut'], values['fadeOutStart'], values['fadeOutDuration'])
    filters = get_filters([setptsFiler, fadeInFilter, fadeOutFilter])
    print(filters)
    cmd = None
    if values['audio']:
        cmd = [FFMPEG_EXE_PATH, '-i', inputFile, '-filter:v', filters, '-an', outputFile]
    else:
        cmd = [FFMPEG_EXE_PATH, '-i', inputFile, '-filter:v', filters, outputFile]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    for stdout_line in iter(process.stdout.readline, ""):
        if len(stdout_line) == 0:
            break
        line = stdout_line.decode("utf-8")
        print(line)
        window.Element('status').Update(line)
        window.read(timeout=400)

window.close()