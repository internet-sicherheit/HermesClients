import os
import shutil
import argparse
import zipfile
import hermesclient

__author__ = 'bitpick'


def main():
    TMP_DIRNAME = "/tmp/hermes/"

    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file", help="the path to the zip file")
    parser.add_argument("zip_pwd", help="Password for ZIP file")
    parser.add_argument("uname", help="username for server login")
    parser.add_argument("pwd", help="password for given user")

    args = parser.parse_args()

    zip_file = args.zip_file
    username = args.uname
    password = args.pwd

    hermes = hermesclient.Hermes()
    hermes.login(hermesclient.LOGIN_URL, username, password)

    if not os.path.isdir(TMP_DIRNAME):
        os.mkdir(TMP_DIRNAME)

    with zipfile.ZipFile(zip_file, 'r') as f:
        f.setpassword(args.zip_pwd)
        flst = f.namelist()

        for item in flst:
            print("Extracting and adding " + item)
            sample = f.extract(item)
            shutil.move(item, item + ".exe")
            hermes.submit_sample(hermesclient.SAMPLE_URL, item + ".exe", item, "unknown sample")
            os.remove(item + ".exe")

    os.rmdir(TMP_DIRNAME)

    return


if __name__ == "__main__":
    main()
