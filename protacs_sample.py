# -*- coding: utf-8 -*-
"""DeepChem provides a platform for researchers working with PROTACs datasets, offering tools like graph convolutional networks and molecular featurization to analyze and predict key properties of these molecules.

In this tutorial, we focus on using DeepChem to predict the Topological Polar Surface Area (TPSA) of molecules from their SMILES strings.

TPSA is a crucial molecular property, informing on a compound's absorption and distribution characteristics, which are vital for drug design.

1. Setup Environment
"""

pip install deepchem

"""Part 1: Setup and Data Preparation

Step 1: Data Preparation

  - Dataset File: The path to the CSV file containing the dataset. It should include at least two columns: one for the SMILES representation of molecules and another for the TPSA values.
  - Dataset used here as example: [Compound Group AAK1, KIAA1048](http://cadd.zju.edu.cn/protacdb/downloads)
  - Feature and Activity Fields: Identifies the columns in the dataset that contain the features ('Smiles') and the target variable ('Topological Polar Surface Area') for the prediction task.
"""

import deepchem as dc
import numpy as np

dataset_file = '/content/AAK1.csv'  # Update with the correct path
feature_field = "Smiles"
activity_field = "Topological Polar Surface Area"
tasks = [activity_field]

"""Step 2: Featurization

  - Featurizer: Converts the SMILES strings into a machine-usable format. The ConvMolFeaturizer is used here, which is suitable for graph-based models.
"""

featurizer = dc.feat.ConvMolFeaturizer()
loader = dc.data.CSVLoader(tasks=tasks, feature_field=feature_field, featurizer=featurizer)
dataset = loader.create_dataset(dataset_file)

"""Step 3: Dataset Splitting

  - Splitter: Divides the dataset into training, validation, and test sets. The RandomSplitter is used for a random split which is crucial for evaluating the model's performance on unseen data.
"""

splitter = dc.splits.RandomSplitter()
train_dataset, valid_dataset, test_dataset = splitter.train_valid_test_split(dataset)

"""Part 2: Model Building, Training, and Evaluation

Step 4: Model Building

  - Graph Convolutional Model: A type of neural network that directly works on graphs of molecules. It's initialized here for regression tasks, targeting the prediction of TPSA.
"""

model = dc.models.GraphConvModel(n_tasks=len(tasks), mode='regression')

"""Step 5: Training

  - Model Training: The model is trained on the training dataset for a specified number of epochs, allowing it to learn the relationship between the molecular features and TPSA values.
"""

model.fit(train_dataset, nb_epoch=50)

"""Step 6: Evaluation

  - Metric: Uses the Pearson R^2 score to evaluate the model's performance. This metric assesses the correlation between the predicted and actual TPSA values across the training, validation, and test datasets.
"""

metric = dc.metrics.Metric(dc.metrics.pearson_r2_score)
print("Training set score:", model.evaluate(train_dataset, [metric]))
print("Validation set score:", model.evaluate(valid_dataset, [metric]))
print("Test set score:", model.evaluate(test_dataset, [metric]))

"""Additional Evaluation

  - Variance in Predictions and Labels: Calculating the variance of the model's predictions and the actual labels helps in understanding the model's learning behavior and the diversity of the dataset.
"""

train_predictions = model.predict(train_dataset)
print("Variance in Train Predictions:", np.var(train_predictions, axis=0))
print("Variance in Train Labels:", np.var(train_dataset.y, axis=0))

"""Predictions"""

#Step 7: Generate predictions
tpsas_predicted = model.predict_on_batch(test_dataset.X[:10])

#Step 8: Display their SMILES, predicted TPSA, and actual TPSA
for molecule, predicted_tpsa, actual_tpsa in zip(test_dataset.ids[:10], tpsas_predicted, test_dataset.y[:10]):
    print("Predicted TPSA:", predicted_tpsa[0], "Actual TPSA:", actual_tpsa[0], "SMILES:", molecule)