import argparse
import os
import shutil
import datetime
from stat import ST_SIZE, ST_ATIME


# '''function that accepts input from the argparse '''
def arrange(args):
    path = args.path
    organiseType = args.by

    # '''Exception handling for invalid location passed as argument'''
    try:
        fileDetails = getFileData(path)
    except FileNotFoundError:
        print('Please enter a valid directory path')
        return

    #'''os module checks if the organized folder is present'''
    if not os.path.exists(path + '\\organized'):
        os.makedirs(path + '\\organized')
    finalPath = path + '\\organized\\'

    # '''Choice based on the choices=['extension','size','recently-used']'''
    if organiseType == 'extension':
        Extension(path, fileDetails, finalPath)

    elif organiseType == 'size':
        Size(path, fileDetails, finalPath)

    elif organiseType == 'recently_used':
        RecentlyUsed(path, fileDetails, finalPath)

    print('Files in specified folder are organised \nOrganized folder path:',
          path + '\\organized')


fileData = []


# '''Function that checks out all hte files present in the folder recursively and stores in a list fileData'''
def getFileData(path):
    for file in os.scandir(path):
        if not file.is_dir():
            file_name = file.name  # extract filename from the os.scandir()
            file_path = file.path  # extract filepath from the os.scandir()
            # extract file extension from the os.scandir()
            file_ext = file_name.split('.')[-1]
            # extract size using ST_SIZE from stat module
            file_size = os.stat(file_path)[ST_SIZE]
            # extract size using ST_ATIME from stat module
            file_last_used = os.stat(file_path)[ST_ATIME]
            fileData.append(
                [file_name, file_path, file_ext, file_size, file_last_used])

        # '''If there are any subfolers availabe'''
        else:
            fileData + [list_data for list_data in (getFileData(file.path))]

    return fileData


# '''rearranges based on the extension of the files'''
def Extension(path, fileDetails, finalPath):

    for list_data in fileDetails:
        file_name = list_data[0]
        file_path = list_data[1]
        extension = list_data[2]

        if not os.path.exists(finalPath + extension):
            os.makedirs(finalPath + extension)

        shutil.move(file_path, finalPath + extension + '\\' + file_name)


# '''rearranges the files based on their sizes'''
def Size(path, fileDetails, finalPath):
    for list_data in fileDetails:
        file_name = list_data[0]
        file_path = list_data[1]
        size = list_data[3]
        # '''1 Megabyte in bytes ==> 1048576'''
        if size <= 1048576:
            if not os.path.exists(finalPath + 'Small'):
                os.makedirs(finalPath + 'Small')

            shutil.move(file_path, finalPath + 'Small\\' + file_name)

        # '''10* 1 Megabyte'''
        elif size <= 10485760:
            if not os.path.exists(finalPath + 'Medium'):
                os.makedirs(finalPath + 'Medium')

            shutil.move(file_path, finalPath + 'Medium\\' + file_name)
        # '''100 megabytes in bytes ==> 104857600'''
        elif size <= 104857600:
            if not os.path.exists(finalPath + 'not exceeding 100 MB'):
                os.makedirs(finalPath + 'not exceeding 100 MB')

            shutil.move(file_path, finalPath +
                        'not exceeding 100 MB\\' + file_name)
        #'''Larger files which exceed 100 MB in size'''
        elif size >= 104857600:
            if not os.path.exists(finalPath + 'Large Files'):
                os.makedirs(finalPath + 'Large Files')
            shutil.move(file_path, finalPath + 'Large Files\\' + file_name)


# '''Rearragne based on last day of access'''
def RecentlyUsed(path, fileDetails, finalPath):
    curDate = datetime.date.today()
    for list_data in fileDetails:
        file_name = list_data[0]
        file_path = list_data[1]
        # ''' date time is used to access the time from the fileData'''
        recentlyUsed = datetime.date.fromtimestamp(list_data[4])

        # '''used today'''
        if recentlyUsed == curDate:
            if not os.path.exists(finalPath + 'today'):
                os.makedirs(finalPath + 'today')

            shutil.move(file_path, finalPath + 'today\\' + file_name)

        # ''' used yesterday'''
        elif curDate - recentlyUsed == datetime.timedelta(days=1):
            if not os.path.exists(finalPath + 'yesterday'):
                os.makedirs(finalPath + 'yesterday')

            shutil.move(file_path, finalPath + 'yesterday\\' + file_name)

        # ''' used for the last week'''
        elif curDate - recentlyUsed <= datetime.timedelta(days=7):
            if not os.path.exists(finalPath + 'this week'):
                os.makedirs(finalPath + 'this week')

            shutil.move(file_path, finalPath + 'this week\\' + file_name)

        # '''used for last month'''
        elif curDate - recentlyUsed <= datetime.timedelta(days=30):
            if not os.path.exists(finalPath + 'this month'):
                os.makedirs(finalPath + 'this month')

            shutil.move(file_path, finalPath +
                        'this month\\' + file_name)


# '''main function for the program'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # '''CLI arguments for the function'''
    parser.add_argument('--path', default='.',
                        help='Provide name of Folder or Directory to be organised')
    parser.add_argument('--by', default='extension', help='Based on what do you want to organise the folder?',
                        choices=['extension', 'size', 'recently_used'])

    args = parser.parse_args()
    arrange(args)
