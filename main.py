import sys
from mft import Client
from passgen import generate_mnemonic_password
import keyring
import os
import glob
from datetime import datetime

if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mft = Client(host=keyring.get_password('mcs', 'mft_host'))
    mft.login(username=keyring.get_password('mcs', 'ae-user'), password=keyring.get_password('mcs', 'ae-pass'))
    input_files = sys.argv[1:]  # Omit main.py.
    mft_files = []
    for file in input_files:
        if os.path.isdir(file):
            mft_files += glob.glob(file + '/**/*', recursive=True)
        else:
            mft_files.append(file)

    password = generate_mnemonic_password()
    link = mft.create_file_share(share_type=Client.ShareType.send, files=mft_files, password=password, subject=f'MFT Context Menu Share {timestamp}')
    output_file = open(os.path.join(os.path.split(input_files[0])[0], 'MFT Context Menu Share {timestamp}.txt'), 'w')
    output_file.write(f"Link: {link}\n")
    output_file.write(f"Password: {password}\n")
    output_file.close()