import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns


class NaiveBayesWithLibraries:
    def __init__(self, file_name='train_data_processed.csv', test_file_name='test_data_processed.csv'):
        self.train_file_name = file_name
        self.test_file_name = test_file_name
        self.train_data = self.load_data(self.train_file_name)
        self.test_data = self.load_data(self.test_file_name)
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.accuracy = None

    def load_data(self, file_name=None):
        data = pd.read_csv(file_name)
        return data

    def preprocess_data(self):
        X = self.vectorizer.fit_transform(self.train_data['text'])
        y = self.train_data['is_spam'].astype('int')
        return X, y

    def train(self, X_train, y_train):
        self.classifier.fit(X_train, y_train)

    def predict(self, X_test):
        return self.classifier.predict(X_test)

    def evaluate_on_train_data(self):
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.train(X_train, y_train)
        y_pred_train = self.predict(X_train)
        self.accuracy = accuracy_score(y_train, y_pred_train)
        print('Bayes Naiv Spam Clasificator implementat cu biblioteci externe...')
        print()
        print(f"Acuratețea la antrenare obținută este de: {self.accuracy * 100:.2f}%")

    def evaluate_on_test_data(self):
        X_test = self.vectorizer.transform(self.test_data['text'])
        y_test = self.test_data['is_spam'].astype('int')
        y_pred_test = self.predict(X_test)

        misclassified_indices = [i for i, (true, pred) in enumerate(zip(y_test, y_pred_test)) if true != pred]
        self.plot_misclassified_instances(misclassified_indices, y_test, y_pred_test)
        self.plot_misclassification_pie_chart(misclassified_indices, y_test, y_pred_test)

        self.accuracy = accuracy_score(y_test, y_pred_test)
        print(f"Acuratețea la testare obținută este de: {self.accuracy * 100:.2f}%")

    def plot_misclassified_instances(self, misclassified_indices, y_test, y_pred_test):
        plt.figure(figsize=(10, 6))
        plt.scatter(misclassified_indices, y_pred_test[misclassified_indices], color='red', marker='x', label='Clasificate greșit')
        plt.scatter(misclassified_indices, y_test[misclassified_indices], color='blue', marker='o', label='Valori reale')
        plt.title('Clasificare greșită pe setul de date de testare \n (Alg Bayes Naiv)')
        plt.xlabel('Index instanță')
        plt.ylabel('Etichetă (0 - Non-Spam, 1 - Spam)')
        plt.legend()
        plt.show()

    def plot_misclassification_pie_chart(self, misclassified_indices, y_test, y_pred_test):
        correct_count = len(y_test) - len(misclassified_indices)
        misclassified_count = len(misclassified_indices)
        proportions = [correct_count, misclassified_count]
        plt.pie(proportions, labels=['Corect', 'Greșit'], autopct='%1.1f%%', colors=['#33B5E5', '#FF5733'])
        plt.title('Procentaj clasificare corectă/greșită (Alg Bayes Naiv)')
        plt.show()

    def cross_validate(self, cv=5):
        X, y = self.preprocess_data()
        scores = cross_val_score(self.classifier, X, y, cv=cv)
        mean_accuracy = scores.mean()
        print(f"Acuratețea la cross-validation obținută este de: {mean_accuracy * 100:.2f}%")

    def plot_word_frequency(self, data, label):
        words = []
        for msg in data[data['is_spam'] == label]['text'].tolist():
            for word in msg.split():
                words.append(word)

        word_counter = Counter(words)
        data_frame = pd.DataFrame(word_counter.most_common(30), columns=['Word', 'Frequency'])
        plt.figure(figsize=(12, 5))

        color_palette = sns.color_palette("Blues", n_colors=30)
        sns.barplot(x='Word', y='Frequency', data=data_frame, palette=color_palette)

        plt.xticks(rotation='vertical')
        if label == True:
            plt.title(f'Top 30 cuvinte în categoria Spam')
        else:
            plt.title(f'Top 30 cuvinte în categoria Non-Spam')
        plt.show()

    def plot_spam_word_frequency(self):
        self.plot_word_frequency(self.train_data, True)

    def plot_non_spam_word_frequency(self):
        self.plot_word_frequency(self.train_data, False)
   
   
if __name__ == '__main__':
    classifier = NaiveBayesWithLibraries()
    classifier.evaluate_on_train_data()
    classifier.cross_validate()
    classifier.evaluate_on_test_data()
    #
    # classifier.plot_spam_word_frequency()
    # classifier.plot_non_spam_word_frequency()
