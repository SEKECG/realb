class MessageProtocol:
    """
    Provides functionalities for formatting messages with optional metadata, parsing raw message strings into dictionaries, validating the structure of messages, and managing metadata within messages.
    """
    
    @staticmethod
    def add_metadata(message_dict, key, value):
        """
        Adds metadata to an existing message dictionary.
        """
        message_dict[key] = value
    
    @staticmethod
    def format_message(recipient, message, metadata=None):
        """
        Formats a message for transmission with optional metadata.
        """
        formatted_message = {"recipient": recipient, "message": message}
        if metadata:
            formatted_message.update(metadata)
        return formatted_message
    
    @staticmethod
    def get_metadata(message_dict, key):
        """
        Retrieves a value from the metadata of a message dictionary.
        """
        return message_dict.get(key)
    
    @staticmethod
    def parse_message(raw_message):
        """
        Parses a raw message string into a dictionary.
        """
        return eval(raw_message)
    
    @staticmethod
    def remove_metadata(message_dict, key):
        """
        Removes a key from the metadata of a message dictionary.
        """
        if key in message_dict:
            del message_dict[key]
    
    @staticmethod
    def validate_message(message_dict):
        """
        Validates the structure of the message.
        """
        required_keys = ["recipient", "message"]
        return all(key in message_dict for key in required_keys)