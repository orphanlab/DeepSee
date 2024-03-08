print("STARTING:...")

import logging
import math
import os
from io import StringIO


#
# Data processing packages
#
import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import swifter


#
# Web app packages
#
from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve


#
# Discrete Sibson (Natural Neighbor) Interpolation in 3D.
# See: https://github.com/innolitics/natural-neighbor-interpolation
#
try:
    from naturalneighbor import griddata as nngd
except ImportError:
    print("WARNING:Cannot import `naturalneighbor` library.")
    print("> `naturalneighbor` library can only be installed on a Windows OS.")
    print("> The frontend should not send a request for `Natural Neighbor` interpolations when the user is not using a Windows OS.")


#
# Nearest and Linear Interpolation over unstructured D-D data.
# See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
#
from scipy.interpolate import griddata as spgd


# Start logging
logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)


# Create Flask app
app = Flask(__name__)
CORS(app)


# determine if application is a script file or frozen exe
# if getattr(sys, "frozen", False):
#     application_path = os.path.dirname(sys.executable)
# else:
#     application_path = os.path.dirname(__file__)


def get_haversine_dist(lat1, lon1, lat2, lon2):
    """Haversine formula. Generally used geo measurement function.

    See: https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
    """
    R = 6378.137  # Radius of earth in kilometers
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180
    ) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # kilometers
    return d * 100000  # centimeters


def point_from_initial_and_dist(lat1, lon1, dx, dy):
    """Get a final lat/lon from an initial lat/lon and distance from initial lat/lon dx and dy in centimeters.

    See: https://www.movable-type.co.uk/scripts/latlong.html
    """
    # Return initial lat/lon if calculating the origin
    if dx <= 0 and dy <= 0:
        return [lon1, lat1]

    # get bearing in radians from positive y (north) => avoid divide by zero error
    if dx <= 0:
        bearing = 0
    elif dy <= 0:
        bearing = math.pi / 2
    else:
        bearing = (math.pi / 2) - math.atan(dy / dx)

    d = math.sqrt(((dx / 100) ** 2) + ((dy / 100) ** 2))  # straight-line distance
    R = 6378.137 * 1000  # Earth's radius, in metres
    ang_dist = d / R  # angular distance travelled

    phi1 = (lat1 * math.pi) / 180  # phi, lambda in radians
    lambda1 = (lon1 * math.pi) / 180
    phi2 = math.asin(math.sin(phi1) * math.cos(ang_dist) + math.cos(phi1) * math.sin(ang_dist) * math.cos(bearing))
    lambda2 = lambda1 + math.atan2(
        math.sin(bearing) * math.sin(ang_dist) * math.cos(phi1), math.cos(ang_dist) - math.sin(phi1) * math.sin(phi2)
    )
    lat2 = (phi2 * 180) / math.pi
    lon2 = (lambda2 * 180) / math.pi
    lon2 = ((lon2 + 540) % 360) - 180  # normalize lon2 to [-180, +180]

    return [lon2, lat2]  # degrees


