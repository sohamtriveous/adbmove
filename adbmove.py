__author__ = 'sohammondal'

import sys
import commands


def add_adb_device(devicename=None):
    '''
    Adds a -s device param to the delete commandline in case the devicename is none
    :param devicename: the name/id of the device
    :return:
    '''
    cmd = 'adb '
    if devicename:
        cmd = cmd + '-s ' + devicename + ' '
    return cmd


def copy_files_manual(to_path='', from_path='', devicename=None):
    '''
    copies the given files to a given path
    :param to_path: the destination path
    :param from_path: the source path
    :param devicename: the device
    :return:
    '''
    # add device whenever necessary
    cmd = add_adb_device(devicename)
    # command for pulling a file
    cmd = cmd + 'pull '
    new_cmd = cmd + from_path + ' ' + to_path
    (status, output) = commands.getstatusoutput(new_cmd)
    if status:
        print 'Could not copy', from_path, sys.stderr
        return False
    return True


def del_files(devicename, path):
    '''
    delete files at a particular path
    :param devicename: device
    :param path: path to be deleted
    :return:
    '''
    # add device whenever necessary
    cmd = add_adb_device(devicename)
    # command for deleting the file
    cmd = cmd + 'shell rm -r ' + path
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        print 'Could not delete', path, sys.stderr
        return False
    else:
        return True


def move_files(from_path, to_path, devicename=None):
    '''
    function to move files from one path to the other
    :param from_path: source path
    :param to_path: destination path
    :param devicename: device id
    :return:
    '''
    # get the list of files from the source path
    if copy_files_manual(to_path, from_path, devicename):
        if del_files(devicename, from_path):
            print 'Moved ', from_path, '-->', to_path
        else:
            print 'Could not move ', from_path, '-->', to_path
    else:
        print 'Could not move ', from_path, '-->', to_path
    return


def copy_files(from_path, to_path, devicename=None):
    '''
    function to copy files from one path to the other
    :param from_path: source path
    :param to_path: destination path
    :param devicename: device id
    :return:
    '''
    if copy_files_manual(to_path, from_path, devicename):
        print 'Copied ', from_path, '-->', to_path
    return


def validate_args_nondevice(args=[], devicename=None):
    '''
    sends the non device part of the arguments forward for further processing
    :param args: post device part of the arguments
    :param devicename: device
    :return:
    '''
    length = len(args)
    operation = args[0]
    if operation == '--copy':
        from_path = args[1]
        if length > 2:
            to_path = args[2]
        else:
            to_path = '.'
        copy_files(from_path, to_path, devicename)
    else:
        from_path = args[0]
        if length > 1:
            to_path = args[1]
        else:
            to_path = '.'
        move_files(from_path, to_path, devicename)


def validate_args(args=[]):
    '''
    Validates and starts the parsing procedure
    :param args: commandline arguments
    :return:
    '''
    length = len(args)
    if length < 2:
        print 'usage: [--device devicename] [--copy] source_dir destination_dir'
        return

    operation = args[1]
    if operation == '--device':
        devicename = args[2]
        validate_args_nondevice(args[3:], devicename)
    else:
        validate_args_nondevice(args[1:])
    return


validate_args(sys.argv)


