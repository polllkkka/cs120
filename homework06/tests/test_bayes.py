import csv
import string
import unittest

from bayes import NaiveBayesClassifier

PATH_FOR_GIT = "/home/runner/work/cs102/cs102/homework06/data/"


class TestBayes(unittest.TestCase):
    def test_fit_predict(self):
        X_train = [
            "I love this sandwich",
            "this is an amazing place",
            "I feel very good about these beers",
            "this is my best work",
            "what an awesome view",
            "I do not like this restaurant",
            "I am tired of this stuff",
            "I cant deal with this",
            "he is my sworn enemy",
            "my boss is horrible",
        ]
        Y_train = [
            "Positive",
            "Positive",
            "Positive",
            "Positive",
            "Positive",
            "Negative",
            "Negative",
            "Negative",
            "Negative",
            "Negative",
        ]
        X_test = [
            "the beer was good",
            "I do not enjoy my job",
            "I aint feeling dandy today",
            "I feel amazing",
            "Gary is a friend of mine",
            "I cant believe I'm doing this",
        ]
        Y_test = ["Positive", "Negative", "Negative", "Positive", "Negative", "Negative"]
        model = NaiveBayesClassifier()
        model.fit(X_train, Y_train)
        Y_output = model.predict(X_test)
        self.assertEqual(Y_output, Y_test)

    @staticmethod
    def clean(s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

    def test_spam(self):
        with open(PATH_FOR_GIT + "SMSSpamCollection", encoding="utf-8") as f:
            data = list(csv.reader(f, delimiter="\t"))
        X, y = [], []
        for target, msg in data:
            X.append(msg)
            y.append(target)
        X = [self.clean(x).lower() for x in X]
        X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
        model = NaiveBayesClassifier()
        model.fit(X_train, y_train)
        actual_score = model.score(X_test, y_test)
        expected_score = 0.982057416268
        self.assertGreaterEqual(actual_score, expected_score)


if __name__ == "__main__":
    unittest.main()
