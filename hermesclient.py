"""hermesclient module for accessing the Hermes server.

The functions in this module can be used to access the web-api methods of Hermes directly
via HTTP-requests.

If used as a script, this module can be used to submit malware samples to Hermes.

Example:
    $ python hermesclient.py Superadmin Superuser

"""

import argparse
import mimetypes
import requests
import sys

__author__ = 'kiview'

HERMES_URL = "https://hermes.tc.if-is.net/Hermes/"
SAMPLE_URL = HERMES_URL + "sample/save"
LOGIN_URL = HERMES_URL + "j_spring_security_check"


def main():
    """Main function, that is run if this file is run as a script.
    :return: Nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username login credential")
    parser.add_argument("password", help="password login credential")
    parser.add_argument("sample_path", help="the path to the sample file")
    parser.add_argument("sample_name", help="the name of the sample")
    parser.add_argument("sample_description", help="the description of the sample")
    args = parser.parse_args()

    hermes = Hermes()

    if hermes.login(LOGIN_URL, args.username, args.password):
        result = hermes.submit_sample(SAMPLE_URL, args.sample_path, args.sample_name, args.sample_description)
        print(result)
    else:
        print("login failed")
        sys.exit()


class Hermes:

    def __init__(self):
        self.session = requests.Session()

    def login(self, url, username, password):
        """Login to a server via HTTP and store the login cookies into the session.

        :param url: The target url of the HTTP request
        :param username: The username credential
        :param password: The password credential
        :return: True if login was successful, else False
        """
        header = {'X-Requested-With': "XMLHttpRequest"}  # simulates ajax request
        payload = {'j_username': username, 'j_password': password}

        response = self.session.post(url, payload, headers=header, verify=False)

        json = response.json()

        success = False
        if 'success' in json:
            success = json['success']

        return success

    def submit_sample(self, url, path, name, description):
        """Submit a malware sample to the given url.

        This means, uploading it as a HTTP multipart form-data post-request.

        :param url: The target url of the HTTP request
        :param path: The path to the sample file on the filesystem
        :param name: The name under which the sample will be saved on the server
        :param description: The description of the malware sample, that will be saved on the server
        :return: The json-parsed HTTP-response of the server
        """
        payload = {'sampleName': name, 'sampleDescription': description}

        sample_file = open(path)
        content_type = mimetypes.guess_type(sample_file.name)[0]
        files = {'fileSample': (sample_file.name, sample_file, content_type)}

        response = self.session.post(url, payload, files=files, verify=False)

        print(response.text)

        json = response.json()

        return json


if __name__ == "__main__":
    main()
