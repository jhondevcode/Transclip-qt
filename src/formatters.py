from impl import AbstractFormatter


class PlainTextFormatter(AbstractFormatter):
    """Provides a formatter for plain texts, rearranging by paragraphs and removing strange characters from the text"""

    def __init__(self):
        """Default constructor"""
        super(PlainTextFormatter, self).__init__()

    def format(self, text: str):
        text_fixed: str = text.replace('\r', '')
        text_length: int = len(text)
        character_string_counter: int = 0
        character_string_buffer: list = []
        # format engine
        while character_string_counter < text_length:
            current_character = text_fixed[character_string_counter]
            if current_character == '-':
                try:
                    if text_fixed[character_string_counter + 1] == '\n':
                        character_string_buffer.append('')
                    else:
                        character_string_buffer.append(current_character)
                except IndexError:
                    character_string_buffer.append(current_character)
            elif current_character == '\n':
                try:
                    if text_fixed[character_string_counter - 1] == '.':
                        character_string_buffer.append('\n\n')
                    elif text_fixed[character_string_counter - 1] == '-':
                        character_string_buffer.append('')
                    else:
                        character_string_buffer.append(' ')
                except IndexError:
                    character_string_buffer.append(current_character)
            else:
                character_string_buffer.append(current_character)
            character_string_counter += 1
        return "".join(character_string_buffer)