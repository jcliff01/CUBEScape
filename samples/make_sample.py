"""Writes made-up CUBE call records (syslog hourly files) to samples/cube1/, for trying CubeScope.
All numbers are 555-01xx style, addresses are documentation ranges. Run: python samples/make_sample.py"""
import datetime, os, random
random.seed(12)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cube1")
os.makedirs(out, exist_ok=True)
day = datetime.datetime(2026, 11, 17)
rx, ios = 4100000, 3200000
def clk(t): return t.strftime("%H:%M:%S.") + f"{t.microsecond // 1000:03d}"
def T(t): return clk(t) + " EST " + t.strftime("%a %b ") + str(t.day) + t.strftime(" %Y")
def H(t):
    global rx, ios
    rx += 1; ios += 1
    return f"{rx}: {ios}: Nov {t.day} {clk(t)} EST: "
def leg(guid, origin, setup, peer, cause, text, connect, disc, talk, oneway=False):
    pkts = int(talk * 50); bytes_ = pkts * 160
    tx, rxp = pkts, (0 if oneway else pkts)
    return (disc, H(disc) + f"%VOIPAAA-5-VOIP_CALL_HISTORY: CallLegType 2, ConnectionId {guid}, SetupTime {T(setup)}, "
            f"PeerAddress {peer}, PeerSubAddress , DisconnectCause {cause}  , DisconnectText {text}, ConnectTime {T(connect)}, "
            f"DisconnectTime {T(disc)}, CallOrigin {origin}, ChargedUnits 0, InfoType 2, TransmitPackets {tx}, "
            f"TransmitBytes {tx * 160}, ReceivePackets {rxp}, ReceiveBytes {rxp * 160}")
lines = []
t = day.replace(hour=8)
while t < day.replace(hour=17, minute=30):
    t += datetime.timedelta(seconds=random.randint(15, 140), milliseconds=random.randint(0, 999))
    guid = "%032X" % random.getrandbits(128)
    caller = f"612555{random.randint(100, 199):04d}"; callee = f"312555{random.randint(100, 199):04d}"
    ring = datetime.timedelta(seconds=random.randint(2, 20))
    r = random.random()
    if r < 0.70:      # answered
        talk = random.randint(20, 900); conn = t + ring; end = conn + datetime.timedelta(seconds=talk)
        oneway = random.random() < 0.04
        for origin, peer in ((2, caller), (1, callee)):
            lines.append(leg(guid, origin, t, peer, "10", "normal call clearing (16)", conn, end, talk, oneway))
    else:
        end = t + ring
        cause, text = random.choice([("11", "user busy (17)"), ("13", "no answer from user, user alerted (19)"),
                                     ("10", "normal call clearing (16)"), ("29", "temporary failure (41)")])
        for origin, peer in ((2, caller), (1, callee)):
            lines.append(leg(guid, origin, t, peer, cause, text, end, end, 0))
lines.sort()
files = {}
for when, text in lines:
    files.setdefault(when.strftime("cube1-%Y-%m-%d-%H.log"), []).append(text)
for name, rows in files.items():
    with open(os.path.join(out, name), "w", newline="\r\n") as f:
        f.write("\n".join(rows) + "\n")
print(f"{len(lines) // 2} calls in {len(files)} files under {out}")
