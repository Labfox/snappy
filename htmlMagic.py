from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement


class ExtractedData:
    """
    Represents text data extracted from a source.

    Attributes:
        texts (list): A list of text strings extracted.
    """
    def __init__(self, texts):
        self.texts = texts

    def __str__(self):
        return f"ExtractedData(texts={self.texts})"


class MessageData(ExtractedData):
    """
        MessageData class inherits from the ExtractedData class to represent message data along with the author information.

        Methods:
            __init__(texts, author):
                Initializes the MessageData instance with provided texts and author.
            __str__():
                Returns a string representation of the MessageData instance.
    """
    def __init__(self, texts, author):
        super().__init__(texts)
        self.author = author

    def __str__(self):
        return f"MessageData(texts={self.texts}, author={self.author})"


class DateData(ExtractedData):
    """
    DateData

    A class to represent extracted data with an associated date.

    Inherits from:
    - ExtractedData

    Attributes:
    - texts (list): A list of extracted texts.
    - date (datetime): The date associated with the extracted data.
    """
    def __init__(self, texts, date):
        super().__init__(texts)
        self.date = date

    def __str__(self):
        return f"DateData(texts={self.texts}, date={self.date})"

class Conversation():
    """
        class Conversation():

        Represents a conversation with details such as title, status, timestamp, and image URL.

        Parameters
        ----------
        title : str
            The title of the conversation.
        status : str
            The status of the conversation (e.g., active, archived).
        timestamp : datetime
            The timestamp of when the conversation was created or last updated.
        image_url : str
            The URL of the image associated with the conversation.

        Methods
        -------
        __str__():
            Returns a string representation of the Conversation object.
    """
    def __init__(self, title, status, timestamp, image_url):
        self.title = title
        self.status = status
        self.timestamp = timestamp
        self.image_url = image_url

    def __str__(self):
        return f"Conversation(title={self.title}, status={self.status}, timestamp={self.timestamp}, image_url={self.image_url})"


def extract_messages(messages: list[WebElement]) -> list[ExtractedData]:
    """
    :param messages: List of HTML messages to be parsed and extracted.
    :type messages: list of str
    :return: List of extracted data objects which can be instances of MessageData, DateData, or ExtractedData.
    :rtype: list
    """
    extracted_data = []
    for message in messages:
        soup = BeautifulSoup(message.get_property("outerHTML"), 'html.parser')

        if soup.find('header'):
            message_type = 'message'
            author = soup.find('header').text.strip()
        elif soup.find('time'):
            message_type = 'date'
            author = None
            date = soup.find('time')['datetime']
        else:
            message_type = 'none'
            author = None
            date = None

        spans = soup.find_all('span', {'dir': 'auto', 'class': 'ogn1z nonIntl'})
        span_texts = [span.text for span in spans]

        if message_type == 'message':
            extracted_data.append(MessageData(
                span_texts,
                author
            ))
        elif message_type == 'date':
            extracted_data.append(DateData(
                span_texts,
                date
            ))
        else:
            extracted_data.append(ExtractedData(span_texts))

    return extracted_data


def interpret_conversations(conversations: list[WebElement]) -> list[Conversation]:
    """
    :param conversations: A list of HTML conversation snippets to be parsed.
    :type conversations: list
    :return: A list of dictionaries, each representing a parsed message with attributes such as title, status, timestamp, and image_url.
    :rtype: list
    """
    serialized = []

    for html_code in conversations:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_code.get_property("outerHTML"), 'html.parser')

        # Extract all the 'listitem' elements which could represent messages
        messages = soup.find_all('div', {'role': 'listitem'})

        parsed_messages = []

        for message in messages:
            # Extract the message title or label
            title_tag = message.find('span', {'class': 'FiLwP'})
            title = title_tag.text if title_tag else None

            # Extract the status (e.g., 'Received', 'Sent', etc.)
            status_span = message.find('span', {'id': lambda x: x and x.startswith('status')})
            status = status_span.text if status_span else None

            # Extract the timestamp
            time_tag = message.find('time')
            timestamp = time_tag['datetime'] if time_tag else None

            # Extract any image URLs
            img_tag = message.find('img', {'role': 'presentation'})
            img_url = img_tag['src'] if img_tag else None

            # Store the parsed message info in a dictionary
            parsed_messages.append(Conversation(
                title,
                status,
                timestamp,
                img_url
            ))

        serialized.append(*parsed_messages)

    return serialized