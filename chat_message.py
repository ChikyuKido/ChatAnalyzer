import os
import re
from datetime import datetime
from enum import Enum

from util import Util

class ChatType(Enum):
    SIGNAL = 1
    WHATSAPP = 2

class ChatMessage:
    def __init__(self,chat):
        self.chat_name = chat
        self.user = ""
        self.date = 0
        self.message = ""
        self.countN = 0
        self.countSlurs = 0

    def parse(self, line,chat_type):
        if chat_type == ChatType.SIGNAL:
            self.parseSignalMessage(line)
        elif chat_type == ChatType.WHATSAPP:
            self.parseWhatsappMessage(line)

    def convertToMap(self):
        return {"user": self.user, "date": self.date, "countN": self.countN, "countSlurs": self.countSlurs,"chatName": self.chat_name}

    def parseSignalMessage(self, line):
        if "***" in line:
            pattern = r"\[(.*?)\] .* <(.*?)> (.*)"
        else:
            pattern = r"\[(.*?)\] <(.*?)> (.*)"
        match = re.match(pattern, line)
        if match:
            date_str = match.group(1)
            self.user = match.group(2)
            self.message = match.group(3)
            self.date = datetime.strptime(date_str, "%b %d, %Y %H:%M:%S").date()
            self.countN = Util.countNWord(self.message)
            self.countSlurs = Util.countSlurs(self.message)
    def parseWhatsappMessage(self,line):
        pattern = r"(\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2}) - ([^:]+): (.+)"
        match = re.match(pattern, line)
        if match:
            date_str = match.group(1)
            self.user = match.group(2)
            self.message = match.group(3)
            self.date = datetime.strptime(date_str, "%m/%d/%y, %H:%M").date()
            self.countN = Util.countNWord(self.message)
            self.countSlurs = Util.countSlurs(self.message)

class Chat:
    chat_name: str
    messages: list[ChatMessage]
    filepath: str
    privateChat: bool
    chat_type: ChatType
    def __init__(self, filepath,chat_type):
        self.filepath = filepath
        self.privateChat = True
        self.messages = []
        self.chat_type = chat_type
        self.chat_name = os.path.basename(self.filepath).split(".")[0]

    def parse(self):
        messages = []
        first = True
        with open(self.filepath, "r") as f:
            for line in f:
                message = ChatMessage(self.chat_name)
                message.parse(line, self.chat_type)
                if message.date == 0:
                    # if the first messages fails to parse then it's a private chat
                    if first:
                        self.privateChat = False
                    continue
                messages.append(message)
                first = False
        self.messages = messages