"""
A standalone partial implementation of sbt
https://www.solutionsbytext.com/api-support/api-documentation/
"""

from .resources import RequireVBT, RequestVBT, Carrier, SendTemplateMessage, GetMessageStatus


__all__ = [
    'RequireVBT', 'SendTemplateMessage', 'Carrier', 'GetMessageStatus', 'RequestVBT'
]

__version__ = '0.0.1'
