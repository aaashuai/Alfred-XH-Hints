#!/usr/bin/python3
# encoding: utf-8

import re
import sys
from workflow import Workflow3
import json


code_regex = re.compile(r"[a-z]+")

with open("./code2ch.json") as fp:
    code2ch = json.load(fp)

with open("./ch2code.json") as fp:
    ch2code = json.load(fp)


def get_chars(code):
    tmp = code2ch

    for i in range(len(code)):
        tmp = tmp.get(code[i])
        if not tmp:
            break
    if not tmp:
        return
    return tmp["value"]


def make_card(code, ch):
    chs = get_chars(code)
    if not chs:
        return []

    card = []
    for i in range(len(chs)):
        if ch and ch not in chs:
            continue
        card.append((code, chs[i]))

    return card


def make_code_card(ch):
    codes = ch2code.get(ch)
    if not codes:
        return []

    code = []
    for i in range(len(codes)):
        ret = make_card(codes[i], ch)
        if not ret:
            continue
        code.extend(ret)
        if len(code) > 10:
            break
    return code


def main(wf):

    if not wf.args:
        return
    args = wf.args[0]

    rets = []
    if code_regex.match(args):
        cards = make_card(args, None)
        rets = [code + u" -> " + zh for code, zh in cards]
        subtitle = u"code -> zh"
    else:
        cards = make_code_card(args)
        rets = [zh + u" -> " + code for code, zh in cards]
        subtitle = u"zh -> code"

    for title in rets:
        wf.add_item(
            title=title,
            subtitle=subtitle,
            valid=True,
        )
    if not rets:
        wf.add_item(
            title=u"No Results",
            valid=True,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
