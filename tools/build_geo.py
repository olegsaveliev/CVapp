import json, math, base64, sys
from shapely.geometry import shape, Point, LineString, Polygon, MultiPolygon, box, mapping
from shapely.ops import linemerge, unary_union, polygonize
from shapely.prepared import prep
D = sys.argv[1]
LAT0, LON0, R = 50.4501, 30.5236, 6371000.0
la0, lo0 = math.radians(LAT0), math.radians(LON0)
def P(lon, lat):  # orthographic tangent plane at Kyiv, meters
    la, lo = math.radians(lat), math.radians(lon)
    return (R*math.cos(la)*math.sin(lo-lo0), R*(math.cos(la0)*math.sin(la) - math.sin(la0)*math.cos(la)*math.cos(lo-lo0)))
def gj(n): return json.load(open(f"{D}/{n}.geojson"))
out = {}

# ---- globe land mask (1 deg) + Ukraine cells
land = prep(unary_union([shape(f["geometry"]) for f in gj("ne_110m_land")["features"]]))
cty = gj("ne_50m_admin_0_countries")["features"]
ua = [shape(f["geometry"]) for f in cty if f["properties"]["ADM0_A3"] == "UKR"][0]
crimea_in = ua.contains(Point(34.1, 45.0))
print("crimea in UA polygon:", crimea_in)
if not crimea_in:
    ru = [shape(f["geometry"]) for f in cty if f["properties"]["ADM0_A3"] == "RUS"][0]
    ua = unary_union([ua, ru.intersection(box(32.3, 44.2, 36.62, 46.25))])
    print("crimea added:", ua.contains(Point(34.1, 45.0)))
