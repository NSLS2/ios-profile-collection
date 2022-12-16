import datetime
import time
import os
import re

logger_update_flag = 1
logger_line_count = 0
filtered_log_line_count = 0
log_file_size = 0
gui_log = []
gui_filtered_log = []

def get_log_filename() :
    #### OLD CODE FOR GENERATING A WEEKLY LOG FILE
    #This section of code does datetime arithmetic to create a timestamp for the current week's monday
    #today = datetime.date.today()
    #day_of_week = datetime.date.today().weekday()
    #file_timestamp = today - datetime.timedelta(days = day_of_week)
    #generate the string for the log file name
    #filename = file_timestamp.strftime("%b-%d-%Y") + "_bs_ui_log.txt"

    #### Generates a name for a log file for every 4 month cycle
    cycle_number = (int((datetime.date.today().month - 1)/4)) + 1
    filename = "/home/xf23id2/Cycle_" + str(cycle_number) + "_" + str(datetime.date.today().year) + "_bs_ui_log.txt"
    #filename = "Cycle_" + str(cycle_number) + "_" + str(datetime.date.today().year) + "_bs_ui_log.txt"
    return filename



def bs_ui_log(str):

    filename = get_log_filename()

    #generate the log string, using a time stamp (accurate to the second) plus the string input into this function
    log = time.ctime(time.time()) + " : " + str + "\r"

    # open file, write log, close file
    f = open(filename, "a")
    f.write(log)
    f.close()

    global logger_update_flag 
    logger_update_flag = 1
    global log_file_size
    log_file_size = os.path.getsize(filename)


#Generator object, that returns log entries in reverse chronological order
#if gen_mode is set to 1, generator will return full log entries with timestamp
#if gen_mode is any number other than 1, generator will return the logs without the timestamp
def log_generator(gen_mode = 0):
    filename = get_log_filename()
    f = open(filename, "r")
    lines = f.read().split("\n")
    f.close()
    counter = len(lines)
    if gen_mode == 1 :
        for i in reversed(range(counter - 1)):
            yield lines[i]
    else:
        for i in reversed(range(counter - 1)):
            yield lines[i].split(" : ")[1]

def load_log_as_list():

    filename = get_log_filename()
    f = open(filename, "r")
    lines = f.read().split("\n")
    f.close()
    global gui_log 
    gui_log = lines
    global logger_update_flag 
    logger_update_flag = 0
    global log_file_size 
    log_file_size = os.path.getsize(filename)
    #return lines

def load_filtered_log(string):
    global gui_log 
    global gui_filtered_log 
    gui_filtered_log = []

    processed_str = ""
    for letter in string :
        if letter == "\"" or letter == "(" or letter == ")" or letter == "[" or letter == "]" or letter == "{" or letter == "}" or letter == "+" or letter == "-" or letter == "*" or letter == "/" or letter == "\\" or letter == "!" or letter == "?" or letter == "$":
            processed_str = processed_str + "\\" + letter
        else :
            processed_str = processed_str + letter

    filter_str = ".+(?i)" + processed_str + ".*"
    re_filter = re.compile(filter_str)
    for word in gui_log :
        if re_filter.search(word):
            gui_filtered_log.append(word)


def check_file_size():
    filename = get_log_filename()
    current_size = os.path.getsize(filename)
    global log_file_size
    global logger_update_flag
    if not current_size == log_file_size :
        logger_update_flag = 1
    ## Do set update flag to 0 here. Update flag may be set to 1 by the logging function, in which case an update is needed

