from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()
nlp = StanfordCoreNLP('stanford-corenlp-full-2018-10-05')

# s = 'At the end of the day, successfully launching a new product means reaching the right audience and consistently delivering a very convincing message. To avoid spending money recklessly because of disjointed strategies, we have developed several recommendations.'
# s = 'I will be employed as a teacher.'
# s = 'I totally was a teacher.'

# print ('Tokenize:', nlp.word_tokenize(s))
# print ('Part of Speech:', nlp.pos_tag(s))
# print ('Named Entities:', nlp.ner(s))
# parse_s = nlp.parse(s)
# print ('Constituency Parsing:', parse_s)

# print ('Dependency Parsing:', nlp.dependency_parse(s))

# tree=Tree.fromstring(nlp.parse(s))
# tree.draw()

class Stack(object):
    """docstring for Stack"""
    def __init__(self):
        super(Stack, self).__init__()
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        if len(self.stack) == 0:
            return None
        node = self.stack[-1]
        self.stack = self.stack[:-1]
        return node
        

def negating(s):
    tree = Tree.fromstring(nlp.parse(s))
    stack = Stack()
    stack.push(tree)
    while True:
        node = stack.pop()
        if node is None:
            break
        if type(node[0]) == str:
            if node.label() in ['MD', 'VB', 'VBN', 'VBD', 'VBZ']:
                if node[0] in ['am', 'is', 'are', 'was', 'were', 'will', 'would', 'may', 'might', 'should', 'must']:
                    node[0] = '%s not' % (node[0])
                elif node[0] == 'can':
                    node[0] = 'cannot'
                elif node[0] == 'could':
                    node[0] = 'couldn\'t'
                else:
                    node[0] = 'didn\'t %s' % (wnl.lemmatize(node[0], 'v'))
                break
        else:
            sub_stack = []
            for sub_node in node:
                sub_stack.append(sub_node)
            for sub_node in sub_stack[::-1]:
                stack.push(sub_node)
    negative_text = ' '.join(tree.flatten())
    return negative_text

if __name__ == '__main__':
    s = 'At the end of the day, successfully launching a new product means reaching the right audience and consistently delivering a very convincing message. To avoid spending money recklessly because of disjointed strategies, we have developed several recommendations.'
    print(negating(s))
    s = 'I will be employed as a teacher.'
    print(negating(s))
    s = 'I totally was a teacher.'
    print(negating(s))
