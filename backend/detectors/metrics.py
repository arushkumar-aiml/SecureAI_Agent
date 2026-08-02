# =============================
# Simple Metrics Calculator
# =============================

def calculate_metrics(y_true, y_pred):

    tp = sum(1 for t, p in zip(y_true, y_pred) if t==1 and p==1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t==0 and p==0)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t==0 and p==1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t==1 and p==0)

    accuracy = (tp+tn)/len(y_true)
    precision = tp/(tp+fp+1e-9)
    recall = tp/(tp+fn+1e-9)
    f1 = 2*precision*recall/(precision+recall+1e-9)

    return accuracy, precision, recall, f1


# Example test
y_true = [0,0,1,1]
y_pred = [0,0,1,1]

acc, p, r, f = calculate_metrics(y_true, y_pred)

print("Accuracy:", round(acc*100,2))
print("Precision:", round(p*100,2))
print("Recall:", round(r*100,2))
print("F1:", round(f*100,2))
