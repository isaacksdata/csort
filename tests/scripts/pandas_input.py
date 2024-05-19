import pandas as pd


class MyClass:
    def __init__(self):
        self._name = "myclass"
        print(123)
        print(456)

    def func(self):
        pass

    def _func(self):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def __len__(self):
        pass

    def query_df(self, df: pd.DataFrame) -> pd.DataFrame:
        query = "`my column` == 'my_value'"
        df = df.query(query)
        return df

    def query_df_single_quotes(self, df: pd.DataFrame) -> pd.DataFrame:
        query = '`my column` == "my_value"'
        df = df.query(query)
        return df

    @staticmethod
    def a_static_method():
        pass

    @classmethod
    def a_class_method(cls):
        pass

    @name.getter
    def name(self):
        return self._name