uap = prep(ua)
bits = bytearray(360*180//8); uac = []
for r in range(180):
    lat = 89.5 - r
    for c in range(360):
        lon = -179.5 + c
        pt = Point(lon, lat)
        if uap.contains(pt): uac.append(r*360+c)
        if land.contains(pt) or uap.contains(pt):
            i = r*360+c; bits[i>>3] |= 1 << (i & 7)
out["land"] = base64.b64encode(bytes(bits)).decode()
# Ukraine at 0.5 deg for a denser highlight
uah = []
for r in range(360):
    lat = 89.75 - r*0.5
    if not 43 < lat < 53: continue
    for c in range(720):
        lon = -179.75 + c*0.5
        if 21 < lon < 41 and uap.contains(Point(lon, lat)): uah.append([round(lon,2), round(lat,2)])
out["uaDots"] = uah
print("land cells", sum(bin(b).count("1") for b in bits), "ua half-deg", len(uah))

def enc(coords, q):  # list of (x,y) meters -> delta-encoded ints at quantum q
    s, px, py = [], 0, 0
    for x, y in coords:
        ix, iy = round(x/q), round(y/q); s += [ix-px, iy-py]; px, py = ix, iy
    return s
def projline(g):
    return [P(x, y) for x, y in g.coords]
def lines_of(g):
    if g.is_empty: return []
    if g.geom_type == "LineString": return [g]
    if g.geom_type in ("MultiLineString", "GeometryCollection"): return [l for x in g.geoms for l in lines_of(x)]
    if g.geom_type == "LinearRing": return [LineString(g.coords)]
    return []

# ---- regional (km quantum): Ukraine outline, coast, Dnipro
regbox = box(14, 40, 48, 58)
reg = {}
uab = ua.boundary.simplify(0.03)
reg["ua"] = [enc(projline(l), 1000) for l in lines_of(uab)]
landr = unary_union([shape(f["geometry"]) for f in gj("ne_50m_land")["features"]]).intersection(regbox)
coast = landr.boundary.difference(regbox.boundary.buffer(0.01)).simplify(0.04)
reg["coast"] = [enc(projline(l), 1000) for l in lines_of(coast) if l.length > 0.2]
rv = [f for f in gj("ne_10m_rivers_lake_centerlines")["features"] if (f["properties"].get("name_en") or f["properties"].get("name") or "") in ("Dnieper", "Dnipro", "Dnepr", "Desna", "Pripyat", "Dniester", "Southern Bug")]
print("rivers:", sorted({(f["properties"].get("name_en") or f["properties"].get("name")) for f in rv}))
rl = unary_union([shape(f["geometry"]) for f in rv]).intersection(regbox).simplify(0.02)
reg["rivers"] = [enc(projline(l), 1000) for l in lines_of(rl)]
out["reg"] = reg

# ---- city (Overpass)
def osm(n): return json.load(open(f"{D}/osm{n}.json"))["elements"]
def wline(e): return LineString([(p["lon"], p["lat"]) for p in e["geometry"]])
def toM(g):  # shapely lon/lat geometry -> meters geometry
    from shapely.ops import transform
    return transform(lambda xs, ys, zs=None: tuple(zip(*[P(x, y) for x, y in zip(xs, ys)])), g)
cls = {"motorway": 0, "trunk": 0, "primary": 1, "secondary": 2}
roads = {0: [], 1: [], 2: []}
for e in osm(1):
    if e["type"] == "way" and "geometry" in e: roads[cls[e["tags"]["highway"]]].append(toM(wline(e)))
cityR = 13000
cityclip = Point(0, 0).buffer(cityR)
out["roads"] = []
for k in (0, 1, 2):
    m = linemerge(unary_union(roads[k])).intersection(cityclip).simplify(9 if k < 2 else 12)
    ls = [l for l in lines_of(m) if l.length > (40 if k < 2 else 120)]
    out["roads"].append([enc(l.coords, 2) for l in ls])
    print("roads", k, len(ls), sum(len(l.coords) for l in ls))

# water: ways that are closed + relation multipolygons
polys = []
for e in osm(2):
    if e["type"] == "way" and "geometry" in e and len(e["geometry"]) > 3:
        c = [(p["lon"], p["lat"]) for p in e["geometry"]]
        if c[0] == c[-1]: polys.append(Polygon(c))
    elif e["type"] == "relation":
        outer = [wline(m) for m in e["members"] if m["type"] == "way" and m.get("role") == "outer" and "geometry" in m]
        inner = [wline(m) for m in e["members"] if m["type"] == "way" and m.get("role") == "inner" and "geometry" in m]
        po = list(polygonize(linemerge(outer))) if outer else []
        pi = list(polygonize(linemerge(inner))) if inner else []
        if po:
            g = unary_union(po)
            if pi: g = g.difference(unary_union(pi))
            polys.append(g)
water = unary_union([p.buffer(0) for p in polys])
water = toM(water).intersection(Point(0, 0).buffer(cityR + 2000)).simplify(12)
wp = [g for g in (water.geoms if hasattr(water, "geoms") else [water]) if g.geom_type == "Polygon" and g.area > 40000]
out["water"] = [[enc(p.exterior.coords, 4)] + [enc(i.coords, 4) for i in p.interiors if Polygon(i).area > 20000] for p in wp]
print("water polys", len(wp), sum(len(p.exterior.coords) for p in wp))
# Dnipro label spot: largest polygon point closest to center latitude
big = max(wp, key=lambda p: p.area)
out["dniproLabel"] = [round(c) for c in big.intersection(LineString([(-20000, -2500), (20000, -2500)])).representative_point().coords[0]]

# street detail roads
sroads = []
for e in osm(4):
    if e["type"] == "way" and "geometry" in e and e["tags"]["highway"] != "footway":
        sroads.append(toM(wline(e)))
m = linemerge(unary_union(sroads)).intersection(Point(0, 0).buffer(1100)).simplify(2.5)
ls = [l for l in lines_of(m) if l.length > 15]
out["sroads"] = [enc(l.coords, 1) for l in ls]
print("street roads", len(ls), sum(len(l.coords) for l in ls))
# label for Khreshchatyk
kh = [toM(wline(e)) for e in osm(1) + osm(4) if e["type"] == "way" and "geometry" in e and e.get("tags", {}).get("name") in ("Хрещатик", "вулиця Хрещатик")]
if kh:
    km = unary_union(kh); c = km.interpolate(0.5, normalized=True) if km.geom_type == "LineString" else km.centroid
    out["khLabel"] = [round(c.x), round(c.y)]
print("khreshchatyk", out.get("khLabel"))

# buildings
bl = []
for e in osm(3):
    if e["type"] != "way" or "geometry" not in e or len(e["geometry"]) < 4: continue
    t = e.get("tags", {})
    if t.get("building") in ("roof", "construction"): continue
    h = None
    try: h = float(str(t.get("height", "")).replace("m", "").strip())
    except: pass
    if not h:
        try: h = float(t.get("building:levels")) * 3.3 + 2
        except: h = None
    if not h: h = 16
    p = toM(Polygon([(q["lon"], q["lat"]) for q in e["geometry"]])).buffer(0).simplify(1.2)
    if p.is_empty or p.geom_type != "Polygon" or p.area < 30: continue
    if p.centroid.distance(Point(0, 0)) > 650: continue
    bl.append([max(4, min(120, round(h)))] + enc(list(p.exterior.coords)[:-1], 1))
out["bld"] = bl
print("buildings", len(bl), sum((len(b)-1)//2 for b in bl))
s = json.dumps(out, separators=(",", ":"))
open(f"{D}/kyiv-geo.json", "w").write(s)
print("bytes", len(s), {k: len(json.dumps(v, separators=(",", ":"))) for k, v in out.items()})
