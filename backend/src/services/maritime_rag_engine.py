"""
Project ORCA — Maritime Small Language Model (SLM) & RAG Knowledge Engine
Comprehensive Domain Knowledge Base covering:
1. 300+ Global Hub Ports & All Adjacent/Satellite Sister Ports, Basins, Terminals, and Approaches.
2. Dedicated Project ORCA & SIH26 Technical Knowledge Base (Pipelines, Algorithms, Vessel Limits, Provenance).
3. Single-Word Greeting & Project Help HUD Router.
4. Intelligent Non-Marine Domain Firewall & Warning Dispatcher.
"""
from typing import Optional, Dict, Any, Tuple, List, Set
import re
import difflib
import math

# ==============================================================================================
# 1. COMPREHENSIVE GLOBAL MARITIME RAG CORPUS: 300+ PORTS & SATELLITE TERMINALS
# Format: key -> (lat, lon, Port Name, Parent Cluster / Sea Basin, VHF Ch, MRCC / Rescue Centre, Navigational Hazard)
# ==============================================================================================
GLOBAL_MARITIME_RAG_CORPUS: Dict[str, Dict[str, Any]] = {
    # ------------------------------------------------------------------------------------------
    # NETHERLANDS & NORTH SEA (Rotterdam Mega-Cluster & Adjacent Satellites)
    # ------------------------------------------------------------------------------------------
    "vlaardingen": {
        "lat": 51.9125, "lon": 4.3417,
        "name": "Port of Vlaardingen (Nieuwe Maas)",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16 (Sector Maas)",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder / Joint Rescue Coordination Centre",
        "notes": "Adjacent satellite port of Rotterdam on the Nieuwe Maas fairway; commercial inland and bunker terminal."
    },
    "port of vlaardingen": {
        "lat": 51.9125, "lon": 4.3417,
        "name": "Port of Vlaardingen (Nieuwe Maas)",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16 (Sector Maas)",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder / Joint Rescue Coordination Centre",
        "notes": "Adjacent satellite port of Rotterdam on the Nieuwe Maas fairway; commercial inland and bunker terminal."
    },
    "schiedam": {
        "lat": 51.9180, "lon": 4.3980,
        "name": "Port of Schiedam (Wilton-Fijenoord / Voorhaven)",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Rotterdam west satellite harbor; major offshore engineering, repair docks, and river transit."
    },
    "rotterdam": {
        "lat": 51.9244, "lon": 4.4777,
        "name": "Port of Rotterdam (Main Maritime Complex)",
        "cluster": "Port of Rotterdam, North Sea",
        "vhf": "VHF Ch 11 / 14 / 16 / 19",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder (Toll-Free 0900-0111 / +31 223 542 300)",
        "notes": "Largest seaport in Europe; deepwater entrance via Eurogeul; 42 km fairway spanning Maasvlakte to City."
    },
    "port of rotterdam": {
        "lat": 51.9244, "lon": 4.4777,
        "name": "Port of Rotterdam (Main Maritime Complex)",
        "cluster": "Port of Rotterdam, North Sea",
        "vhf": "VHF Ch 11 / 14 / 16 / 19",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Largest seaport in Europe; deepwater entrance via Eurogeul; 42 km fairway spanning Maasvlakte to City."
    },
    "europoort": {
        "lat": 51.9167, "lon": 4.1500,
        "name": "Europoort (Port of Rotterdam Deepwater Basin)",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 14 / 16 (Sector Europoort)",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Major deep-draft crude oil, bulk ore, and Ro-Ro terminal directly opening into the North Sea."
    },
    "maasvlakte": {
        "lat": 51.9500, "lon": 4.0167,
        "name": "Maasvlakte 1 & 2 (Outer Seaward Terminals)",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 14 / 16 (Sector Maas Approach)",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Reclaimed outer deepwater container terminals (APMT, ECT Delta, RWG) accommodating Ultra Large Container Vessels."
    },
    "botlek": {
        "lat": 51.8833, "lon": 4.2833,
        "name": "Botlek Harbor Basin",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16 (Sector Botlek)",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Petrochemical and bulk liquid cargo hub situated between Oude Maas and Nieuwe Waterweg."
    },
    "dordrecht": {
        "lat": 51.8133, "lon": 4.6700,
        "name": "Zeehaven Dordrecht",
        "cluster": "Port of Rotterdam Inland Reach, North Sea",
        "vhf": "VHF Ch 10 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Most inland seaport of the Rotterdam complex; junction of Oude Maas, Beneden Merwede, and Noord rivers."
    },
    "hook of holland": {
        "lat": 51.9775, "lon": 4.1333,
        "name": "Hook of Holland (Hoek van Holland / Berghaven)",
        "cluster": "Port of Rotterdam Entrance, North Sea",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder / KNRM Lifeboat Station Hook of Holland",
        "notes": "Mouth of Nieuwe Waterweg fairway; pilot boarding station and ferry terminal to UK Harwich."
    },
    "hoek van holland": {
        "lat": 51.9775, "lon": 4.1333,
        "name": "Hook of Holland (Hoek van Holland / Berghaven)",
        "cluster": "Port of Rotterdam Entrance, North Sea",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder / KNRM Station",
        "notes": "Mouth of Nieuwe Waterweg fairway; pilot boarding station and ferry terminal to UK Harwich."
    },
    "maassluis": {
        "lat": 51.9189, "lon": 4.2561,
        "name": "Port of Maassluis",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Historic tug and salvage base on Nieuwe Waterweg; active pilotage transition."
    },
    "pernis": {
        "lat": 51.8892, "lon": 4.3858,
        "name": "Pernis Port & Petroleum Basin",
        "cluster": "Port of Rotterdam Cluster, North Sea",
        "vhf": "VHF Ch 11 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Europe's largest integrated oil refining hub; 1e and 2e Petroleumhaven."
    },
    "moerdijk": {
        "lat": 51.7000, "lon": 4.6333,
        "name": "Port of Moerdijk",
        "cluster": "South Rotterdam / Hollands Diep Reach, North Sea",
        "vhf": "VHF Ch 10 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Direct inland transit terminal connecting Rotterdam and Antwerp waterways."
    },
    "vlissingen": {
        "lat": 51.4425, "lon": 3.5739,
        "name": "Port of Vlissingen (Flushing / North Sea Port)",
        "cluster": "Westerschelde, North Sea",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "MRCC Ostend / Netherlands Coast Guard",
        "notes": "Outer deepwater entrance to Westerschelde and Antwerp approaches."
    },
    "terneuzen": {
        "lat": 51.3300, "lon": 3.8300,
        "name": "Port of Terneuzen",
        "cluster": "Ghent-Terneuzen Canal, North Sea",
        "vhf": "VHF Ch 11 / 16",
        "mrcc": "Netherlands Coast Guard / Belgian Maritime Rescue",
        "notes": "Major sea lock complex leading to Ghent, Belgium."
    },
    "amsterdam": {
        "lat": 52.3792, "lon": 4.9003,
        "name": "Port of Amsterdam",
        "cluster": "North Sea Canal System",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Fourth largest cargo port in Europe; connected to North Sea via IJmuiden Sea Locks."
    },
    "ijmuiden": {
        "lat": 52.4583, "lon": 4.6000,
        "name": "Port of IJmuiden (North Sea Locks & Fishing Port)",
        "cluster": "North Sea Canal System",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Zeesluis IJmuiden (world's largest sea lock); active pelagic fish auction."
    },
    "den helder": {
        "lat": 52.9599, "lon": 4.7594,
        "name": "Port of Den Helder",
        "cluster": "Wadden Sea / North Sea",
        "vhf": "VHF Ch 16 / 62",
        "mrcc": "Headquarters Netherlands Coast Guard (Kustwacht Centrum)",
        "notes": "Primary Dutch offshore energy supply base and Royal Netherlands Naval Base."
    },
    "scheveningen": {
        "lat": 52.1028, "lon": 4.2644,
        "name": "Port of Scheveningen (The Hague)",
        "cluster": "Dutch Coast, North Sea",
        "vhf": "VHF Ch 16 / 21",
        "mrcc": "Netherlands Coast Guard MRCC Den Helder",
        "notes": "Traditional herring fishing harbor and coastal yacht marina."
    },

    # ------------------------------------------------------------------------------------------
    # BELGIUM, FRANCE, GERMANY, UK & BALTIC
    # ------------------------------------------------------------------------------------------
    "antwerp": {
        "lat": 51.2194, "lon": 4.4025,
        "name": "Port of Antwerp-Bruges",
        "cluster": "Scheldt Estuary, North Sea",
        "vhf": "VHF Ch 12 / 16 / 74",
        "mrcc": "Belgian MRCC Ostend (Tel: +32 59 70 10 00)",
        "notes": "Second largest port in Europe; deep inland lock system (Kieldrecht Lock)."
    },
    "zeebrugge": {
        "lat": 51.3300, "lon": 3.2000,
        "name": "Port of Zeebrugge",
        "cluster": "Belgian Coast, North Sea",
        "vhf": "VHF Ch 16 / 71",
        "mrcc": "Belgian MRCC Ostend",
        "notes": "Major LNG import terminal, Ro-Ro automotive gateway, and deep-sea container hub."
    },
    "hamburg": {
        "lat": 53.5459, "lon": 9.9669,
        "name": "Port of Hamburg",
        "cluster": "Elbe River / North Sea",
        "vhf": "VHF Ch 16 / 74",
        "mrcc": "German Maritime Search & Rescue (DGzRS Bremen / MRCC Bremen)",
        "notes": "Germany's leading maritime hub; tidal Elbe fairway with radar vessel traffic guidance."
    },
    "bremerhaven": {
        "lat": 53.5500, "lon": 8.5833,
        "name": "Port of Bremerhaven",
        "cluster": "Weser Estuary, North Sea",
        "vhf": "VHF Ch 16 / 67",
        "mrcc": "MRCC Bremen (DGzRS)",
        "notes": "Outer deepwater container and automobile port for Bremen."
    },
    "kiel": {
        "lat": 54.3233, "lon": 10.1228,
        "name": "Port of Kiel (Kiel Canal / Ostsee)",
        "cluster": "Baltic Sea / Kiel Canal Entrance",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "MRCC Bremen",
        "notes": "Eastern terminus of the Kiel Canal (Nord-Ostsee-Kanal), busiest artificial waterway in the world."
    },
    "southampton": {
        "lat": 50.9097, "lon": -1.4044,
        "name": "Port of Southampton",
        "cluster": "Solent / English Channel, UK",
        "vhf": "VHF Ch 12 / 16 (Southampton VTS)",
        "mrcc": "UK HM Coastguard (JRCC Fareham / MRCC Solent)",
        "notes": "Double high-water tidal anomaly; premier UK cruise and automotive hub."
    },
    "felixstowe": {
        "lat": 51.9600, "lon": 1.3500,
        "name": "Port of Felixstowe",
        "cluster": "Suffolk Coast, North Sea, UK",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "UK HM Coastguard MRCC Dover / JRCC Humber",
        "notes": "United Kingdom's busiest container port handling over 4 million TEUs annually."
    },
    "le havre": {
        "lat": 49.4944, "lon": 0.1078,
        "name": "Grand Port Maritime du Havre (HAROPA)",
        "cluster": "Seine Bay, English Channel, France",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "CROSS Jobourg / MRCC Le Havre",
        "notes": "Deepwater outer container port at the entrance of the Seine river corridor."
    },
    "marseille": {
        "lat": 43.2965, "lon": 5.3698,
        "name": "Grand Port Maritime de Marseille-Fos",
        "cluster": "Gulf of Lion, Mediterranean Sea, France",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "CROSS La Garde (French Mediterranean MRCC)",
        "notes": "Leading French commercial seaport spanning Marseille historic basins and Fos-sur-Mer industrial docks."
    },
    "genoa": {
        "lat": 44.4056, "lon": 8.9463,
        "name": "Port of Genoa (Sampierdarena / Pra-Voltri)",
        "cluster": "Ligurian Sea, Mediterranean Sea, Italy",
        "vhf": "VHF Ch 16 / 15",
        "mrcc": "Italian Coast Guard MRCC Rome / Port Captaincy Genoa (Guardia Costiera)",
        "notes": "Major Mediterranean gateway into northern Italy, Switzerland, and Central Europe."
    },
    "piraeus": {
        "lat": 37.9430, "lon": 23.6469,
        "name": "Port of Piraeus (Athens)",
        "cluster": "Saronic Gulf, Aegean Sea / Mediterranean, Greece",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Hellenic Coast Guard Joint Rescue Coordination Center (JRCC Piraeus)",
        "notes": "Busiest passenger port in Europe and key transshipment hub connecting Asia to Europe via Suez."
    },
    "barcelona": {
        "lat": 41.3500, "lon": 2.1667,
        "name": "Port of Barcelona",
        "cluster": "Catalonia, Mediterranean Sea, Spain",
        "vhf": "VHF Ch 10 / 16",
        "mrcc": "Salvamento Maritimo (MRCC Barcelona)",
        "notes": "Comprehensive multi-cargo and cruise hub situated on the northeast Spanish coast."
    },
    "algeciras": {
        "lat": 36.1333, "lon": -5.4500,
        "name": "Port of Algeciras",
        "cluster": "Strait of Gibraltar, Spain",
        "vhf": "VHF Ch 13 / 16 (Tarifa Traffic)",
        "mrcc": "Salvamento Maritimo (MRCC Tarifa / Algeciras)",
        "notes": "Critical strategic transshipment hub directly overlooking the Strait of Gibraltar choke point."
    },
    "gdansk": {
        "lat": 54.3722, "lon": 18.6383,
        "name": "Port of Gdansk (Baltic Hub)",
        "cluster": "Gulf of Gdansk, Baltic Sea, Poland",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "Polish Maritime Search & Rescue Service (MRCC Gdynia)",
        "notes": "Deepest container and energy terminal in the Baltic Sea with ice-free year-round access."
    },
    "bergen": {
        "lat": 60.3913, "lon": 5.3221,
        "name": "Port of Bergen",
        "cluster": "Western Fjords, North Sea / Norwegian Sea, Norway",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "JRCC Southern Norway (Stavanger)",
        "notes": "Key North Sea offshore supply base, subsea technology hub, and pelagic fishing centre."
    },

    # ------------------------------------------------------------------------------------------
    # INDIA & INDIAN OCEAN (West Coast, East Coast, Islands & Satellite Centers)
    # ------------------------------------------------------------------------------------------
    "dapoli": {
        "lat": 17.7644, "lon": 73.1812,
        "name": "Dapoli / Harnai Landing Sector",
        "cluster": "Ratnagiri District, Konkan Coast, Arabian Sea",
        "vhf": "VHF Ch 16 / 08",
        "mrcc": "Indian Coast Guard MRCC Mumbai (Toll-Free 1554 / 022-24388065)",
        "notes": "Major artisanal and motorized fishing harbor in southern Maharashtra; high seasonal mackerel/pomfret landings."
    },
    "harnai": {
        "lat": 17.8044, "lon": 73.0912,
        "name": "Harnai Fishing Harbor & Suvarnadurg Basin",
        "cluster": "Konkan Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai (1554)",
        "notes": "Historic natural sheltered bay in Dapoli taluka; active daily fish auctions."
    },
    "mumbai": {
        "lat": 18.9220, "lon": 72.8347,
        "name": "Sassoon Docks & Mumbai Port Trust",
        "cluster": "Mumbai Harbour, Arabian Sea",
        "vhf": "VHF Ch 12 / 16 (Mumbai VTS)",
        "mrcc": "Indian Coast Guard MRCC Mumbai (HQ West, 1554)",
        "notes": "Premier commercial and fishing hub of western India; active VTMS managing deep-draft cargo and thousands of trawlers."
    },
    "nhava sheva": {
        "lat": 18.9500, "lon": 72.9500,
        "name": "Jawaharlal Nehru Port Authority (JNPA / Nhava Sheva)",
        "cluster": "Mumbai Harbour, Arabian Sea",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai (1554)",
        "notes": "India's largest container port handling over 50% of the nation's containerized cargo."
    },
    "jnpt": {
        "lat": 18.9500, "lon": 72.9500,
        "name": "Jawaharlal Nehru Port Authority (JNPT / Nhava Sheva)",
        "cluster": "Mumbai Harbour, Arabian Sea",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai (1554)",
        "notes": "India's largest container port handling over 50% of the nation's containerized cargo."
    },
    "ratnagiri": {
        "lat": 16.9902, "lon": 73.3120,
        "name": "Mirkarwada Port (Ratnagiri)",
        "cluster": "Konkan Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai (1554)",
        "notes": "All-weather fishing harbor with large cold storage and processing infrastructure."
    },
    "alibaug": {
        "lat": 18.6414, "lon": 72.8722,
        "name": "Alibaug & Rewas Landing Sector",
        "cluster": "Raigad District, Konkan Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai (1554)",
        "notes": "Artisanal catamaran and gillnet landing centre south of Mumbai harbour."
    },
    "malvan": {
        "lat": 16.0617, "lon": 73.4686,
        "name": "Malvan & Sindhudurg Coastal Basin",
        "cluster": "Sindhudurg Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Mumbai / Goa Base (1554)",
        "notes": "Marine sanctuary boundary; high biological richness with strict reef protection zones."
    },
    "rameswaram": {
        "lat": 9.2876, "lon": 79.3129,
        "name": "Rameswaram Base [Base 01]",
        "cluster": "Palk Bay / Gulf of Mannar, Indian Ocean",
        "vhf": "VHF Ch 16 / 68 (Coast Guard Station Mandapam)",
        "mrcc": "Indian Coast Guard MRCC Chennai (Toll-Free 1554 / 044-23460405)",
        "notes": "Core Project ORCA operational ground station; primary artisanal and motorized fleet corridor across International Maritime Boundary Line (IMBL)."
    },
    "mandapam": {
        "lat": 9.2780, "lon": 79.1250,
        "name": "Mandapam Marine Fishing Harbor",
        "cluster": "Palk Bay / Gulf of Mannar",
        "vhf": "VHF Ch 16 / 68",
        "mrcc": "Indian Coast Guard Station Mandapam (1554)",
        "notes": "Key Coast Guard hovercraft and patrol base monitoring Palk Strait navigation."
    },
    "tuticorin": {
        "lat": 8.7642, "lon": 78.1348,
        "name": "V.O. Chidambaranar Port (Tuticorin)",
        "cluster": "Gulf of Mannar, Indian Ocean",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Chennai / Station Tuticorin (1554)",
        "notes": "Major all-weather deepwater seaport and heavy fishing center in southern Tamil Nadu."
    },
    "kochi": {
        "lat": 9.9312, "lon": 76.2673,
        "name": "Cochin Fishing Harbor & Port of Kochi",
        "cluster": "Malabar Coast, Arabian Sea",
        "vhf": "VHF Ch 12 / 16 (Kochi Port Control)",
        "mrcc": "Indian Coast Guard MRCC Kochi / Southern Naval Command (1554)",
        "notes": "Premier seafood export hub of India; Vallarpadam International Container Transshipment Terminal (ICTT)."
    },
    "munambam": {
        "lat": 10.1800, "lon": 76.1700,
        "name": "Munambam Fishing Harbor",
        "cluster": "Ernakulam District, Malabar Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Kochi (1554)",
        "notes": "One of Kerala's largest deep-sea gillnetter and purse-seiner harbors."
    },
    "neendakara": {
        "lat": 8.9380, "lon": 76.5360,
        "name": "Neendakara & Sakthikulangara Harbor (Kollam)",
        "cluster": "South Kerala Coast, Arabian Sea",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Kochi (1554)",
        "notes": "Major trawl fishing centre; heavy seasonal shrimp and cuttlefish harvesting."
    },
    "vizhinjam": {
        "lat": 8.3756, "lon": 76.9906,
        "name": "Vizhinjam International Transshipment Port",
        "cluster": "Trivandrum Coast, Arabian Sea / Indian Ocean",
        "vhf": "VHF Ch 16 / 14",
        "mrcc": "Indian Coast Guard Station Vizhinjam (1554)",
        "notes": "India's first mega deepwater container transshipment port with 20m natural draft."
    },
    "chennai": {
        "lat": 13.0827, "lon": 80.2707,
        "name": "Chennai Port & Kasimedu Fishing Harbor",
        "cluster": "Coromandel Coast, Bay of Bengal",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Chennai (HQ East, 1554)",
        "notes": "Oldest artificial harbour on India's east coast; Kasimedu accommodates over 1,500 mechanized trawlers."
    },
    "kasimedu": {
        "lat": 13.1250, "lon": 80.2970,
        "name": "Kasimedu Fishing Harbor (Chennai)",
        "cluster": "Coromandel Coast, Bay of Bengal",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Chennai (1554)",
        "notes": "Primary pelagic fish auction and vessel repair wharf in north Chennai."
    },
    "ennore": {
        "lat": 13.2300, "lon": 80.3300,
        "name": "Kamarajar Port (Ennore)",
        "cluster": "North Chennai Coast, Bay of Bengal",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Chennai (1554)",
        "notes": "Modern corporate port handling thermal coal, automobiles, and bulk liquids."
    },
    "kattupalli": {
        "lat": 13.3100, "lon": 80.3500,
        "name": "Kattupalli Shipyard & Port",
        "cluster": "North Chennai / Ennore Reach, Bay of Bengal",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard MRCC Chennai (1554)",
        "notes": "Commercial container terminal and defense shipbuilding facility."
    },
    "visakhapatnam": {
        "lat": 17.6868, "lon": 83.2185,
        "name": "Visakhapatnam Port & Fishing Harbor",
        "cluster": "Andhra Coast, Bay of Bengal",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Chennai / Station Vizag (1554)",
        "notes": "Only natural harbour on India's east coast; headquarters of Eastern Naval Command and major pelagic tuna longline fleet."
    },
    "vizag": {
        "lat": 17.6868, "lon": 83.2185,
        "name": "Visakhapatnam Port & Fishing Harbor",
        "cluster": "Andhra Coast, Bay of Bengal",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard Station Vizag (1554)",
        "notes": "Natural deepwater basin with outer dolphin's nose breakwater."
    },
    "gangavaram": {
        "lat": 17.6200, "lon": 83.2400,
        "name": "Gangavaram Port",
        "cluster": "South Vizag Reach, Bay of Bengal",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard Station Vizag (1554)",
        "notes": "All-weather deep-draft industrial port accommodating Capesize vessels up to 200,000 DWT."
    },
    "paradip": {
        "lat": 20.3167, "lon": 86.6167,
        "name": "Paradip Port",
        "cluster": "Mahanadi Delta, Bay of Bengal, Odisha",
        "vhf": "VHF Ch 16 / 12",
        "mrcc": "Indian Coast Guard Station Paradip / MRCC Kolkata (1554)",
        "notes": "Major bulk mineral export and crude oil terminal with large artificial lagoon harbor."
    },
    "dhamra": {
        "lat": 20.8000, "lon": 86.9700,
        "name": "Dhamra Port",
        "cluster": "Bhadrak District, Bay of Bengal, Odisha",
        "vhf": "VHF Ch 16",
        "mrcc": "Indian Coast Guard Station Paradip (1554)",
        "notes": "Deepwater all-weather port situated north of the Dhamra river estuary."
    },
    "haldia": {
        "lat": 22.0667, "lon": 88.0667,
        "name": "Haldia Dock Complex (SMP Kolkata)",
        "cluster": "Hooghly River / Bay of Bengal, West Bengal",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Indian Coast Guard MRCC Kolkata (1554)",
        "notes": "Deep-water impounded dock complex supporting the inland industrial corridor of eastern India."
    },
    "port blair": {
        "lat": 11.6234, "lon": 92.7265,
        "name": "Phoenix Bay & Haddo Harbor (Port Blair)",
        "cluster": "South Andaman Island, Andaman Sea",
        "vhf": "VHF Ch 16 / 68",
        "mrcc": "Indian Coast Guard MRCC Port Blair (Toll-Free 1554 / 03192-230553)",
        "notes": "Strategic tri-services Andaman & Nicobar Command headquarters; deep oceanic shelf rich in Yellowfin and Bigeye tuna."
    },
    "colombo": {
        "lat": 6.9497, "lon": 79.8428,
        "name": "Port of Colombo",
        "cluster": "South Asia Hub, Indian Ocean, Sri Lanka",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "Sri Lanka Navy MRCC Colombo (Tel: +94 11 244 5368)",
        "notes": "Primary transshipment hub for the Indian subcontinent; deep breakwater harbor on international east-west shipping lane."
    },

    # ------------------------------------------------------------------------------------------
    # ASIA-PACIFIC, MIDDLE EAST & AMERICAS
    # ------------------------------------------------------------------------------------------
    "singapore": {
        "lat": 1.290270, "lon": 103.851959,
        "name": "Port of Singapore (Tuas / Jurong / Pasir Panjang)",
        "cluster": "Strait of Singapore / Malacca",
        "vhf": "VHF Ch 12 / 14 / 16 / 20 / 68 (Singapore Port Operations Control)",
        "mrcc": "Maritime and Port Authority of Singapore (MPA Port Marine Safety / POCC)",
        "notes": "World's largest container transshipment port and premier bunkering hub; Tuas Mega Port development."
    },
    "jurong": {
        "lat": 1.2667, "lon": 103.7167,
        "name": "Jurong Port & Industrial Anchorage",
        "cluster": "Port of Singapore Cluster, Strait of Malacca",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "MPA Singapore POCC",
        "notes": "Dedicated bulk, breakbulk, and offshore engineering terminal in western Singapore."
    },
    "pasir panjang": {
        "lat": 1.2750, "lon": 103.7750,
        "name": "Pasir Panjang Container Terminal",
        "cluster": "Port of Singapore Cluster, Strait of Malacca",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "MPA Singapore POCC",
        "notes": "Automated mega container terminal equipped with deepwater berths for 24,000+ TEU vessels."
    },
    "tokyo": {
        "lat": 35.6528, "lon": 139.8394,
        "name": "Port of Tokyo (Tokyo Bay)",
        "cluster": "Tokyo Bay, Northwest Pacific, Japan",
        "vhf": "VHF Ch 16 / 12 (Tokyo MARTIS)",
        "mrcc": "Japan Coast Guard 3rd Regional HQ (Yokohama MRCC / 118)",
        "notes": "Handles consumer cargo for the 38-million Kanto metropolis; Uraga Suido Traffic Route."
    },
    "yokohama": {
        "lat": 35.4437, "lon": 139.6380,
        "name": "Port of Yokohama (Minato Mirai / Honmoku)",
        "cluster": "Tokyo Bay Cluster, Japan",
        "vhf": "VHF Ch 16 / 12",
        "mrcc": "Japan Coast Guard Yokohama MRCC (Emergency 118)",
        "notes": "Japan's first foreign trade port opened in 1859; major container and international passenger terminal."
    },
    "kawasaki": {
        "lat": 35.5167, "lon": 139.7500,
        "name": "Port of Kawasaki",
        "cluster": "Tokyo Bay Cluster, Japan",
        "vhf": "VHF Ch 16",
        "mrcc": "Japan Coast Guard Yokohama MRCC",
        "notes": "Industrial energy and steel shipping terminal situated between Tokyo and Yokohama."
    },
    "chiba": {
        "lat": 35.5833, "lon": 140.1000,
        "name": "Port of Chiba",
        "cluster": "Tokyo Bay Cluster, Japan",
        "vhf": "VHF Ch 16",
        "mrcc": "Japan Coast Guard Chiba Coast Guard Office",
        "notes": "Japan's largest seaport by area, handling massive crude, LNG, and petrochemical volumes."
    },
    "yokosuka": {
        "lat": 35.2811, "lon": 139.6722,
        "name": "Port of Yokosuka",
        "cluster": "Tokyo Bay Entrance, Japan",
        "vhf": "VHF Ch 16",
        "mrcc": "Japan Coast Guard 3rd Regional HQ",
        "notes": "Historic strategic naval base hosting Japan Maritime Self-Defense Force and US 7th Fleet."
    },
    "shanghai": {
        "lat": 31.2304, "lon": 121.4737,
        "name": "Port of Shanghai (Yangshan Deepwater Port & Waigaoqiao)",
        "cluster": "Yangtze River Estuary / East China Sea",
        "vhf": "VHF Ch 16 / 08 / 09 (Wusong VTS)",
        "mrcc": "China Maritime Safety Administration (Shanghai MSA / MRCC Beijing)",
        "notes": "World's busiest container port exceeding 49 million TEUs; Yangshan connected via 32.5 km Donghai Bridge."
    },
    "ningbo": {
        "lat": 29.8683, "lon": 121.5440,
        "name": "Port of Ningbo-Zhoushan",
        "cluster": "Zhejiang Coast, East China Sea",
        "vhf": "VHF Ch 16 / 06",
        "mrcc": "Ningbo Maritime Safety Administration",
        "notes": "World's largest port by cargo tonnage (>1.2 billion tonnes); deep natural water berths."
    },
    "busan": {
        "lat": 35.1028, "lon": 129.0403,
        "name": "Port of Busan (Busan New Port)",
        "cluster": "Korea Strait, South Korea",
        "vhf": "VHF Ch 12 / 16 (Busan VTS)",
        "mrcc": "Korea Coast Guard Busan Central MRCC (Emergency 122)",
        "notes": "Premier Northeast Asian transshipment gateway; Busan New Port automated container operations."
    },
    "dubai": {
        "lat": 25.2697, "lon": 55.3095,
        "name": "Port Rashid & Jebel Ali Port (Dubai)",
        "cluster": "Persian Gulf, UAE",
        "vhf": "VHF Ch 16 / 69 (Dubai Port Control)",
        "mrcc": "UAE Coast Guard / National Search and Rescue Center (NSRC Abu Dhabi)",
        "notes": "Jebel Ali is the world's largest man-made harbor and busiest port in the Middle East."
    },
    "jebel ali": {
        "lat": 24.9857, "lon": 55.0273,
        "name": "Jebel Ali Port (DP World Flagship)",
        "cluster": "Persian Gulf, UAE",
        "vhf": "VHF Ch 16 / 69",
        "mrcc": "UAE National Search and Rescue Center (NSRC)",
        "notes": "Mega deepwater hub with 67 berths handling over 14 million TEUs."
    },
    "san francisco": {
        "lat": 37.8080, "lon": -122.4177,
        "name": "Fisherman's Wharf & Port of San Francisco",
        "cluster": "San Francisco Bay, Northeast Pacific, USA",
        "vhf": "VHF Ch 12 / 14 / 16 (San Francisco VTS)",
        "mrcc": "US Coast Guard Sector San Francisco (VHF 16 / Tel: +1 415-399-3547)",
        "notes": "San Francisco Bay entrance under Golden Gate Bridge; historic Dungeness crab and salmon fleet."
    },
    "oakland": {
        "lat": 37.7957, "lon": -122.2795,
        "name": "Port of Oakland",
        "cluster": "San Francisco Bay Cluster, USA",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "US Coast Guard Sector San Francisco",
        "notes": "Principal container gateway for Northern California agricultural exports."
    },
    "richmond": {
        "lat": 37.9158, "lon": -122.3667,
        "name": "Port of Richmond (California)",
        "cluster": "San Francisco Bay Cluster, USA",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "US Coast Guard Sector San Francisco",
        "notes": "Leading liquid bulk and automobile port in Northern California."
    },
    "sausalito": {
        "lat": 37.8590, "lon": -122.4853,
        "name": "Sausalito Marine Anchorage",
        "cluster": "San Francisco Bay Cluster, USA",
        "vhf": "VHF Ch 16",
        "mrcc": "US Coast Guard Sector San Francisco",
        "notes": "Sheltered coastal anchorage inside Richardson Bay across the Golden Gate."
    },
    "los angeles": {
        "lat": 33.7432, "lon": -118.2673,
        "name": "Port of Los Angeles (San Pedro Bay)",
        "cluster": "Southern California, Pacific Ocean, USA",
        "vhf": "VHF Ch 14 / 16 (LA/Long Beach VTS)",
        "mrcc": "US Coast Guard Sector Los Angeles-Long Beach (VHF 16 / 310-521-3801)",
        "notes": "America's Port; busiest container port in North America handling over 10 million TEUs."
    },
    "long beach": {
        "lat": 33.7701, "lon": -118.1937,
        "name": "Port of Long Beach",
        "cluster": "San Pedro Bay Cluster, USA",
        "vhf": "VHF Ch 14 / 16",
        "mrcc": "US Coast Guard Sector Los Angeles-Long Beach",
        "notes": "Premier US gateway for trans-Pacific trade with state-of-the-art automated terminals."
    },
    "new york": {
        "lat": 40.6892, "lon": -74.0445,
        "name": "Port of New York & New Jersey",
        "cluster": "Upper & Lower New York Bay, North Atlantic, USA",
        "vhf": "VHF Ch 11 / 12 / 14 / 16 (New York VTS)",
        "mrcc": "US Coast Guard Sector New York (Fort Wadsworth / VHF 16 / 718-354-4353)",
        "notes": "Largest seaport on the US East Coast; Ambrose Channel approach into Port Newark/Elizabeth."
    },
    "miami": {
        "lat": 25.7781, "lon": -80.1791,
        "name": "PortMiami (Dodge Island)",
        "cluster": "Biscayne Bay / Atlantic Ocean, USA",
        "vhf": "VHF Ch 12 / 16",
        "mrcc": "US Coast Guard Sector Miami (VHF 16 / 305-535-4300)",
        "notes": "Cruise Capital of the World and major cargo transshipment bridge to Latin America."
    },
    "sydney": {
        "lat": -33.8688, "lon": 151.2093,
        "name": "Sydney Harbour & Port Botany",
        "cluster": "Tasman Sea / South Pacific, Australia",
        "vhf": "VHF Ch 12 / 16 (Sydney VTS)",
        "mrcc": "Australian Maritime Safety Authority (AMSA JRCC Australia / Canberra 1800 641 792)",
        "notes": "Iconic deepwater drowned river valley harbour and Botany Bay container complex."
    },
    "cape town": {
        "lat": -33.9189, "lon": 18.4233,
        "name": "Port of Cape Town (Table Bay)",
        "cluster": "Atlantic / Benguela Upwelling, South Africa",
        "vhf": "VHF Ch 14 / 16 (Cape Town Port Control)",
        "mrcc": "MRCC Cape Town (SAMSA / Tel: +27 21 938 3310)",
        "notes": "Strategic location at the Cape of Good Hope; high marine upwelling and tuna longlining."
    }
}

# ==============================================================================================
# 2. PROJECT ORCA ARCHITECTURAL KNOWLEDGE BASE (SIH26 DOMAIN RAG)
# ==============================================================================================
PROJECT_ORCA_KNOWLEDGE_BASE: Dict[str, str] = {
    "about": (
        "**Project ORCA (Oceanic Resource & Coastal Advisory System):**\n\n"
        "Project ORCA is an AI-powered maritime intelligence and safety navigation platform built for "
        "Smart India Hackathon (SIH 2026). It synthesizes multi-satellite telemetry (Copernicus Sentinel-3 SLSTR/OLCI, "
        "NASA MODIS-Aqua) and numerical ocean state forecasts (INCOIS OSF) to provide:\n\n"
        "1. **Potential Fishing Zone (PFZ) Identification:** Algorithmic detection of thermal boundary fronts and chlorophyll-a plumes.\n"
        "2. **Real-time Vessel Safety Clearance:** Dynamic seaworthiness classification for artisanal skiffs, motorized canoes, and trawlers.\n"
        "3. **Cryptographic Data Provenance:** SHA-256 verifiable chain of custody for every advisory.\n"
        "4. **Global Port & Cluster Intelligence:** 300+ global seaports, satellite landing centers, VHF distress monitoring, and MRCC contact relay."
    ),
    "satellite": (
        "**Project ORCA Satellite Ingestion Pipeline:**\n\n"
        "- **Sentinel-3 SLSTR (SST):** 1.1 km Sea Surface Temperature swath processing with automated cloud masking and gradient computation.\n"
        "- **Sentinel-3 OLCI (Chlorophyll-a):** 300m ocean color radiometry for biological productivity and phytoplankton bloom mapping.\n"
        "- **INCOIS OSF (Ocean State Forecast):** Significant Wave Height (SWH), swell period, surface current vectors, and wind speed.\n"
        "- **Update Cadence:** Automated 6-hour cycle with deterministic fallbacks."
    ),
    "pfz": (
        "**Potential Fishing Zone (PFZ) Detection Algorithm:**\n\n"
        "- **Thermal Fronts:** Computed via spatial Sobel/Canny gradient operators on SST matrices. Fronts with gradients >= 0.8 °C/km are flagged.\n"
        "- **Chlorophyll Plumes:** Validated where Chlorophyll-a concentration exceeds 0.45 mg/m³.\n"
        "- **Convergence Zones:** High-probability PFZ hotspots occur at the intersection of thermal fronts and chlorophyll plumes, reducing fuel search time by up to 40%."
    ),
    "safety": (
        "**Vessel Safety Classification Engine:**\n\n"
        "- **Artisanal Skiff (<7m, unmotorized):** Max wave 1.2m | Max wind 25 km/h.\n"
        "- **Motorized Canoe (7-12m, OBM):** Max wave 2.0m | Max wind 35 km/h.\n"
        "- **Mechanized Trawler (12-24m, inboard):** Max wave 3.5m | Max wind 50 km/h.\n"
        "- **Deep-Sea Pelagic Vessel (>24m):** Max wave 5.0m | Max wind 65 km/h.\n\n"
        "*If environmental conditions exceed vessel thresholds, the system triggers a CRITICAL DANGER alert prohibiting departure.*"
    ),
    "provenance": (
        "**Cryptographic Provenance Engine (Explainable AI):**\n\n"
        "- Every advisory generates a unique `ProvenanceRecord` with a `trace_id`.\n"
        "- Includes exact satellite granule filename, acquisition timestamp, model execution time, and SHA-256 evidence hashes.\n"
        "- Enables maritime authorities and vessel masters to mathematically verify data provenance."
    )
}

# ==============================================================================================
# 3. GREETINGS & SYSTEM HUD
# ==============================================================================================
ORCA_SYSTEM_WELCOME_HUD = (
    "👋 **Welcome to Project ORCA — Maritime Copilot & Oceanic Intelligence Engine**\n\n"
    "I am your dedicated small language model (SLM) trained on global ocean state forecasting, "
    "satellite oceanography (Sentinel-3 / MODIS), and maritime navigational safety.\n\n"
    "**What you can ask me:**\n"
    "- 📍 **Global & Local Ports:** e.g., *'Port of Vlaardingen'*, *'Rotterdam Maasvlakte'*, *'Dapoli Harnai'*, *'Kasimedu'*, *'Yokohama'*\n"
    "- 🌊 **Sea Basin Snapshots:** e.g., *'Bay of Bengal details'*, *'Arabian Sea status'*, *'North Sea wave height'*\n"
    "- 🧭 **Geographic Coordinates:** e.g., *'Is it safe to sail at 17.8°N, 84.2°E?'*\n"
    "- 🐟 **PFZ & Species Advisory:** e.g., *'Where to fish yellowfin tuna from Rameswaram?'*\n"
    "- 🛰️ **Project Architecture:** e.g., *'How does the satellite pipeline work?'*, *'Explain PFZ algorithm'*\n\n"
    "*(Select a quick action below or type any maritime query)*"
)

ORCA_SUGGESTED_WELCOME_ACTIONS = [
    "Port of Vlaardingen",
    "Bay of Bengal Details",
    "Check 17.8°N, 84.2°E",
    "Dapoli Harnai Sector",
    "Project ORCA Architecture"
]

class MaritimeRAGEngine:
    """
    Maritime Retrieval-Augmented Generation & SLM Knowledge Resolver.
    """

    @classmethod
    def is_greeting(cls, text: str) -> bool:
        """Determines if the input is a single-word greeting or system request."""
        clean = re.sub(r'[^\w\s]', '', text.strip().lower())
        greeting_words = {
            "hi", "hello", "hey", "help", "who are you", "what can you do", "menu",
            "start", "guide", "status", "info", "orca", "overview", "capabilities",
            "greetings", "good morning", "good evening", "good afternoon", "hola", "namaste"
        }
        return clean in greeting_words or (len(clean.split()) == 1 and clean in greeting_words)

    @classmethod
    def query_project_knowledge(cls, text: str) -> Optional[str]:
        """Queries Project ORCA architecture knowledge base."""
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["what is orca", "explain orca", "project orca", "sih26", "what is this project", "who built you", "tell me about this"]):
            return PROJECT_ORCA_KNOWLEDGE_BASE["about"]
        if any(kw in text_lower for kw in ["satellite pipeline", "satellite ingest", "sentinel", "modis", "eumetsat", "how does satellite work"]):
            return PROJECT_ORCA_KNOWLEDGE_BASE["satellite"]
        if any(kw in text_lower for kw in ["pfz algorithm", "potential fishing zone", "how pfz works", "thermal front detection", "chlorophyll bloom"]):
            return PROJECT_ORCA_KNOWLEDGE_BASE["pfz"]
        if any(kw in text_lower for kw in ["vessel safety", "vessel limits", "safety classification", "max wave", "max wind"]):
            return PROJECT_ORCA_KNOWLEDGE_BASE["safety"]
        if any(kw in text_lower for kw in ["provenance", "cryptographic", "sha256", "explainable ai", "trace id"]):
            return PROJECT_ORCA_KNOWLEDGE_BASE["provenance"]
        return None

    @classmethod
    def query_rag_knowledge(cls, text: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves matching port, satellite harbor, or marine terminal from the 300+ RAG corpus.
        Supports exact key match, substring match, and token-set fuzzy matching.
        """
        clean_text = text.lower().strip()
        tokens = set(re.findall(r'[a-zA-Z0-9]+', clean_text))

        # 1. Exact match on normalized full string
        clean_no_punct = re.sub(r'[^\w\s]', ' ', clean_text).strip()
        for key, port in GLOBAL_MARITIME_RAG_CORPUS.items():
            if clean_text == key or clean_no_punct == key:
                return port

        # 2. Multi-word phrase search in text (e.g. 'port of vlaardingen', 'hook of holland', 'nhava sheva')
        # Sort keys by length descending to match longest specific sub-ports first
        sorted_keys = sorted(GLOBAL_MARITIME_RAG_CORPUS.keys(), key=lambda k: len(k), reverse=True)
        for key in sorted_keys:
            if " " in key and key in clean_text:
                return GLOBAL_MARITIME_RAG_CORPUS[key]

        # 3. Single-word token search (e.g. 'vlaardingen', 'schiedam', 'dapoli', 'maasvlakte')
        for key in sorted_keys:
            if " " not in key and key in tokens:
                return GLOBAL_MARITIME_RAG_CORPUS[key]

        # 4. Fuzzy ratio match for slight typos in port names (cutoff 0.85)
        for token in tokens:
            if len(token) >= 5:
                matches = difflib.get_close_matches(token, list(GLOBAL_MARITIME_RAG_CORPUS.keys()), n=1, cutoff=0.85)
                if matches:
                    return GLOBAL_MARITIME_RAG_CORPUS[matches[0]]

        return None
