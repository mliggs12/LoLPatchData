"""LoLPatchData module.

Problem statement: Updated champion data is needed when the live LoL patch version changes.
Needs to check the patch version of the most recently saved dataset and requests new data if outdated.
"""
import os
import json
import requests

DATA_FOLDER = os.path.join(os.getcwd(), 'Data')


def get_live_patch():
    """Makes a request for the live patch version and returns it as a string."""
    data = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/patches.json").json()
    latest_patch = data['patches'][-1]
    patch = latest_patch['name']
    print(f"\nThe current live patch is {patch}.")

    return patch


def get_saved_patch(data_folder=DATA_FOLDER):
    """Checks the data folder for datafiles, and returns the latest modified patch version."""
    if os.listdir(data_folder):
        latest_timestamp = 0.0
        for file in os.listdir(data_folder):
            filepath = os.path.join(DATA_FOLDER, file)
            last_modified = os.path.getmtime(filepath)
            latest_timestamp = max(last_modified, latest_timestamp)
            if last_modified == latest_timestamp:
                patch = file.split('.json')[0]
        print(f"\nThe latest saved patch is: {patch}")

        return patch

    else:
        return None


def get_live_dataset():
    saved_patch = get_saved_patch()
    live_patch = get_live_patch()
    if saved_patch and saved_patch == live_patch:
        with open(os.path.join(DATA_FOLDER, saved_patch + '.json'), 'r') as read_file:
            data = json.load(read_file)
        msg = f"\nLoading saved patch datafile '{saved_patch}'"
    else:
        print("\nLive patch datafile not found. Making request for live patch data...")
        data = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json").json()
        with open(os.path.join(DATA_FOLDER, live_patch + '.json'), 'w') as write_file:
            json.dump(data, write_file, indent=4)
        msg = f"\nLive patch dataset saved as '{live_patch}'. Patch data loaded."

    print(msg)
    return data


if __name__ == "__main__":
    champion_data = get_live_dataset()
