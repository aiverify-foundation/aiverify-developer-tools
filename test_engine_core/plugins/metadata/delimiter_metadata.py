from typing import Any, Union

from test_engine_core.plugins.enums.delimiter_type import DelimiterType


class DelimiterMetadata:
    """
    The DelimiterMetadata class comprises information on Delimiter
    """

    _data: Union[Any, None] = None
    _delimiter_type: DelimiterType = None

    def __init__(self, data: Any, delimiter_type: DelimiterType):
        self._data = data
        self._delimiter_type = delimiter_type

    def get_data(self) -> Any:
        """
        A method to return data value

        Returns:
             Any: the delimited data that is read from the file
        """
        return self._data

    def get_delimiter_type(self) -> DelimiterType:
        """
        A method to return delimiter type

        Returns:
            DelimiterType: the delimiter type that the data is being delimited
        """
        return self._delimiter_type
