import struct
from io import BytesIO

import h5py
import numpy as np
from astropy.io import fits
from PIL import Image

import xarray as xr
import polars as pl
import dask.array as da


def gen_xarray_data():
    """
    Generate Xarray-based data (labeled multi-dimensional arrays).
    """
    arr = np.array([[1, 2], [3, 4]], dtype=np.uint16)
    return xr.DataArray(arr, dims=("x", "y"), coords={"x": [0, 1], "y": [0, 1]})

def gen_polars_data():
    """
    Generate Polars-based data (fast, Rust-backed DataFrame).
    """
    return pl.DataFrame({
        "uint16_column": pl.Series([10, 20], dtype=pl.UInt16),
        "float64_column": [1.5, 2.5],
    })

def gen_dask_data():
    """
    Generate Dask-based data (parallelized arrays).
    """
    np_arr = np.array([1, 2, 3, 4], dtype=np.uint16)
    dask_arr = da.from_array(np_arr, chunks=2)
    return dask_arr

def gen_astropy_data():
    data = np.array([[100, 200]], dtype=np.uint16)
    hdu = fits.PrimaryHDU(data)
    hdulist = fits.HDUList([hdu])

    buffer = BytesIO()
    hdulist.writeto(buffer)
    buffer.seek(0)

    hdul_from_buffer = fits.open(buffer)
    return hdul_from_buffer[0].data

def gen_h5py_data():
    # Simulate HDF5 in-memory
    buffer = BytesIO()
    with h5py.File(buffer, "w") as f:
        f.create_dataset("my_uint16_data", data=np.array([1, 2, 3], dtype=np.uint16))

    # Read the dataset
    buffer.seek(0)
    with h5py.File(buffer, "r") as f:
        h5py_data = f["my_uint16_data"][:]
    return h5py_data

def gen_pil_data():
    # Create a dummy 16-bit grayscale image for PIL
    img = Image.new(mode="I;16", size=(1, 1))
    buffer = BytesIO()
    img.save(buffer, format="TIFF")
    buffer.seek(0)
    return Image.open(buffer)

# Pack a 16-bit unsigned int using struct
def gen_struct_data():
    packed_data = struct.pack("H", 65535)  # 'H' = uint16
    return struct.unpack("H", packed_data)[0]

