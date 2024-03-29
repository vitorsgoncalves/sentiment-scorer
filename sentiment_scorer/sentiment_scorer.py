#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from argparse import ArgumentParser
from gooey import Gooey, GooeyParser
import nltk

nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def analyze_sentiment(row, column, keywords=None):
    """
    Analyzes the sentiment of a given text in a row of the CSV file using VADER sentiment analysis.

    Args:
        row (dict): The row from the CSV file as a dictionary.
        column (str): The title of the column containing the text to be scored in the input file.
        keywords (list, optional): Keywords to filter the input data (default is None).

    Returns:
        float or None: The sentiment score of the text or None if the filtered text is empty.
    """
    text = row[column].split('\n')

    if keywords is not None:
        # Filter text based on keywords (if provided)
        filtered_text = [t for t in text if any(word in t.lower() for word in keywords)]
    else:
        # If no keywords provided, use the entire text
        filtered_text = text

    if len(''.join(filtered_text).strip('\n').strip(' ')) == 0:
        # If the filtered text is empty, return None
        return None
    else:
        # Analyze sentiment of the filtered text using VADER
        ss = sia.polarity_scores('\n'.join(filtered_text))
        return ss["compound"]


def process_files(input_path, output_path, column, keywords=None):
    """
    Process CSV files in the input directory, perform sentiment analysis, and create output files.

    Args:
        input_path (str): Path to the directory containing input CSV files.
        output_path (str): Path to the directory where output CSV files and the average_scores.csv will be saved.
        column (str): The title of the column containing the text to be scored in the input file.
        keywords (list, optional): Keywords to filter the input data (default is None).
    """
    averages = []

    for files in os.listdir(input_path):
        if files.endswith(".csv"):
            filename = files.replace(".csv", "")

            with open(os.path.join(input_path, files), "r") as path:
                file = csv.DictReader(path)

                # Variables for calculating the averages for each input file
                positive_comments = 0
                negative_comments = 0
                neutral_comments = 0
                sum = 0

                with open(os.path.join(output_path, files[:-4] + '_scored.csv'), 'w', encoding='UTF8', newline='') as f:
                    writer = csv.DictWriter(f, file.fieldnames + ["Sentiment score"])
                    writer.writeheader()

                    for row in file:
                        # Analyze sentiment score for each row and update the row with the score
                        sentiment_score = analyze_sentiment(row, column, keywords)

                        if sentiment_score is None:
                            # If the sentiment score is None, skip the row and continue to the next one
                            continue

                        row.update({"Sentiment score": sentiment_score})

                        # update the variables used to calculate the averages
                        if sentiment_score > 0.05:
                            positive_comments += 1
                        elif sentiment_score < -0.05:
                            negative_comments += 1
                        else:
                            neutral_comments += 1

                        sum += sentiment_score

                        writer.writerow(row)

                average_score = sum / (neutral_comments + negative_comments + positive_comments) if (neutral_comments + negative_comments + positive_comments) else 0
                averages.append({'filename': filename, 'positive_comments': positive_comments, 'neutral_comments': neutral_comments, 'negative_comments': negative_comments, 'average_score': average_score})

    # Writes the file with the average values
    with open(os.path.join(output_path, 'average_scores.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'positive_comments', 'neutral_comments', 'negative_comments', 'average_score'])
        writer.writeheader()
        writer.writerows(averages)


@Gooey(
    program_name="Sentiment Scorer",
    language="english",
    program_description="Sentiment analysis using VADER",
    image_dir=".",
    default_size=(610, 660)
)
def main():
    parser = GooeyParser()

    required = parser.add_argument_group(
        'Parameters',
        gooey_options={
            'show_border': False,
            'columns': 2,
        }
    )

    required2 = parser.add_argument_group(
        '',
        gooey_options={
            'show_border': False,
            'columns': 1,
        }
    )

    required.add_argument(
        "-i",
        "--input",
        required=True,
        metavar="Input",
        help="Input CSV file(s) directory path",
        widget="DirChooser"
    )
    required.add_argument(
        "-o",
        "--output",
        required=True,
        metavar="Output",
        help="Output CSVs directory path",
        widget="DirChooser"
    )
    required2.add_argument(
        "-c",
        "--column",
        required=True,
        metavar="Column name",
        help="Title of the column containing the text to be scored in the input file",
    )
    required2.add_argument(
        "-k",
        "--keywords",
        required=False,
        metavar="Keywords",
        help="Keywords to be searched for, in case you want to filter the input data (separated by single space)",
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    if args.keywords is not None:
        keywords = args.keywords.split(' ')
    else:
        keywords = None
    column = args.column

    # Runs the processing code with the inut arguments
    process_files(input_path, output_path, column, keywords)


if __name__ == "__main__":
    main()
