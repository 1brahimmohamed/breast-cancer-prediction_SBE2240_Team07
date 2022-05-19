import pandas as pd
import matplotlib.pyplot as plt
import pickle

pd.set_option('display.max_column', None)  ## Displaying all columns ##

df = pd.read_csv('data.csv')  ## Importing Breast cancer data ##

df = df.drop(columns='id', axis=1)
# removing unnecessary columns : id column


df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

mean_features = list(df.columns[1:11])

se_features = list(df.columns[11:21])

worst_features = list(df.columns[21:31])

mean_features.append('diagnosis')
se_features.append('diagnosis')
worst_features.append('diagnosis')

corr_mean = df[mean_features].corr()
corr_se = df[se_features].corr()
corr_worst = df[worst_features].corr()

import seaborn as sns

plt.figure(figsize=(10, 10))
sns.heatmap(corr_mean, annot=True, cmap=plt.cm.CMRmap_r)

plt.figure(figsize=(10, 10))
sns.heatmap(corr_se, annot=True, cmap=plt.cm.CMRmap_r)

plt.figure(figsize=(10, 10))
sns.heatmap(corr_worst, annot=True, cmap=plt.cm.CMRmap_r)

## taking in account features having corr 60% or higher (considering mean)
## taking in account features having corr 50% or higher (considering se)
## taking in account features having corr 70% or higher (considering worst)


prediction_vars = ['radius_mean', 'perimeter_mean', 'area_mean', 'compactness_mean', 'concavity_mean',
                   'concave points_mean',
                   'radius_se', 'perimeter_se', 'area_se', 'concave points_se', 'radius_worst', 'perimeter_worst',
                   'area_worst',
                   'concavity_worst', 'compactness_worst']

from sklearn.model_selection import train_test_split

train, test = train_test_split(df, test_size=0.15, random_state=1)

train_X = train[prediction_vars]
train_y = train['diagnosis']
test_X = test[prediction_vars]
test_y = test['diagnosis']

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()

model.fit(train_X, train_y)

from sklearn.metrics import confusion_matrix

confusion = confusion_matrix(test_y, model.predict(test_X))
class_label = ["malignant", "benign"]
df_cm = pd.DataFrame(confusion, index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, cmap=plt.cm.CMRmap_r)
plt.title("Confusion Matrix", fontsize=15)
plt.xlabel("Predicted")
plt.ylabel("True")

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score

precision = precision_score(test_y, model.predict(test_X))

recall = recall_score(test_y, model.predict(test_X))

accuracy = accuracy_score(test_y, model.predict(test_X))

print("precision score :%5.3f " % (precision))
print("recall score :%5.3f " % (recall))
print("accuracy score :%5.3f " % (accuracy))


pickle.dump(model, open(r"D:\My PC\Projects\Python\Our Model Deploy\model.pkl", "wb"))