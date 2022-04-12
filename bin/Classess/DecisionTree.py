import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump, load


class DecisionTree:
    def __init__(self):
        self.classifier = load('../../files/decision tree/classifier.joblib')


def Learning():
    # Uploading data from file
    dataset = pd.read_csv("../../files/decision tree/database.csv")

    print(f'Shape: {dataset.shape}')
    print(f'Head:\n{dataset.head()}')

    X = dataset.drop('decision', axis=1)
    y = dataset['decision']

    # Split data to training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    # Training
    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)

    # Predictions test
    y_pred = classifier.predict(X_test)

    print()
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save predictions
    dump(classifier, '../../files/decision tree/classifier.joblib')
