from django.test import TestCase

# Create your tests here.
def longestCommonPrefix(strs):
    """
    :type strs: List[str]
    :rtype: str
    """
    first_word = strs[0]
    for item in strs:
        if first_word[0] not in item:
            return ""
    for k in range(2,len(first_word)):
        res = first_word[:k]
        for item in strs:
            if res not in item:
                return res[:(k - 1)]
    else:
        return first_word



print(longestCommonPrefix(["cag","cagecar","cagt"]))