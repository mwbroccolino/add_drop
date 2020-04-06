#! /usr/bin/env python

#--------
# Imports
#--------
import sys
import urllib2
import datetime
import csv
import json 

from optparse import OptionParser

import logging 
log = logging.getLogger()
log.setLevel(logging.INFO) 

def sortHittersByXwoba(a,b):
    if a["xwoba"] < b["xwoba"]:  return 1
    if a["xwoba"] == b["xwoba"]: return 0
    else: return -1

def sortPitchersByXwoba(a,b):
    if a["xwoba"] < b["xwoba"]:  return -1
    if a["xwoba"] == b["xwoba"]: return 0
    else: return 1

def query_statcast_barrel_leaderboard(player_type="batter", year=2019, debug=False): 
    # ----------------
    # Assemble the URL
    # ----------------
    url = "https://baseballsavant.mlb.com/leaderboard/statcast?type=%s&year=%d&position=&team=&min=q" % (player_type, year) 

    if debug: 
        log.info("Querying URL: %s" % url) 

    #--------------
    # Query the URL 
    #--------------
    data = urllib2.urlopen(url)
    data = data.readlines()

    #----------------
    # Gather the data
    #----------------
    odata = []
    for iii in range(len(data)):
        line = data[iii]
        if line.count("Trout"): 
            print len(line)
            print type(line) 
            print json.loads(line)
        """ 
        if line.count("\"player_name\""):
            name = line.split(">")[1].split("<")[0]
            spl = data[iii+2].strip().split("-")
            try: 
                woba  = float(spl[0])
                xwoba = float(spl[1])
            except ValueError: 
                woba  = 0.0
                xwoba = 0.0
            odata.append({"name":name, "woba":woba, "xwoba":xwoba})
            iii += 2
        """
    return odata
        
def query_statcast(start_date, end_date, player_type="batter", min_pas=10, debug=False): 
    #----------------
    # Assemble the URL
    #-----------------
    url  = "https://baseballsavant.mlb.com/statcast_search?"
    url += "hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hf"
    url += "NewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C&hfSit=&"
    url += "player_type=%s&hfOuts=&opponent=&pitcher_throws=&" % player_type
    url += "batter_stands=&hfSA=&game_date_gt=%s&game_date_lt=%s&" % (start_date, end_date)
    url += "hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&"
    url += "hfPull=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=wobadiff&"
    url += "player_event_sort=h_launch_speed&sort_order=desc&min_pas=%s#results" % str(min_pas)

    if debug: 
        print url 

    #--------------
    # Query the URL 
    #--------------
    data = urllib2.urlopen(url)
    data = data.readlines()

    if debug: 
        ofp = open("%s.txt" % player_type, "w")
        for line in data: 
            ofp.write(line)
        ofp.close()

    #----------------
    # Gather the data
    #----------------
    odata = []
    for iii in range(len(data)):
        line = data[iii] 
        if line.count("\"player_name\""):
            name = line.split(">")[1].split("<")[0]
            spl = data[iii+2].strip().split("-")
            try: 
                woba  = float(spl[0])
                xwoba = float(spl[1])
            except ValueError: 
                woba  = 0.0
                xwoba = 0.0
            odata.append({"name":name, "woba":woba, "xwoba":xwoba})
            iii += 2
    return odata

def read_fantrax_file(fantrax_file): 
    ifile = open(fantrax_file)

    data = csv.DictReader(ifile)

    return data

def write_output(input_list, ofile, keys=None):
    #--------------------- 
    # open the output file
    #--------------------- 
    ofile = open(ofile, "w") 

    #-------------
    # get the keys
    #-------------
    if not keys: 
        keys = []
        tmp = input_list[0]
        for key in tmp.keys(): 
            keys.append(key)

    #----------------- 
    # write the header
    #----------------- 
    for key in keys: 
        ofile.write("%s," % key)
    ofile.write("\n")

    #_----------------    
    # write the output  
    #k----------------
    for player in input_list:
        for key in keys: 
            ofile.write("%s," % str(player[key]))
        ofile.write("\n")

    ofile.close()

def main(opts, args): 
    pass 

def get_date_range(start_date, end_date): 
    start = start_date
    end   = end_date

    if not start_date: 
        start = "2019-03-20" # opening day
    if not end_date: 
        now = datetime.datetime.now() 
        if now.month < 10: 
            end = "%d-0%d-%d" % (now.year, now.month, now.day)
        else: 
            end = "%d-%d-%d" % (now.year, now.month, now.day)

    return start, end 

