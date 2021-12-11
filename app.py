import PySimpleGUI as sg
import os
import subprocess

from utils.fileUtils import get_files_in_folder

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

sg.theme('DarkAmber')   # Add a touch of color

# Change this to your FFmpeg install location
FFMPEG_EXE_PATH = "C:/Users/Chuan/Videos/MrSnorlax808/ffmpeg-4.3.2-2021-02-27-essentials_build/bin/ffmpeg.exe"
#DEFAULT_INPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/Full-4K"
#DEFAULT_OUTPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/Timelapsed-4K"
DEFAULT_INPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/TestInput"
DEFAULT_OUTPUT_FOLDER = "C:/Users/Chuan/Videos/MrSnorlax808/TestOutput"

timelapse_options = ['x30', 'x60', 'x90']
# All the stuff inside your window.
layout = [  [sg.Text("FFmpeg executable: ")], 
            [sg.Input(key="ffmpeg", default_text=FFMPEG_EXE_PATH, change_submits=True), sg.FileBrowse()],
            [sg.Text("Input Folder: (location of the videos to convert)")],
            [sg.Input(key="inputFolder" ,default_text=DEFAULT_INPUT_FOLDER, change_submits=True), sg.FolderBrowse()],
            [sg.Text("Output Folder: (location of the converted videos)")],
            [sg.Input(key="outputFolder", default_text=DEFAULT_OUTPUT_FOLDER, change_submits=True), sg.FolderBrowse()],
            [sg.Text('Timelapse Speedup'), sg.DropDown(key='speedup', values=timelapse_options, default_value='x30')],
            [sg.Multiline(key='status', default_text='', size=(60, 5))],
            [sg.Button('Process'), sg.Button('Quit')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        break
    #print('You entered ', values[0])
    print(values['speedup'])
    print(values['inputFolder'])
    print(get_files_in_folder(values['inputFolder']))
    #print("IN2" + values['-IN2-'])
    #subprocess.Popen(FFMPEG_EXE_PATH, cwd=r'd:\test\local')
    #-i Full-4K/kuhio.webm -filter:v "setpts=0.0333*PTS" -an Timelapsed-4K/kuhio4.webm
    inputFile = DEFAULT_INPUT_FOLDER + '/' + get_files_in_folder(values['inputFolder'])[0]
    outputFile = DEFAULT_OUTPUT_FOLDER + '/' + values['speedup'] + get_files_in_folder(values['inputFolder'])[0]
    cmd = [FFMPEG_EXE_PATH, '-i', inputFile, '-filter:v', 'setpts=0.0333*PTS', '-an', outputFile]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    for stdout_line in iter(process.stdout.readline, ""):
        if len(stdout_line) == 0:
            break
        print(stdout_line.decode("utf-8"))
        window.Element('status').Update(stdout_line.decode("utf-8"))
        window.read(timeout=400)
        
    #subprocess.call(FFMPEG_EXE_PATH)
    #execute(cmd)

window.close()