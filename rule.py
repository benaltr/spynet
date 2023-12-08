from db import coll_rules
import datetime

class Rule:

    def __init__(self, name, action, url, from_, to, state):
        self.rule_name = name
        self.action = action
        self.url = url
        self.from_ = from_
        self.to = to
        self.state = state
        self.created = datetime.datetime.now()

    def add_rule(self):
        post = {"rule_name": self.rule_name,
                "action": self.action,
                "url": self.url,
                "from": self.from_, "to": self.to,
                "state": self.state,
                "created": self.created}
        
        coll_rules.insert_one(post) 

