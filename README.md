# A snapchat API (webdriver)
## Features
### Connect to snapchat

```python
import snappy
import selenium.webdriver

snapchat_c = snappy.main.SnapchatCredentials("<your username>", "<your password>")

client = snappy.main.SnapchatClient(selenium.webdriver.Edge(), snapchat_c)
```

### List conversations

```python
client.listConversations()
```

### Get messages list on a conversation

```python
client.getMessagesBacklog(conversation)
```

### Send a message to a conversation

```python
client.sendMessage(conversation, message, cool_down=True)
```