import pytest
import mock
import urllib2 
import csv
import datetime 

from add_drop import * 

class Opts:
    def __init__(self): 
        opts.h_file = None
        opts.p_file = None
        opts.start_date = ""
        opts.end_date = "" 

def test_get_date_range(): 
    # test 1 
    start_date = None
    end_date = None

    start, end = get_date_range(start_date, end_date) 
    
    now = datetime.datetime.now()
 
    assert start == "2019-03-20"
    assert end == "%d-0%d-%d" % (now.year, now.month, now.day)   
    
    # tes 2 
    start_date = "2019-05-20"
    end_date = None

    start, end = get_date_range(start_date, end_date) 
    
    now = datetime.datetime.now()
 
    assert start == "2019-05-20"
    assert end == "%d-0%d-%d" % (now.year, now.month, now.day)   
 
    # test 3 
    start_date = "2019-05-20"
    end_date = "2019-05-27"

    start, end = get_date_range(start_date, end_date) 
 
    assert start == "2019-05-20"
    assert end == "2019-05-27"
    
    # test 3 
    start_date = None
    end_date = "2019-05-27"

    start, end = get_date_range(start_date, end_date) 
 
    assert start == "2019-03-20"
    assert end == "2019-05-27"
    
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