if __name__ == "__main__":
    #-------------
    # Command Line
    #-------------
    parser = OptionParser()

    default_min_pas   = "20"
    default_max_xwoba = ".240"
    default_min_xwoba = ".360" 

    parser.add_option("--start-date", default=None, help="Start date for statcast query. Form: YYYY-MM-DD")
    parser.add_option("--end-date", default=None, help="End date for statcast query. Form: YYYY-MM-DD")
    parser.add_option("--min-xwoba", default=default_min_xwoba, help="Mininum filter for hitter xwOBA [default: %s]" % default_min_xwoba)
    parser.add_option("--max-xwoba", default=default_max_xwoba, help="Maximum filter for pitcher xwOBA [default: %s]" % default_max_xwoba)
    parser.add_option("--min-pas", default=default_min_pas, help="Minimum number of plate appearances [default: %s]" % default_min_pas)
    parser.add_option("--h-file", default=None, help="If the file is Fantrax-players-SMCM Alums(19).csv, use --h-file=19")
    parser.add_option("--p-file", default=None, help="If the file is Fantrax-players-SMCM Alums(19).csv, use --p-file=19")
    parser.add_option("--debug", default=False, action="store_true") 
    
    opts, args = parser.parse_args()

    #--------------------------------------
    # Figure out the date range to query on
    #---------------------------------------
    start_date, end_date = get_date_range(opts.start_date, opts.end_date)

    # --------------------------
    # Get the Barrel Leaderboard
    # --------------------------
    leaderboard = query_statcast_barrel_leaderboard() 
    
    """
    #---------------
    # Query Statcast
    #---------------
    statcast_hitters  = query_statcast(start_date, end_date, min_pas=opts.min_pas, debug=opts.debug)
    statcast_pitchers = query_statcast(start_date, end_date, player_type="pitcher", min_pas=opts.min_pas, debug=opts.debug)

    #-----------------------
    # Read the fantrax file
    #-----------------------
    if opts.h_file: 
        hitter_fantrax_file = "/Users/michaelbroccolino/Downloads/Fantrax-players-SMCM Alums(%s).csv" % opts.h_file
    if opts.p_file:
        pitcher_fantrax_file = "/Users/michaelbroccolino/Downloads/Fantrax-players-SMCM Alums(%s).csv" % opts.p_file

    hitters  = read_fantrax_file(hitter_fantrax_file)
    pitchers = read_fantrax_file(pitcher_fantrax_file)

    #------------------------------------------------------
    # Match up the statcast data with the available players
    #------------------------------------------------------
    hitter_report  = []
    pitcher_report = []

    for player in hitters:
        try:
            #player_name     = "%s %s" % (player.get("Player","").split(",")[1].strip(), player.get("Player","").split(",")[0].strip()) 
            player_name     = player.get("Player", "").strip()  
        except: 
            print "Error creating player name from: %s" % str(player)
            continue 
        player["Tag"]   = ""
        player["woba"]  = 0.0
        player["xwoba"] = 0.0
        for p in statcast_hitters:
            if p.get("name") in player_name:
                pos = player.get("Position", "").split(",")[0]
                player["woba"]  = p.get("woba")
                player["xwoba"] = p.get("xwoba")
                player["Tag"]   = "%s %s %s" % (player_name, pos, player.get("Team", ""))
        if player_name.count("Drury"): 
            print player["woba"], player["xwoba"]
        if float(player.get("xwoba")) >= float(opts.min_xwoba):
            if player_name.count("Drury"):
                print "Adding Drury to hitter report"
            hitter_report.append(player)

    for player in pitchers:          
        try: 
            #player_name     = "%s %s" % (player.get("Player","").split(",")[1].strip(), player.get("Player","").split(",")[0].strip()) 
            player_name = player.get("Player", "").strip()
        except: 
            print "Error creating player name from: %s" % str(player)
            continue 
            
        player["Tag"]   = ""
        player["woba"]  = 1.0
        player["xwoba"] = 1.0
        for p in statcast_pitchers: 
            if p.get("name") in player_name:
                pos = player.get("Position", "").split(",")[0]
                player["woba"]  = p.get("woba")
                player["xwoba"] = p.get("xwoba")
                player["Tag"]   = "%s %s %s" % (player_name, pos, player.get("Team", ""))
        if float(player.get("xwoba")) <= float(opts.max_xwoba) and int(player.get("GS", 0)) > 0:
            pitcher_report.append(player) 

    #---------------
    # Sort the lists
    #---------------
    hitter_report  = sorted(hitter_report, sortHittersByXwoba)
    pitcher_report = sorted(pitcher_report, sortPitchersByXwoba)
    
    #-----------------
    # Write the output
    #-----------------
    hitter_keys  = ["Tag", "Score", "% Owned", "GP", "AB", "H", "2B", "3B", "HR", "R", "RBI", "SB", "CS", "BB", "SO", "AVG", "OBP", "SLG", "OPS", "woba", "xwoba"]
    pitcher_keys = ["Tag", "Score", "% Owned", "GP", "GS", "IP", "W", "L", "K", "BB", "SV", "HLD", "ERA", "WHIP", "woba", "xwoba"]

    write_output(hitter_report, "fa_hitters.csv", keys=hitter_keys)
    write_output(pitcher_report, "fa_pitchers.csv", pitcher_keys)

    """
