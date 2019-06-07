import pytest
import mock
import urllib2 
import csv

from add_drop import * 

def test_sort_hitters_by_xwoba(): 
    a = {}
    b = {}

    a["xwoba"] = .400 
    b["xwoba"] = .370
    assert sortHittersByXwoba(a,b) == -1  
    
    a["xwoba"] = .370 
    b["xwoba"] = .400
    assert sortHittersByXwoba(a,b) == 1  
    
    a["xwoba"] = .400 
    b["xwoba"] = .400
    assert sortHittersByXwoba(a,b) == 0  

def test_sort_pitchers_by_xwoba(): 
    a = {}
    b = {}

    a["xwoba"] = .400 
    b["xwoba"] = .370
    assert sortPitchersByXwoba(a,b) == 1  
    
    a["xwoba"] = .370 
    b["xwoba"] = .400
    assert sortPitchersByXwoba(a,b) == -1  
    
    a["xwoba"] = .400 
    b["xwoba"] = .400
    assert sortPitchersByXwoba(a,b) == 0  

def test_query_statcast(monkeypatch):
    def mock_urlopen(url):
        class FakeResp():
            def __init__(self): 
                pass
            def readlines(self):
                lines = [] 
                lines.append("<\"player_name\">Mike Broccolino</\"player_name\">")
                lines.append("\n")
                lines.append(".500-.600")
         
                return lines

        fakeresp = FakeResp() 

        return fakeresp  
         
    start_date = "2019-05-04"
    end_date = "2019-06-02"

    monkeypatch.setattr(urllib2, "urlopen", mock_urlopen) 
    
    retval = query_statcast(start_date, end_date)

    assert retval[0].get("name") == "Mike Broccolino"
    assert retval[0].get("woba") == .500 
    assert retval[0].get("xwoba") == .600 
    #assert retval == []
