

from javamew.lexer.tokenizer import JavaTokenizer


def _get_tokens(it):
    ret = []
    while not it.is_eof():
        ret.append(it.advance_token())
    return ret


tokenizer = JavaTokenizer("\"abcd\" ")
tokens = _get_tokens(tokenizer)