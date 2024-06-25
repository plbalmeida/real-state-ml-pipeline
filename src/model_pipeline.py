from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline


class ModelPipeline:
    def __init__(self, categorical_cols, target):
        """
        Initialize the model pipeline with preprocessing and model steps.

        Args:
            categorical_cols (list): List of categorical column names.
            target (str): The target column name.
        """
        self.categorical_cols = categorical_cols
        self.target = target

        self.categorical_transformer = TargetEncoder()

        self.preprocessor = ColumnTransformer(
            transformers=[
                (
                    'categorical',
                    self.categorical_transformer,
                    self.categorical_cols
                )
            ]
        )

        self.steps = [
            ('preprocessor', self.preprocessor),
            ('model', GradientBoostingRegressor(**{
                "learning_rate": 0.01,
                "n_estimators": 300,
                "max_depth": 5,
                "loss": "absolute_error"
            }))
        ]

        self.pipeline = Pipeline(self.steps)

    def fit(self, X_train, y_train):
        """
        Fit the model pipeline on the training data.

        Args:
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
        """
        self.pipeline.fit(X_train, y_train)

    def predict(self, X_test):
        """
        Make predictions on the test data.

        Args:
            X_test (pd.DataFrame): Test features.

        Returns:
            np.ndarray: Predicted values.
        """
        return self.pipeline.predict(X_test)
