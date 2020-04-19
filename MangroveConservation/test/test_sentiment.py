from MangroveConservation import sentiment_analysis1 as sentiment
import pytest

def test_Tokenize():
    data = "Are u looking for Sundarban Mangrove Forest To protect the environment?"
    assert sentiment.Tokenize(data) == ['are', 'u', 'looking', 'for', 'sundarban', 'mangrove', 'forest', 'to', 'protect', 'the', 'environment','?']

def test_GetLemma():
    data = "forests"
    assert sentiment.GetLemma(data) == "forest"
    
def test_ProcessToken():
    data = "Are u looking for Sundarban Mangrove Forest To protect the environment"
    assert sentiment.ProcessToken(data) == ['u', 'looking', 'sundarban', 'mangrove', 'forest', 'protect', 'environment']
    
