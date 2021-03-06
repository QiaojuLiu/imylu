# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2018-06-26 14:41:08
@Last Modified by: tushushu
@Last Modified time: 2018-06-26 14:41:08
"""

from random import sample, choices, choice
from ..tree.decision_tree import DecisionTree


class RandomForest(object):
    def __init__(self):
        """RandomForest, randomly build some DecisionTree instance,
        and the average score of each DecisionTree

        Attributes:
        trees {list} -- 1d list with DecisionTree objects
        """

        self.trees = None
        self.tree_features = None

    def fit(self, X, y, n_estimators=10, max_depth=3, min_samples_split=2,
            max_features=None, n_samples=None):
        """Build a RandomForest classifier.

        Arguments:
            X {list} -- 2d list with int or float
            y {list} -- 1d list object with int 0 or 1

        Keyword Arguments:
            n_estimators {int} -- number of trees (default: {5})
            max_depth {int} -- The maximum depth of each tree. (default: {3})
            min_samples_split {int} -- The minimum number of samples required
            to split an internal node (default: {2})
            n_samples {int} -- number of samples (default: {None})
        """

        self.trees = []
        self.tree_features = []
        for _ in range(n_estimators):
            m = len(X[0])
            n = len(y)
            # Choose rows randomly with replacement
            if n_samples:
                idx = choices(population=range(n), k=min(n, n_samples))
            else:
                idx = range(n)
            # Choose columns randomly without replacement
            if max_features:
                n_features = min(m, max_features)
            else:
                n_features = int(m ** 0.5)
            features = sample(range(m), choice(range(1, n_features + 1)))
            # Subsample of X and y
            X_sub = [[X[i][j] for j in features] for i in idx]
            y_sub = [y[i] for i in idx]
            # Train decision tree classifier
            clf = DecisionTree()
            clf.fit(X_sub, y_sub, max_depth, min_samples_split)
            self.trees.append(clf)
            self.tree_features.append(features)

    def _predict(self, Xi):
        """Auxiliary function of predict.

        Arguments:
            Xi {list} -- 1d list object with int or float

        Returns:
            int -- 0 or 1
        """

        # Count positive vote
        pos_vote = 0
        for tree, features in zip(self.trees, self.tree_features):
            score = tree._predict([Xi[j] for j in features])
            if score >= 0.5:
                pos_vote += 1
        # Get negative vote
        neg_vote = len(self.trees) - pos_vote
        if pos_vote > neg_vote:
            return 1
        elif pos_vote < neg_vote:
            return 0
        # Return 1 or 0 randomly if number of positive vote equals to negative
        else:
            return choice([0, 1])

    def predict(self, X):
        """Get the prediction of y.

        Arguments:
            X {list} -- 2d list object with int or float

        Returns:
            list -- 1d list object with float
        """

        return [self._predict(Xi) for Xi in X]