def interp(cruise_data_string, method, resolution, color_mode, cylinders, variables, category):
    """Interpolate values."""
    df = pd.read_csv(StringIO(cruise_data_string))

    # filter dataframe for only relevant cylinders
    if cylinders:
        df = df[df["Cylinder"].isin(cylinders)]

    # cannot find cylinders requested => don't interpolate
    if len(df.index) == 0:
        return jsonify([])

    # keep only relevant columns
    meta = [
        "Sample_Name",
        "Cylinder",
        "Latitude",
        "Longitude",
        "Horizon",
        "start_depth",
        "sum_abundance",
    ]
    df = df[df.columns.intersection(meta + variables)].reset_index().drop(columns=["index"])

    #
    # normalize coordinates to relative cm
    #
    #  1. get haversine distance in cm from min lat/lon to point along straight lines
    #
    #            (cm)
    #    lon_min ---> lon
    #  |----------------x lat
    #  |                |  ^
    #  |                |  | (cm)
    #  |                |  |
    #  |                | lat_min
    #  o-----------------
    #
    #  2. round it to the nearest resolution cm
    #
    lon_min = df["Longitude"].min()
    lat_min = df["Latitude"].min()
    df[["Longitude_rel_cm", "Latitude_rel_cm"]] = df[["Longitude", "Latitude"]].apply(
        lambda x: [
            resolution
            * round(float(get_haversine_dist(x["Latitude"], lon_min, x["Latitude"], x["Longitude"])) / resolution),
            resolution
            * round(float(get_haversine_dist(lat_min, x["Longitude"], x["Latitude"], x["Longitude"])) / resolution),
        ],
        axis=1,
        result_type="expand",
    )
    meta += ["Longitude_rel_cm", "Latitude_rel_cm"]

    # transform the taxa counts to relative abundance
    if category == "Taxa":
        for var in variables:
            df[var] /= df["sum_abundance"]

    # get the input x,y,z coords
    x = df["Longitude_rel_cm"]
    y = df["Latitude_rel_cm"]
    z = df["start_depth"]

    # this should give the correct axis sizes and interval (since x,y,z are in cm already)
    xi, yi, zi = np.ogrid[
        min(x) : max(x) + resolution : resolution, min(y) : max(y) + resolution : resolution, min(z) : max(z) + 1 : 1
    ]

    # create the output grid X,Y,Z
    X1 = xi.reshape(
        xi.shape[0],
    )
    Y1 = yi.reshape(
        yi.shape[1],
    )
    Z1 = zi.reshape(
        zi.shape[2],
    )
    ar_len = len(X1) * len(Y1) * len(Z1)
    X = np.arange(ar_len, dtype=float)
    Y = np.arange(ar_len, dtype=float)
    Z = np.arange(ar_len, dtype=float)
    l = 0
    for i in range(0, len(X1)):
        for j in range(0, len(Y1)):
            for k in range(0, len(Z1)):
                X[l] = X1[i]
                Y[l] = Y1[j]
                Z[l] = Z1[k]
                l = l + 1

    # helper for natural neighbors output
    grid_ranges = [
        [min(x), max(x) + resolution, resolution],
        [min(y), max(y) + resolution, resolution],
        [min(z), max(z) + 1, 1],
    ]

    # get interpolated values
    xyz_og_values = []
    var_og_values = []
    var_interp_values = []
    for var in variables:
        # have to drop nans or griddata fails
        df_temp = df[meta + [var]].dropna().reset_index().drop(columns=["index"])
        if len(df_temp.index) == 0:
            # no data
            xyz_og_values.append((pd.Series(dtype=object), pd.Series(dtype=object), pd.Series(dtype=object)))
            var_og_values.append(pd.Series(dtype=object))
            var_interp_values.append(np.full((ar_len,), np.nan, dtype=float))  # same shape as X, Y, Z
        else:
            # get x,y,z
            x = df_temp["Longitude_rel_cm"]
            y = df_temp["Latitude_rel_cm"]
            z = df_temp["start_depth"]
            xyz_og_values.append((x, y, z))
            # get v
            v = df_temp[var]
            var_og_values.append(v)
            try:
                # interpolate!
                if method == "Linear":
                    V = spgd((x, y, z), v, (X, Y, Z), method="linear")
                elif method == "Natural":
                    V = nngd(np.stack([x, y, z], axis=1), v, grid_ranges)
            except Exception:
                # interpolation failed, return NaNs
                V = np.full((ar_len,), np.nan, dtype=float)
            finally:
                # store results
                var_interp_values.append(V.flatten())

    # build the final 3D dataset, joining observed metadata with gridded data
    df_3d = pd.DataFrame(X.astype(int), columns=["Longitude_rel_cm"])
    df_3d["Latitude_rel_cm"] = pd.DataFrame(Y.astype(int))
    df_3d["start_depth"] = pd.DataFrame(Z.astype(int))
    i = 0
    for var in variables:
        df_3d[var] = pd.DataFrame(var_interp_values[i])
        i += 1
        
    df_og = df[meta]
    df_og = df_og.assign(observed=lambda x: 1)
    
    df_final = df_3d.merge(df_og, how="left", on=["Longitude_rel_cm", "Latitude_rel_cm", "start_depth"])
    
    df_final["observed"] = df_final["observed"].fillna(0).astype(int)

    #
    # get calculated lat/lon in degrees from relative cm from min lat/lon
    #          0deg
    #  dy (cm) |  bearing     o <- lat/lon calc
    #          |  /  \     /
    #          |        /    d = sqrt(dx^2 + dy^2)
    #          |     /
    #          |  /    ) theta = arctan(dy/dx)
    #  lat_min o--------------- 90deg
    #       lon_min          dx (cm)
    #
    if (df_final.shape[0] < 250000):
        df_final[["Longitude_calc", "Latitude_calc"]] = df_final[["Longitude_rel_cm", "Latitude_rel_cm"]].apply(
            lambda x: point_from_initial_and_dist(
                lat_min,
                lon_min,
                x["Longitude_rel_cm"],  # dx
                x["Latitude_rel_cm"],  # dy
            ),
            axis=1,
            result_type="expand",
        )
    else:
        df_final[["Longitude_calc", "Latitude_calc"]] = df_final[["Longitude_rel_cm", "Latitude_rel_cm"]].swifter.set_npartitions(30).apply(
            lambda x: point_from_initial_and_dist(
                lat_min,
                lon_min,
                x["Longitude_rel_cm"],  # dx
                x["Latitude_rel_cm"],  # dy
            ),
            axis=1,
            result_type="expand",
        )
        
    # build a tree using the observed points from earlier to find nearest neighbor of each point in the datase
    if color_mode == "Uncertainty":
        tree = KDTree(df[["Longitude_rel_cm", "Latitude_rel_cm", "start_depth"]])
        df_final[["dist_to_nearest", "idx_of_nearest"]] = pd.DataFrame(
            [
                tree.query([row[0], row[1], row[2]])
                for row in df_final[["Longitude_rel_cm", "Latitude_rel_cm", "start_depth"]].to_numpy()
            ],
            index=df_final.index,
        )
        df_final["xyz_of_nearest"] = pd.Series(
            [
                (df.iloc[idx]["Longitude_rel_cm"], df.iloc[idx]["Latitude_rel_cm"], df.iloc[idx]["start_depth"])
                for idx in df_final["idx_of_nearest"].to_numpy()
            ],
            index=df_final.index,
        )
        df_final = df_final.drop(columns=["idx_of_nearest"])

    # clean up column names
    df_final = df_final.rename(
        columns={
            "Longitude": "Longitude_real",
            "Latitude": "Latitude_real",
            "Longitude_rel_cm": "X",
            "Latitude_rel_cm": "Y",
            "start_depth": "Z",
        }
    )
    # get final output as valid json
    return df_final.to_json(orient="records")


@app.route("/", methods=["GET"])
def get_connected():
    return jsonify("Connected!")


@app.route("/getInterp", methods=["POST"])
def get_interp():
    data_in = request.json  # request is sent as JSON, which is converted to a dict

    cruise_data_string = data_in["cruise_data_string"]  # cruise data from file as string
    method = data_in["method"]  # 'Linear' or 'Natural' => determines interpolation method used
    resolution = data_in["resolution"]  # resolution to interpolate at in cm^2 (x,y)
    color_mode = data_in["color_mode"]  # 'Standard', 'Uncertainty' => determines whether NN-search is needed
    cylinders = data_in["cylinders"]  # filter data by cylinders
    variables = data_in["variables"]  # variables to interpolate
    category = data_in["category"]  # 'Geochemistry' or 'Taxa' => determines if variable needs adjusting before interp

    data_out = interp(
        cruise_data_string, method, resolution, color_mode, cylinders, variables, category
    )  # interpolate!

    return data_out  # send data to client


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 3000))
    serve(app, host=host, port=port)
