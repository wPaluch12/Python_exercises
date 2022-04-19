import pandas as pd
import numpy as np
import time

def load_data(source_path):
    data = pd.read_csv(source_path, sep=' ', header=None)
    return data


def train(data, number_of_rekords):
    data = data.sample(frac=1)
    lear_data = data.iloc[:int(0.8*number_of_rekords), :]
    test_data = data.iloc[int(0.8*number_of_rekords):, :]
    return lear_data, test_data


def f_eucl(data, vector, max):
    result = 0.0
    for i in range(max):
        result += (data[i] - vector[i]) ** 2
    return result ** 0.5


def euclidean_distance(learn_dataset, vector, max):
    learn_dataset["Distance"] = f_eucl(learn_dataset, vector, max)
    learn_dataset = learn_dataset.sort_values(by=["Distance"], ascending=True)
    return learn_dataset


def f_taxi(data, vector, max):
    result = 0.0
    for i in range(max):
        result += abs(data[i] - vector[i])
    return result


def taxi_distance(learn_dataset, vector, max):
    learn_dataset["Distance"] = f_taxi(learn_dataset, vector, max)
    learn_dataset = learn_dataset.sort_values(by=["Distance"], ascending=True)
    return learn_dataset


def f_max(data, vector, max_c):
    result = pd.DataFrame()
    for i in range(max_c):
        result[i] = (abs(data[i] - vector[i]))
    return result.max(axis=1, skipna=False)


def max_distance(learn_dataset, vector, max):
    learn_dataset["Distance"] = f_max(learn_dataset, vector, max)
    learn_dataset = learn_dataset.sort_values(by=["Distance"], ascending=True)
    return learn_dataset


def f_cos(data, vector, max):
    mianownikA = 0.0
    mianownikB = 0.0
    licznik = 0.0
    for i in range(max):
        licznik += (data[i] * vector[i])
        mianownikA += (data[i])**2
        mianownikB += (vector[i])**2
    return 1 - (licznik/((mianownikA**0.5) * (mianownikB**0.5)))


def cos_distance(learn_dataset, vector, max):
    learn_dataset["Distance"] = f_cos(learn_dataset, vector, max)
    learn_dataset = learn_dataset.sort_values(by=["Distance"], ascending=True)
    return learn_dataset


def predict(learn_dataset, vector, k, max, choice):

    if choice == 1:
        learn_dataset = euclidean_distance(learn_dataset, vector, max)
    elif choice == 2:
        learn_dataset = taxi_distance(learn_dataset, vector, max)
    elif choice == 3:
        learn_dataset = max_distance(learn_dataset, vector, max)
    elif choice == 4:
        learn_dataset = cos_distance(learn_dataset, vector, max)

    neighour = learn_dataset.iloc[:k]
    neighourT = neighour.transpose()

    n = neighourT.iloc[max, :].sum()

    if n > (k / 2):
        return 1
    else:
        return 0


def f1(vector_results, vector_verified):
    verification = vector_results & vector_verified
    true_positives = verification.sum()

    verification = vector_results & ~vector_verified
    false_positives = verification.sum()

    verification = ~vector_results & vector_verified
    false_negatives = verification.sum()

    verification = vector_verified.count()
    true_negatives = verification-true_positives - false_positives - false_negatives


    error_matrix = {'Error_Matrix': ['True_Positives', 'False_Positives', 'False_Negatives', 'True_Negatives'],
            'Count': [true_positives, false_positives, false_negatives, true_negatives]
            }
    error_matrix = pd.DataFrame(error_matrix)
    print("\n Macierz błędów \n")
    print(error_matrix)

    accuracy = (true_positives+true_negatives)/(false_positives+false_negatives+true_positives+true_negatives)
    precission = true_positives/(true_positives+false_positives)
    recall = true_positives/(false_negatives+true_positives)
    F1 = 2*((precission*recall)/(precission+recall))


    print("\n Macierz metryk \n")

    metricks = {'Metricks': ['accuracy', 'precission', 'recall', 'F1'],
                    'Value': [accuracy, precission, recall, F1]
                    }
    metricks = pd.DataFrame(metricks)
    print(metricks)


def validate_k():
    while True:
        try:
            value = int(input("Wprowadź badaną k ilość sąsiadów, może być: 1, 3 lub 5 >>"))
        except ValueError:
            print("Wprowadzono niepoprawne dane.")
            continue
        if value == 1:
            return 1
        elif value == 3:
            return 3
        elif value == 5:
            return 5
        else:
            print("wprowadzona wartość jest niepoprawna")
            continue


def validate_method():
    while True:
        print("""Wybierz metodę liczenia odległości. Wpisz wybraną cyfrę:
        1. Odległość Euklidesowa
        2. Odległość taksówkowa
        3. Odległość maksimum
        4. Odległość cosinusowa
        """)
        try:
            value = int(input("Wybierz metodę >>"))
        except ValueError:
            print("Wprowadzono niepoprawne dane.")
            continue
        if value == 1:
            return 1
        elif value == 2:
            return 2
        elif value == 3:
            return 3
        elif value == 4:
            return 4
        else:
            print("Nie ma metody o takim numerze, wpisz poprawną liczbę")
            continue


def run(path):
    dataset = load_data(path)
    k = validate_k()
    choice = validate_method()
    number_of_rekords = dataset[0].count()
    max = len(dataset.columns) - 1
    print(dataset)

    predictions = []
    learn_dataset, test_dataset = train(dataset, number_of_rekords)

    for i in range(int(0.2 * number_of_rekords)):
        vector = test_dataset.iloc[i]
        predictions.append(predict(learn_dataset, vector, k, max, choice))

    test_dataset["prediction"] = predictions
    print(test_dataset)
    f1(test_dataset[max], test_dataset["prediction"])


if __name__ == '__main__':
    run("dataset2.csv")
    #end