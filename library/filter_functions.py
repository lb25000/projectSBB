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
        Filtering the Dataframe based on a integer in a column.

        :param df: The DataFrame to be filtered.
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
        Filtering the Dataframe based on a integer in a column.

        :param df: The DataFrame to be filtered.
        :param word: Word to be searched and compared
        :param column_name: The column name to filter on
        :return: Filtered dataframe
        """
        filtered_df = df
        if word is not None:
            filtered_df = df[df[column_name] == float(word)]

        return filtered_df

    @staticmethod
    def filter_direct(df, word=None, column_name=None):
        """
        Filtering the Dataframe based on a number type in a column.

        :param df: The DataFrame to be filtered.
        :param word: Word to search for and compare, can be integer or float
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
        Filtering the Dataframe with an assignment operator, a number and in a specified column

        :param df: The DataFrame to be filtered.
        :param first_operator: First assignment operator which filters the data, for example, >=
        :param first_number: First number to be filtered
        :param second_operator: Second assignment operator which filters the data
        :param second_number: Second number to be filtered
        :param column_name: The column name to filter on
        :return: Filtered dataframe
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
    

    @staticmethod
    def filter_assignmentString(df, assignmentOp, word, column):
        """
        :param df: The dataframe
        :param assignmentOp: Is the assignment operator to the word
        :param word: Is the search word
        :param column: The column where the search happens
        :return: filtered dataframe
        
        """
        filtered_df = df
        ops = {
            "==": operator.eq
        }

        filtered_df = df[df[column] == word]
        return filtered_df


    