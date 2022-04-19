import numpy as np
import pandas as pd
import pickle


class KNN:
    def __init__(self):
        self.max_col = 0
        self.max_rows = 0
        self.dist_choice = 0
        self.k_choice = 0
        self.learn_real_classes = np.array([])
        self.real_classes = np.array([])

    def run(self, data):
        num_rows, num_cols = data.shape
        self.max_col = num_cols - 1
        self.max_rows = num_rows

        self.k_choice = validate_k()
        self.dist_choice = validate_method()
        predictions = []

        learn_dataset, test_dataset = self.train(data)

        n_rows, n_cols = test_dataset.shape

        for i in range(int(n_rows)):
            vector = test_dataset[i, :]
            predictions.append(self.predict(learn_dataset, vector))

        predictions1 = np.array(predictions)
        print(len(predictions1))
        print(predictions1)
        int_array = self.real_classes.astype(int)
        print(len(int_array))
        self.f1(predictions1, int_array)

    def train(self, data):
        np.random.shuffle(data)
        lear_data = data[:int(0.8 * self.max_rows), :]
        test_data = data[int(0.8 * self.max_rows):, :]
        last = self.max_col
        self.learn_real_classes = lear_data[:, last]
        self.real_classes = test_data[:, last]
        return lear_data[:, 0:last], test_data[:, 0:last]

    def predict(self, learn_dataset, vector):

        if self.dist_choice == 1:
            learn_dataset = self.euclidean_distance(learn_dataset, vector)
        elif self.dist_choice == 2:
            learn_dataset = self.taxi_distance(learn_dataset, vector)
        elif self.dist_choice == 3:
            learn_dataset = self.max_distance(learn_dataset, vector)
        elif self.dist_choice == 4:
            learn_dataset = self.cos_distance(learn_dataset, vector)

        neig = learn_dataset[:3, 1]

        n = np.sum(neig)

        if n > (self.max_col / 2):
            return 1
        else:
            return 0

    def euclidean_distance(self, learn_dataset, vector):
        d = np.subtract(learn_dataset, vector)
        d = np.multiply(d, d)
        d = np.sum(d, axis=1)
        d1 = np.stack((d, self.learn_real_classes), axis=-1)
        sorted_array = d1[np.argsort(d1[:, 0])]
        return sorted_array

    def taxi_distance(self, learn_dataset, vector):
        d = np.subtract(learn_dataset, vector)
        d = np.absolute(d)
        d = np.sum(d, axis=1)
        d1 = np.stack((d, self.learn_real_classes), axis=-1)
        sorted_array = d1[np.argsort(d1[:, 0])]
        return sorted_array

    def max_distance(self, learn_dataset, vector):
        d = np.subtract(learn_dataset, vector)
        d = np.absolute(d)
        d = np.amax(d, axis=1)
        d1 = np.stack((d, self.learn_real_classes), axis=-1)
        sorted_array = d1[np.argsort(d1[:, 0])]
        return sorted_array

    def cos_distance(self, learn_dataset, vector):
        licznik = np.multiply(learn_dataset, vector)
        licznik = np.sum(licznik, axis=1)

        mianownikA = np.multiply(learn_dataset, learn_dataset)
        mianownikA = np.sum(mianownikA, axis=1)
        mianownikA = np.sqrt(mianownikA)

        l = len(mianownikA)
        mB = np.full((l, len(vector)), vector)
        mianownikB = np.multiply(mB, mB)
        mianownikB = np.sum(mianownikB, axis=1)
        mianownikB = np.sqrt(mianownikB)

        mianownik = np.multiply(mianownikA, mianownikB)

        d = np.divide(licznik, mianownik)

        d = np.subtract(1, d)

        d1 = np.stack((d, self.learn_real_classes), axis=-1)
        sorted_array = d1[np.argsort(d1[:, 0])]
        return sorted_array

    def f1(self, vector_results, vector_verified):
        verification = vector_results & vector_verified
        true_positives = verification.sum()

        verification = vector_results & ~vector_verified
        false_positives = verification.sum()

        verification = ~vector_results & vector_verified
        false_negatives = verification.sum()

        verification = self.max_rows
        ver = true_positives + false_positives + false_negatives
        true_negatives = len(vector_results) - ver

        error_matrix = {'Error_Matrix': ['True_Positives', 'False_Positives', 'False_Negatives', 'True_Negatives'],
                        'Count': [true_positives, false_positives, false_negatives, true_negatives]
                        }
        error_matrix = pd.DataFrame(error_matrix)
        print("\n Macierz błędów \n")
        print(error_matrix)

        accuracy = (true_positives + true_negatives) / (false_positives + false_negatives + true_positives + true_negatives)
        precission = true_positives / (true_positives + false_positives)
        recall = true_positives / (false_negatives + true_positives)
        F1 = 2 * ((precission * recall) / (precission + recall))

        print("\n Macierz metryk \n")

        metricks = {'Metricks': ['accuracy', 'precission', 'recall', 'F1'],
                    'Value': [accuracy, precission, recall, F1]
                    }
        metricks = pd.DataFrame(metricks)
        print(metricks)

        frames = [error_matrix, metricks]
        result = pd.concat(frames, axis=1, ignore_index=True)

        s = "method_"+str(self.dist_choice)+"_k_" + str(self.k_choice) + ".txt"
        result.to_csv(s, sep=",")


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


if __name__ == '__main__':
    my_data = np.genfromtxt('dataset2.csv', delimiter=' ')
    k = KNN()
    k.run(my_data)
    # end
