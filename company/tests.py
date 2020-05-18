# from django.test import TestCase

# Create your tests here.
import re
text = input('>>> ')
# pattern = re.compile('^[0-9]|[,.:-]$')
# pattern.match(text)

# pattern = '^[0-9]|[,.:-]$'
# pattern = "^(0[1-9]|1[012])[.](0[1-9]|[12][0-9]|3[01])[.][0-9]{4}(\s((0[1-9]|1[024])[:]([0-5][0-9])))?$"
# pattern = "^(0[1-9]|1[012])[.](0[1-9]|[12][0-9]|3[01])[.][0-9]{4}(\s(([01][0-9]|[012][0-3]):([0-5][0-9])))*$"
# s = '^(([01][0-9]|[012][0-3]):([0-5][0-9]))*$'
pattern = '((\(\d{2}\) ?)|(\d{2}/))?\d{2}/\d{4} ([0-2][0-9]\:[0-6][0-9])'


x = re.match(pattern, text)
print(x)
while x is None:
    text = input('>>> ')
    x = re.match(pattern, text)
print( 'OK')