import sys
from mft import Client
from passgen import generate_mnemonic_password
import keyring
import os
import glob
from datetime import datetime
from win10toast import ToastNotifier
import pyperclip

if __name__ == '__main__':
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
        mft.login(username=keyring.get_password('mcs', 'ae-user'), password=keyring.get_password('mcs', 'ae-pass'))
        password = generate_mnemonic_password()
        link = mft.create_file_share(share_type=Client.ShareType.send, files=mft_files, password=password, subject=f'MFT Context Menu Share {timestamp}')
        output_file = open(os.path.join(os.path.split(input_files[0])[0], 'MFT Context Menu Share {timestamp}.txt'), 'w')
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