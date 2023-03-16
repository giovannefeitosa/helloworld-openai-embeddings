from sklearn.linear_model import LogisticRegression
import joblib
from commons.Configs import configs
from commons.File import file


class Model:
    def __init__(self, debug=False):
        self.debug = debug

    def train(self, x, y):
        return LogisticRegression(solver='lbfgs', random_state=42, max_iter=150).fit(x, y)

    def save(self, clf):
        # save model
        joblib.dump(clf, configs.generatedModelPath)
        print("Model saved to: ", configs.generatedModelPath)

    def load(self):
        if not file.exists(configs.generatedModelPath):
            print("Model not found at: ", configs.generatedModelPath)
            exit(1)
        return joblib.load(configs.generatedModelPath)


model = Model()
