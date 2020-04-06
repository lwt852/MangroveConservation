#import ExploratoryAnalysis as sentiment
import pytest

def test_Tokenize():
    data = "@abc yes good"
    assert ea.Tokenize(data) == ["SCREEN_NAME", "yes", "good"]

def test_GetLemma():
    data = "cars"
    assert ea.GetLemma(data) == "car"
    
def test_ProcessToken():
    data = "many cars on these streets"
    assert ea.ProcessToken(data) == ["many" , "car", "street"]
    
def test_Prepare():
    data = ["many cars on these streets", "yes that is good"]
    assert ea.Prepare(data) == [["many", "car", "street"], ["yes", "good"]]

def test_LDAtopic():
    data = [["bus"],["good", "busy"]]
    t, m, c, d = ea.LDAtopic(data,1,1)
    assert t == [(0, '0.333*"bus"')]
    assert c == [[(0,1)],[(1,1),(2,1)]]
