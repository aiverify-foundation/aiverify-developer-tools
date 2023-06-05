# Introduction
Today, there are more than 20 fairness metrics that cannot be all satisfied altogether [1]. The challenge then, is to provide a methodology that can assist in selecting the most appropriate fairness metric(s) to use in the use case. We called this the *Fairness Metrics Selection problem*.

In this guide, we will describe the list of fairness metrics available to use for both binary and multiclass classification. Then, we will describe our approach to our fairness decision tree, which is developed to address the *Fairness Metrics Selection Problem* in AI Verify.

This guide is beginner-focused, but it assumes a basic understanding of terminologies in in data science. We will briefly cover in the next section.

### Confusion Matrix
Most fairness metrics are calculated based on the performance measurement for classification models (sometimes placed in a form of matrix called confusion matrix).

In a **binary classification model**, this can be easily calculated with two outcomes. Typically, positive outcomes are denoted as *1* and negative outcomes are denoted as *0*. Any predicted outcomes that are not predicted positively or negatively (wrong predictions) are false positives and false negatives respectively while any predicted outcomes that are predicted correctly (correct predictions) are true positives and true negatives. This is shown in the table below.

| Class      | Description | Meaning | 
| ----------- | ----------- | ----------- |
| True Positives (TP)     | Both actual class and predicted value are positive.      | Correct Prediction       |
| True Negatives (TN)     | Both actual class and predicted value are negative.      | Correct Prediction       |
| False Positives (FP)     | The actual class is negative, but the predicted value is positive.     | Wrong Prediction       |
| False Negatives (FN)     | The actual class is positive, but the predicted value is negative.     | Wrong Prediction       |

In a **multiclass classification model** where there are more than two outcomes, the performance measurement needs to be computed concerning **a particular class**. In a multiclass classification model predicting whether an image is a cat, dog and mouse, the calculation for **cat** is shown in the table above.

| Class      | Description | Meaning | 
| ----------- | ----------- | ----------- |
| True Positives (TP)     |  The actual value and predicted value are both **cat**.     | Correct Prediction       |
| True Negatives (TN)     | The actual value and predicted value are both **NOT cat**.     | Correct Prediction       |
| False Positives (FP)     | The actual value is **NOT cat**, but the predicted value **cat**.    | Wrong Prediction       |
| False Negatives (FN)     | The actual value is **cat**, but the predicted value is **NOT cat**.     | Wrong Prediction       |

This calculation will be repeated for other classes (e.g., two separate measurements for dog and mouse using the same logic above).

## List of Fairness Metrics in AI Verify
There are more than 20 fairness metrics in the literature. However, some metrics are task-specific (e.g., steorotype can only be computed in NLP tasks) while some are more abstract to be understood and used in operation (e.g., sufficiency). In AI Verify, we have selected 10 commonly used fairness metrics.

*G = the entire dataset*

| Metrics      | Formula | Definition | 
| ----------- | ----------- | ----------- |
| Equal Selection Parity     |  Subgroup 1(TP + FP)/Subgroup 2(TP+FP)   |  The **difference** in the number of positive predictions between the subgroups  |
| Disparate Imapct     |  (TP + FP) | G    |  The **ratio** in the number of positive predictions between the subgroups  |


# Reference
[1]: The Impossibility of Theorem of Machine Fairness: A Casual Perspective. https://arxiv.org/pdf/2007.06024.pdf.