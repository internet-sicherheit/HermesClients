import argparse
import json
import hermesclient

__author__ = 'kiview'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="the path to the json file")

    args = parser.parse_args()

    json_dict = load_json_file(args.json_file)
    username = json_dict['username']
    password = json_dict['password']
    samples = json_dict['samples']

    hermes = hermesclient.Hermes()

    hermes.login(hermesclient.LOGIN_URL, username, password)

    for s in samples:
        hermes.submit_sample(hermesclient.SAMPLE_URL, s['path'], s['name'],
                                   s['description'])

    return


def load_json_file(file_path):
    json_file = open(file_path)
    return json.load(json_file)


if __name__ == "__main__":
    main()
