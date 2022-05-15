import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

names = ["a","b","c","d","e","f","g","h","i","j","label"]

def KNN(indiv, train, k):
    global names
    # calculate the distance between the indiv and train
    dist = np.sqrt(np.sum((indiv - train[names[:-1]])**2, axis=1))
    # sort the distance
    sort_keys= dist.argsort()
    # get the label of the k nearest data
    labels = train["label"][sort_keys[:k]]
    # get the most frequent label
    # return np.argmax(np.bincount(labels,weights=range(len(labels))))
    return np.argmax(np.bincount(labels))

def calculate_accuracy_KNN(test, train_norm, k):
    global names
    # get the number of test data
    n = len(test)
    # get the number of correct prediction
    correct = 0
    # get the number of wrong prediction
    wrong = 0
    # for each test data
    for i in range(n):
        # get the label of the test data
        label = test.iloc[i]["label"]
        # get the label of the predicted data
        predicted = KNN(test.iloc[i][names[:-1]], train_norm, k)
        # if the label is the same as the predicted label
        # print(label, predicted)
        if label == predicted:
            # increase the number of correct prediction
            correct += 1
        else:
            # increase the number of wrong prediction
            wrong += 1
    # print("correct:", correct)
    return correct / (n)


def main():
    df = pd.read_csv('data.txt',sep=";")
    global names
    df.columns = names
    # change the label to -1 and 1
    df["label"] = df["label"].apply(lambda x: -1 if x == 0 else 1)

    # shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    # split the data into test and train
    train = df.iloc[:int(len(df)*0.8),:]
    test = df.iloc[int(len(df)*0.8):,:]

    print("raw:")
    print(df.head())
    means = train[names[:-1]].mean()
    stds = train[names[:-1]].std()
    train_norm = (train[names[:-1]] - means) / stds
    train_norm["label"] = train["label"]
    print("normalized:")
    print(train_norm.head())

    # find correlation
    corr = train_norm.corr()
    print("correleation is:")
    print(corr)
    # find the most correlated features
    corr_features = corr.iloc[-1,:-1].sort_values(ascending=False)
    print("most correlated features are:")
    print(corr_features)
    # find the most correlated features

    # norm test
    test_norm = (test[names[:-1]] - means) / stds
    test_norm["label"] = test["label"]
    print("test:")
    print(test_norm.head())
    # calculate the accuracy for k in range 100
    k = np.arange(1,4)
    accuracy = []
    for i in k:
        print("k =", i)
        accuracy.append(calculate_accuracy_KNN(test_norm, train_norm, i))
    # calculate the rolling average
    kernel_size = 3
    kernel = np.ones(kernel_size) / kernel_size
    accuracy_convolved = np.convolve(np.array(accuracy), kernel, mode='same')

    # choose the best k
    best_k = k[np.argmax(accuracy_convolved)]
    print("best k:", best_k)
    # calculate the accuracy for the best k
    best_acc = calculate_accuracy_KNN(test_norm, train_norm, best_k)
    print("accuracy:", best_acc)

    # plot the accuracy
    plt.plot(k, accuracy, label="accuracy")
    plt.plot(k, accuracy_convolved, label="rolling average")
    plt.legend()
    plt.xlabel("k")
    plt.ylabel("accuracy")
    # draw a line for the best k
    plt.axvline(best_k, color='r', linestyle='--')
    plt.show()







if __name__ == '__main__':
    main()