"""
Contains the FilterFunctions class with static methods for filtering the DataFrame.
"""
import operator
import pandas as pd

class FilterFunctions:
    """
    The class enables filtering in DataFrame.
    """
    @staticmethod
    def filter_string(df, word=None, column_name=None):
        """
        Filter the DataFrame based on a word in a specified column.
        
        :param df: The DataFrame to be filtered.
        :param word: The word to be searched and compared.
        :param column_name: The column name to filter on.
        :return: The filtered DataFrame.
        """
        filtered_df = df  # Assign the DataFrame to a new variable
        if word is not None:
            word_in_capitals = word.upper()  # Convert the word to uppercase for comparison
            # Check if the specified column exists in the DataFrame
            mask = df[column_name].str.upper().str.contains(word_in_capitals) if column_name in df.columns else True
            # Replace all occurrences of pd.NA with False
            mask = mask.replace(pd.NA, False)
            # Filter the DataFrame based on the mask
            filtered_df = df[mask]
        return filtered_df

    @staticmethod
    def filter_integer(df, word=None, column_name=None):
        """
        :param word: Word to be searched and compared
        :param column_name: The column name to filter on
        :return: Filtered dataframe
        """
        filtered_df = df
        if word is not None:
            filtered_df = df[df[column_name] == int(word)]

        return filtered_df

    @staticmethod
    def filter_float(df, word=None, column_name=None):
        """
        :param word: wort nachdem gesucht und verglichen wird
        :param column_name: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes datafram
        """
        filtered_df = df
        if word is not None:
            filtered_df = df[df[column_name] == float(word)]

        return filtered_df

    @staticmethod
    def filter_direct(df, word=None, column_name=None):
        """
        :param word: Word to search for and compare
        :param column_name: The column name to filter on
        :return: Filtered dataframe
        """
        if word.isdigit():
            word = int(word)
        else:
            word = float(word)
        filtered_df = df
        if word is not None:
            filtered_df = df[df[column_name] == word]

        return filtered_df

    @staticmethod
    def filter_general(df, first_operator=None, first_number=None,
                       second_operator=None, second_number=None, column_name=None):
        """
        :param first_operator: erster assignment operator nach dem gefiltert wird. Z.B >=
        :param first_number: erste grösse nachdem gefiltert wird, z.b. 200
        :param second_operator: zweiter assignment operator nach dem gefiltert wird. Z.B <
        :param second_number: zweite grösse nachdem gefiltert wird, z.b. 400
        :param column_name: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes dataframe
        """
        ops = {
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        '!=': operator.ne,
        ">=": operator.ge,
        ">": operator.gt
        }
        if first_number.isdigit():
            first_number = int(first_number)
        else:
            first_number = float(first_number)
        filtered_df = df
        if first_operator is not None and second_number is None:
            filtered_df = filtered_df[ops[first_operator](filtered_df[column_name], first_number)]
        if first_operator is not None and second_number is not None:
            filtered_df = filtered_df[(ops[first_operator](filtered_df[column_name], first_number))
                              & (ops[second_operator](filtered_df[column_name], second_number))]

        return filtered_df
    