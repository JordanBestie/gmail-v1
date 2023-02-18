from langchain.text_splitter import SpacyTextSplitter
from config import UTILITIES
import re
from langchain.utilities.google_search import GoogleSearchAPIWrapper
from langchain.utilities.gmail_search import GmailAPIWrapper

class AIAssistant:
    def __init__(self, query, content):
        self.query = query
        self.content = content

    def tokenize(self,separator=" ."):
        splitter = SpacyTextSplitter(separator=separator)
        tokens = splitter.tokenization(self.query)
        return tokens

    def execute_utility(self):
        query_tokens = self.tokenize(separator=",")
        current_utility = None
        for utility in UTILITIES:
            tags = self.tokenize(utility["tags"])
            extracted_tags = set(query_tokens).intersection(tags)
            for tag in extracted_tags:
                reg_ex = re.search(tag + ' (.*)', self.query)
                if reg_ex:
                    current_utility = utility
                    break
        try:
            wrapper = eval(current_utility["wrapper"])()
            func = current_utility["func"]
            output_function = getattr(wrapper, func)(self.content)
            return True,output_function
        except Exception as e:
            return False, str(e)

