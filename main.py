# My simple interpreter to understand how interpreters work
# It will be only able to interprete simple "x [+-] y" expressions for now


# # My token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
EOF = 'EOF'

class Token():
  def __init__(self, token_type, value):
    self.token_type = token_type
    self.value = value
  
  def __str__(self):
    return 'Token(type: {}, value: {})'.format(self.token_type, self.value)


  def __repr__(self):
    return self.__str__()


class Interpreter():
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_token = None
    self.current_char = self.text[self.pos]


  def error(self):
    raise Exception('Error parsing input')


  def move_pos(self):
    self.pos += 1
    if self.pos > len(self.text) - 1:
      self.current_char = None
    else:
      self.current_char = self.text[self.pos]


  def skip_whitespace(self):
    while self.current_char is not None and self.current_char.isspace():
      self.move_pos()


  def integer(self):
    result = ''
    while self.current_char is not None and self.current_char.isdigit():
      result += self.current_char
      self.move_pos()
    return int(result)


  def get_next_token(self):
    """
    This will analyze client input and break it into tokens (lexical analyzer)
    """
    while self.current_char is not None:
  
      if self.current_char.isspace():
        self.skip_whitespace()
        continue

      if self.current_char.isdigit():
        return Token(INTEGER, self.integer())

      if self.current_char == '+':
        self.move_pos()
        return Token(PLUS, '+')
      
      if self.current_char == '-':
        self.move_pos()
        return Token(MINUS, '-')

      self.error()

    return Token(EOF, None)


  def move_to_next_token(self, type_of_token):
    if self.current_token.token_type == type_of_token:
      self.current_token = self.get_next_token()
    else:
      self.error()


  def expr(self):
    self.current_token = self.get_next_token()

    left = self.current_token
    self.move_to_next_token(INTEGER)

    operator = self.current_token
    if operator.token_type == PLUS:
      self.move_to_next_token(PLUS)
    else:
      self.move_to_next_token(MINUS)

    right = self.current_token
    self.move_to_next_token(INTEGER)

    if operator.token_type == PLUS:
      result = left.value + right.value
    else:
       result = left.value - right.value
    return result


def main():
  while True:
    try:
      text = input("calc> ")
    except EOFError:
      break
    if not text:
      continue
    
    interpreter = Interpreter(text)
    result = interpreter.expr()
    print(result)


if __name__ == '__main__':
  main()
