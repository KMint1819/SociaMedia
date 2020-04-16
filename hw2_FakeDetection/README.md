# Kaggle challenge - Fake News Detection
- [Link](https://www.kaggle.com/c/smm-hw2-fakenewsdetecion)
- Used modules:
    - pandas
    - numpy
    - tensorflow
    - sklearn
    - pickle

- Training Flow:
    1. Parse csv
        - Extracting only text and label
    2. Tokenize the text
        - Using keras.preprocessing.text.Tokenizer
        - After fitting the texts, save the tokenizer for prediction later.
    3. Turn texts to sequences by the tokenizer
    4. Pad texts
    5. Split data to training set and validation set by provided ratio
    6. Get network
        - Architecture:
            - Embedding
            - GlobalAveragePooling
            - FC_relu
            - FC_relu
            - FC_sigmoid
    7. Start training
    8. Evaluate
