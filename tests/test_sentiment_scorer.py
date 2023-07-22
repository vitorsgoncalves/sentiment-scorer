import unittest
import os
import tempfile
import csv

from sentiment_scorer.sentiment_scorer import analyze_sentiment
from sentiment_scorer.sentiment_scorer import process_files


class SentimentScorerTest(unittest.TestCase):

    def test_analyze_sentiment(self):
        # Test with a simple positive sentence
        row = {"text": "I love this product. It's amazing!"}
        score = analyze_sentiment(row, "text")
        self.assertGreater(score, 0)

        # Test with a simple negative sentence
        row = {"text": "This is terrible. I hate it!"}
        score = analyze_sentiment(row, "text")
        self.assertLess(score, 0)

        # Test with a neutral sentence
        row = {"text": "This is a neutral comment."}
        score = analyze_sentiment(row, "text")
        self.assertEqual(score, 0)

    def test_process_files(self):

    # Create temporary directories for input and output
        with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:

            # Create test CSV files
            test_file1 = os.path.join(input_dir, "test1.csv")
            test_file2 = os.path.join(input_dir, "test2.csv")

            with open(test_file1, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["text"])
                writer.writerow(["I love this product. It's amazing!"])
                writer.writerow(["This is terrible. I hate it!"])
                writer.writerow(["This product is terrible. I hate it!"])
                writer.writerow(["This is okay. It's neither good nor bad."])
                writer.writerow(["This app is okay. It's neither good nor bad."])

            with open(test_file2, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["text"])
                writer.writerow(["I'm feeling happy."])
                writer.writerow(["I'm feeling sad."])
                writer.writerow(["I'm feeling neutral."])

            # Tests the funcion without keywords
            process_files(input_dir,output_dir,"text")

            # Check if the output files were created
            output_file1 = os.path.join(output_dir, "test1_scored.csv")
            output_file2 = os.path.join(output_dir, "test2_scored.csv")
            output_file3 = os.path.join(output_dir, "average_scores.csv")

            self.assertTrue(os.path.exists(output_file1))
            self.assertTrue(os.path.exists(output_file2))
            self.assertTrue(os.path.exists(output_file3))

            # Check if the output files contain the score column
            with open(output_file1, "r") as f:
                self.assertEqual(next(csv.reader(f), None)[-1].strip(), "Sentiment score")
            with open(output_file2, "r") as f:
                self.assertEqual(next(csv.reader(f), None)[-1].strip(), "Sentiment score")

            # Now testing with keywords
            process_files(input_dir,output_dir,"text", ["product","app"])

            # Check if the output files were created
            output_file1 = os.path.join(output_dir, "test1_scored.csv")
            output_file2 = os.path.join(output_dir, "average_scores.csv")

            self.assertTrue(os.path.exists(output_file1))
            self.assertTrue(os.path.exists(output_file2))

            # Check if the output file contains the correct number of filtered lines, including header
            lines = 0
            with open(output_file1, "r") as f:
                
                for line in f:
                    lines = lines + 1
            self.assertEqual(lines, 4)



if __name__ == "__main__":
    unittest.main()
