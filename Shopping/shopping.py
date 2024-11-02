from calendar import month
import csv
from email import header
from importlib import readers
from os import read
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    evidence = []
    labels = []

    month_mapping = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(header)
        
         # Define the index of each column
        col_indexes = {
            'Administrative': 0,
            'Administrative_Duration': 1,
            'Informational': 2,
            'Informational_Duration': 3,
            'ProductRelated': 4,
            'ProductRelated_Duration': 5,
            'BounceRates': 6,
            'ExitRates': 7,
            'PageValues': 8,
            'SpecialDay': 9,
            'Month': 10,
            'OperatingSystems': 11,
            'Browser': 12,
            'Region': 13,
            'TrafficType': 14,
            'VisitorType': 15,
            'Weekend': 16,
            'Revenue': -1  # Last column for labels
        }
        
        for row in reader:
            evidence_row = []
            
            for col_name, col_index in col_indexes.items():
                if col_name == 'Month':
                    evidence_row.append(month_mapping[row[col_index]])
                elif col_name == 'VisitorType':
                    evidence_row.append(1 if row[col_index] == 'Returning_Visitor' else 0)
                elif col_name == 'Weekend':
                    evidence_row.append(1 if row[col_index] == 'TRUE' else 0)
                elif col_name == 'Revenue':
                    labels.append(1 if row[col_index] == 'TRUE' else 0)
                else:
                    value = int(row[col_index]) if '.' not in row[col_index] else float(row[col_index])
                    evidence_row.append(value)
            

            evidence.append[evidence_row]
       
    return evidence, labels
                    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    

    return model
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    # Initialize variables to count True Positive, False Positive, True Negative, and False Negative
    TP = FP = TN = FN = 0

    # Calculate True Positive, False Positive, True Negative, and False Negative
    for actual, predicted in zip(labels, predictions):
        if actual == 1 and predicted == 1:
            TP += 1
        elif actual == 0 and predicted == 1:
            FP += 1
        elif actual == 0 and predicted == 0:
            TN += 1
        elif actual == 1 and predicted == 0:
            FN += 1

    # Calculate Sensitivity (True Positive Rate)
    sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0

    # Calculate Specificity (True Negative Rate)
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    return sensitivity, specificity
            


if __name__ == "__main__":
    main()
