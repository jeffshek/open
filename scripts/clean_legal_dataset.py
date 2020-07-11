# flake8: noqa

import os
import glob
import json
import re
from tqdm import tqdm
from json.decoder import JSONDecodeError

from random import shuffle

"""
place this file in the folder you downloaded then run it
this script only runs on python 3.6+ due to f strings

python ./clean_legal_dataset.py
"""


def get_serialized_text(plain_text):
    """
    you thought you'd spend today training models, instead you're scrubbing data for ... ever.
    """
    serialized_text = plain_text

    # lot of - and then new lines, ie. "Mass-\n\nchusetts" truncate that
    # have to use sub instead of replace because replace catches false positives in page numbers
    serialized_text = re.sub("[a-zA-Z]-\n\n", "", serialized_text)
    serialized_text = re.sub("[a-zA-Z]-\n", "", serialized_text)

    # some texts will combine both \f\r\n ... only care for one
    serialized_text = serialized_text.replace("\r", " ").replace("\f", " ")

    # the new lines are just all over the place from legal documents, compromise and strip them all out (sorry)
    # maybe come back to this later and think about something more optimal to do instead
    serialized_text = serialized_text.replace("\n", " ")

    # remove \xa0
    serialized_text = serialized_text.replace("\xa0", " ")

    # remove another weird pattern
    serialized_text = re.sub("- [- ]{3,100}", " ", serialized_text)

    # remove any page numbers that look like this -3-, -4-, etc, go up to -99-
    # didn't see anymore than 100
    serialized_text = re.sub("-(\d{1,3})-", " ", serialized_text)

    # and then there's page numbers that look like this - 3 - (as opposed to -3-)
    serialized_text = re.sub("- \d{1,3} -", " ", serialized_text)

    # and sometimes they like to write lot of long dashes. i haven't seen more than 90. only catch when at least 3 dashes are used
    serialized_text = re.sub("[-]{3,90}", " ", serialized_text)

    # but even baffling, sometimes they prefer underscores
    serialized_text = re.sub("[_]{3,90}", " ", serialized_text)

    # some texts have 20+ spaces randomly
    serialized_text = re.sub(" +", " ", serialized_text)

    # remove any multiple \n\n in the text. legal seems to really like new lines??
    serialized_text = re.sub("\\n[\\n]{0,10}\\n", "\n", serialized_text)

    # lot of extra spaces at the beginning of many dockets ..
    serialized_text = serialized_text.strip()

    return serialized_text


def get_json_files():
    # alternatively, you can rename current_path to wherever you want
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_files = glob.glob(f"{current_path}/**/*.json", recursive=True)

    # shuffle output to be mixed, therefore trainiing won't be as region specific (ie. only from ca1, ca4, etc.)
    shuffle(json_files)
    return json_files


def run():
    output = []
    json_files = get_json_files()

    for count, file_path in enumerate(tqdm(json_files)):
        # if count > 100:
        # 	continue

        with open(file_path, "r+") as contents:
            try:
                serialized = json.loads(contents.read())
            except JSONDecodeError as exc:
                print(f"Unable To Extract Contents {file_path}")
                continue

            # do a little of early exit validation upfront
            plain_text = serialized.get("plain_text")

            if not plain_text:
                continue

            # less than 500 characters mean it's something like this document has
            # been amended, and that's it. that's not very useful
            if len(plain_text) < 500:
                continue

            bad_file = "Error: May not be a PDF file" in plain_text
            if bad_file:
                continue

            serialized_text = get_serialized_text(plain_text)

            # debug version
            # output.append(f"{file_path}|{serialized_text}|Original\n{plain_text}")

            # live version
            output.append(f"{serialized_text}")

    with open("appeals_dataset.txt", "w+") as opened_file:
        for line in tqdm(output):
            opened_file.write(f"{line}\n")

    print("Done!")


if __name__ == "__main__":
    run()
