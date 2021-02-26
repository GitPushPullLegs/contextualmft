import sys
from mft import Client
from passgen import generate_mnemonic_password
import keyring
import os
import glob
from datetime import datetime
from win10toast import ToastNotifier
import pyperclip
import getpass
import win32com.client
import tkinter
from tkinter import ttk


def setup(username: str):
    file_pieces = "/".join(__file__.split("/")[:-1])
    # Make trigger bat script.
    with open(os.path.join(os.path.split(__file__)[0], 'Trigger.bat'), 'w') as bat:
        bat.writelines([
            f"\"{file_pieces}/venv/Scripts/python.exe\" ",
            f"\"{__file__}\" ",
            f"\"\"%*\"\""
        ])

    path = rf"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\SendTo\Share with MFT.lnk"
    target = os.path.join(os.path.split(__file__)[0], 'Trigger.bat')

    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WindowStyle = 7
    shortcut.save()


def set_credentials(window, username: str, password: str):
    window.destroy()
    keyring.set_password('mft', 'user', username)
    keyring.set_password('mft', 'pswd', password)


def get_mft_credentials():
    window = tkinter.Tk()
    window.title("MFT Login")

    username_label = ttk.Label(window, text="Username")
    username_label.grid(row=0, column=0)
    username_input = ttk.Entry(window, width=50)
    username_input.grid(row=0, column=1)

    pswd_label = ttk.Label(window, text="Password")
    pswd_label.grid(row=1, column=0)
    pswd_input = ttk.Entry(window, width=50, show="*")
    pswd_input.grid(row=1, column=1)

    submit_btn = ttk.Button(window, text="Login", command= lambda: set_credentials(window=window, username=username_input.get(), password=pswd_input.get()))
    submit_btn.grid(row=4, column=0)
    window.mainloop()

if __name__ == '__main__':
    username = getpass.getuser()
    send_to_path = rf"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\SendTo"
    if not glob.glob(send_to_path + '/Share with MFT*'):
        get_mft_credentials()
        setup(username)

    toaster = ToastNotifier()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    input_files = [x.replace("\"", "") for x in sys.argv[1:]]  # Omit main.py.
    mft_files = []
    for file in input_files:
        if os.path.isdir(file):
            mft_files += glob.glob(file + '/**/*', recursive=True)
        else:
            mft_files.append(file)

    if len(mft_files) > 20:
        toaster.show_toast(title="MFT Error",
                           msg="Cannot share more than 20 files at a time.",
                           threaded=True)
    else:
        mft = Client(host=keyring.get_password('mcs', 'mft_host'))
        while True:
            try:
                mft.login(username=keyring.get_password('mft', 'user'), password=keyring.get_password('mft', 'pswd'))
                break
            except ConnectionRefusedError:
                get_mft_credentials()
                pass

        password = generate_mnemonic_password()
        link = mft.create_file_share(share_type=Client.ShareType.send, files=mft_files, password=password,
                                     subject=f'MFT Context Menu Share {timestamp}')
        output_file = open(os.path.join(os.path.split(input_files[0])[0], f'MFT Context Menu Share {timestamp}.txt'),
                           'w')
        output_file.write(f"Link: {link}\n")
        output_file.write(f"Password: {password}\n\n")
        output_file.write(f"Files:\n")
        for file in mft_files:
            output_file.write(f"{file}\n")
        output_file.close()
        if pyperclip.is_available():
            pyperclip.copy(f"{link}\nPassword: {password}")
            toaster.show_toast(title="MFT Link Generated",
                               msg="The link and password have been copied to your clipboard.")
        else:
            toaster.show_toast(title="MFT Link Generated",
                               msg="Details in the txt file.")
