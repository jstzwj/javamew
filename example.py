

from javamew.lexer.tokenizer import JavaTokenizer


def _get_tokens(it):
    ret = []
    while not it.is_eof():
        ret.append(it.advance_token())
    return ret


tokenizer = JavaTokenizer("public static class Big_ma// Nice!")
tokens = _get_tokens(tokenizer)