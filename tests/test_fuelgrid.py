"""
Test fuelgrid object and endpoints.
"""

# Internal imports
import sys

sys.path.append("../")
from fastfuels_sdk.datasets import *
from fastfuels_sdk.treelists import *
from fastfuels_sdk.fuelgrids import *

# Core imports
from uuid import uuid4
from time import sleep

# External imports
import zarr
import pytest
import numpy as np
from requests.exceptions import HTTPError


def setup_module(module):
    with open("test-data/test.geojson") as f:
        spatial_data = json.load(f)

    # Create a test dataset
    global DATASET
    DATASET = create_dataset(name="test_dataset", description="test dataset",
                             spatial_data=spatial_data)

    # Create a test treelist
    global TREELIST
    TREELIST = DATASET.create_treelist(name="test_treelist",
                                       description="test treelist",)
    TREELIST.wait_until_finished()


def test_create_fuelgrid_uniform():
    """
    Test creating a fuelgrid.
    """
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform")

    assert fuelgrid.id is not None

    # Test that the fuelgrid is in the dataset
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]

    # Test that the fuelgrid is in the treelist
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]


def test_create_fuelgrid_distribution_methods():
    """
    Test creating a fuelgrid with different distribution methods.
    """
    # Test random distribution
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="random")
    assert fuelgrid.id is not None
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]

    # Test realistic distribution
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="realistic")
    assert fuelgrid.id is not None
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]


def test_create_fuelgrid_interpolation_methods():
    """
    Test creating a fuelgrid with different interpolation methods.
    """
    temp_id_list = []

    # Test zipper interpolation
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform",
                               surface_interpolation_method="zipper")
    assert fuelgrid.id is not None
    temp_id_list.append(fuelgrid.id)
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]

    # Test linear interpolation
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform",
                               surface_interpolation_method="linear")
    assert fuelgrid.id is not None
    temp_id_list.append(fuelgrid.id)
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]

    # Test cubic interpolation
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="test_fuelgrid",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform",
                               surface_interpolation_method="cubic")
    assert fuelgrid.id is not None
    temp_id_list.append(fuelgrid.id)
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]

    # Iterate over temp_id_list and check for status finished
    for temp_id in temp_id_list:
        fuelgrid = get_fuelgrid(temp_id)
        while fuelgrid.status != "Finished":
            fuelgrid = get_fuelgrid(temp_id)
            sleep(2)


def test_create_fuelgrid_bad_inputs():
    """
    Test creating a fuelgrid with bad inputs.
    """
    # Test bad dataset id
    with pytest.raises(HTTPError):
        create_fuelgrid(dataset_id=uuid4().hex,
                        treelist_id=TREELIST.id,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        distribution_method="uniform",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)

    # Test bad treelist id
    with pytest.raises(HTTPError):
        create_fuelgrid(dataset_id=DATASET.id,
                        treelist_id=uuid4().hex,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        distribution_method="uniform",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)

    # Test bad surface fuel source
    with pytest.raises(ValueError):
        create_fuelgrid(dataset_id=DATASET.id,
                        treelist_id=uuid4().hex,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        surface_fuel_source="nonesuch",
                        distribution_method="uniform",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)

    # Test bad surface interpolation method
    with pytest.raises(ValueError):
        create_fuelgrid(dataset_id=DATASET.id,
                        treelist_id=uuid4().hex,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        surface_interpolation_method="nonesuch",
                        distribution_method="uniform",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)

    # Test bad distribution method
    with pytest.raises(ValueError):
        create_fuelgrid(dataset_id=DATASET.id,
                        treelist_id=uuid4().hex,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        distribution_method="nonesuch",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)


def test_create_fuelgrid_incomplete_treelist():
    """
    Test creating a fuelgrid with an incomplete treelist.
    """
    # Create a treelist
    treelist = create_treelist(dataset_id=DATASET.id,
                               name="test_treelist",
                               description="test treelist")

    # Try and create a fuelgrid while the treelist is incomplete
    with pytest.raises(HTTPError):
        create_fuelgrid(dataset_id=DATASET.id,
                        treelist_id=treelist.id,
                        name="test_fuelgrid",
                        description="test fuelgrid",
                        distribution_method="uniform",
                        horizontal_resolution=1,
                        vertical_resolution=1,
                        border_pad=1)


def test_get_fuelgrid():
    """
    Test getting a fuelgrid.
    """
    # Create a fuelgrid
    new_fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                                   treelist_id=TREELIST.id,
                                   name="test_fuelgrid",
                                   description="test fuelgrid",
                                   distribution_method="uniform",
                                   horizontal_resolution=1,
                                   vertical_resolution=1,
                                   border_pad=1)
    while new_fuelgrid.status != "Finished":
        new_fuelgrid = get_fuelgrid(new_fuelgrid.id)
        sleep(2)

    # Get the fuelgrid
    fuelgrid = get_fuelgrid(new_fuelgrid.id)

    # Compare the fuelgrids
    assert fuelgrid.id == new_fuelgrid.id
    assert fuelgrid.name == new_fuelgrid.name
    assert fuelgrid.description == new_fuelgrid.description
    assert fuelgrid.status == new_fuelgrid.status
    assert fuelgrid.dataset_id == new_fuelgrid.dataset_id
    assert fuelgrid.treelist_id == new_fuelgrid.treelist_id
    assert fuelgrid.surface_fuel_source == new_fuelgrid.surface_fuel_source
    assert fuelgrid.surface_interpolation_method == new_fuelgrid.surface_interpolation_method
    assert fuelgrid.distribution_method == new_fuelgrid.distribution_method
    assert fuelgrid.horizontal_resolution == new_fuelgrid.horizontal_resolution
    assert fuelgrid.vertical_resolution == new_fuelgrid.vertical_resolution
    assert fuelgrid.border_pad == new_fuelgrid.border_pad
    assert fuelgrid.created_on == new_fuelgrid.created_on
    assert fuelgrid.version == new_fuelgrid.version


def test_get_fuelgrid_bad_id():
    """
    Test getting a fuelgrid with a bad id.
    """
    with pytest.raises(HTTPError):
        get_fuelgrid(uuid4().hex)


def test_list_fuelgrids():
    """
    Test listing fuelgrids.
    """
    # Create a fuelgrid
    new_fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                                   treelist_id=TREELIST.id,
                                   name="test_fuelgrid",
                                   description="test fuelgrid",
                                   distribution_method="uniform",
                                   horizontal_resolution=1,
                                   vertical_resolution=1,
                                   border_pad=1)

    # List the fuelgrids
    fuelgrids = list_fuelgrids()

    # Check that the new fuelgrid is in the list
    assert new_fuelgrid.id in [fuelgrid.id for fuelgrid in fuelgrids]

    # Check that all the fuelgrids are in the dataset
    dataset = get_dataset(DATASET.id)
    for fuelgrid in fuelgrids:
        assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]

    # Check that all the fuelgrids are in the treelist
    treelist = get_treelist(TREELIST.id)
    for fuelgrid in fuelgrids:
        assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]


def test_download_fuelgrid_data():
    """
    Test downloading fuelgrid data to a string file path.
    """
    # Create a fuelgrid
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="fuelgrid_download_test",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform")

    # Assert that we get an error when the fuelgrid is not finished
    with pytest.raises(HTTPError):
        download_zarr(fuelgrid.id, "test-data")

    # Wait for the fuelgrid to finish
    while fuelgrid.status != "Finished":
        fuelgrid = get_fuelgrid(fuelgrid.id)
        sleep(2)

    # Open the test data
    test_zroot = zarr.open("test-data/test_small_fuelgrid.zip")
    test_canopy = test_zroot["canopy"]
    test_surface = test_zroot["surface"]

    for fpath in ["test-data/tmp", "test-data/tmp/fuelgrid_download_test.zip",
                  Path("test-data/tmp/fuelgrid_download_test.zip"),
                  Path("test-data/tmp")]:
        # Download the fuelgrid data to a file path
        download_zarr(fuelgrid.id, fpath)

        # Open the file and check that it is not empty
        zroot = zarr.open(f"test-data/tmp/{fuelgrid.name}.zip")
        assert len(zroot) > 0

        # Check that the file has the correct attributes
        attributes = zroot.attrs.asdict()
        assert attributes["dx"] == 1.0
        assert attributes["dy"] == 1.0
        assert attributes["dz"] == 1.0
        assert attributes["nx"] == 72
        assert attributes["ny"] == 93
        assert attributes["nz"] > 40
        assert attributes["pad"] == 0
        assert attributes["xmax"] == -1366699.5
        assert attributes["xmin"] == -1366770.5
        assert attributes["ymax"] == 2777949.5
        assert attributes["ymin"] == 2777857.5

        # Check that the file contains two groups: canopy and surface
        assert "canopy" in zroot
        assert "surface" in zroot
        assert "not-a-real-group" not in zroot

        # Check that the canopy group has the following arrays: bulk-density,
        # SAV, and species-code
        canopy = zroot["canopy"]
        assert len(canopy) == 4
        assert "bulk-density" in canopy
        assert "SAV" in canopy
        assert "species-code" in canopy
        assert "FMC" in canopy
        assert "not-a-real-array" not in canopy

        # Assert that the x and y dimensions are the same for the downloaded
        # canopy and test canopy groups
        assert (canopy["bulk-density"].shape[0] ==
                test_canopy["bulk-density"].shape[0])
        assert (canopy["bulk-density"].shape[1] ==
                test_canopy["bulk-density"].shape[1])
        assert canopy["SAV"].shape[0] == test_canopy["SAV"].shape[0]
        assert canopy["SAV"].shape[1] == test_canopy["SAV"].shape[1]
        assert canopy["FMC"].shape[0] == test_canopy["FMC"].shape[0]
        assert canopy["FMC"].shape[1] == test_canopy["FMC"].shape[1]
        assert (canopy["species-code"].shape[0] ==
                test_canopy["species-code"].shape[0])
        assert (canopy["species-code"].shape[1] ==
                test_canopy["species-code"].shape[1])

        # Assert that the canopy arrays are not all zeros
        assert canopy["bulk-density"][...].any()
        assert canopy["SAV"][...].any()
        assert canopy["FMC"][...].any()
        assert canopy["species-code"][...].any()

        # Assert that the canopy array has a sparse matrix attribute
        # assert len(canopy.attrs["sparse_array"]["data"]) > 0

        # Check that downloaded canopy data is similar to the test canopy data.
        assert np.isclose(canopy["bulk-density"][...].mean(),
                          test_canopy["bulk-density"][...].mean(), atol=1e-3)

        # Check that the surface group has the following arrays: bulk-density,
        # DEM, FMC, fuel-depth, and SAV
        surface = zroot["surface"]
        assert len(surface) == 5
        assert "bulk-density" in surface
        assert "DEM" in surface
        assert "FMC" in surface
        assert "fuel-depth" in surface
        assert "SAV" in surface
        assert "not-a-real-array" not in surface

        # Assert that the surface arrays are the correct shape
        assert (surface["bulk-density"][...].shape ==
                test_surface["bulk-density"][...].shape)
        assert (surface["DEM"][...].shape ==
                test_surface["DEM"][...].shape)
        assert (surface["FMC"][...].shape ==
                test_surface["FMC"][...].shape)
        assert (surface["fuel-depth"][...].shape ==
                test_surface["fuel-depth"][...].shape)
        assert (surface["SAV"][...].shape ==
                test_surface["SAV"][...].shape)

        # # Assert that the downloaded surface arrays and the test surface arrays
        # # are similar
        # assert np.allclose(surface["bulk-density"][...],
        #                    test_surface["bulk-density"][...])
        # assert np.allclose(surface["DEM"][...],
        #                    test_surface["DEM"][...])
        # assert np.allclose(surface["FMC"][...],
        #                    test_surface["FMC"][...])
        # assert np.allclose(surface["fuel-depth"][...],
        #                    test_surface["fuel-depth"][...])
        # assert np.allclose(surface["SAV"][...],
        #                    test_surface["SAV"][...])


def test_download_fuelgrid_data_bad_id():
    """
    Test downloading fuelgrid data with a bad fuelgrid id.
    """
    with pytest.raises(HTTPError):
        download_zarr(uuid4().hex, "test-data")


def test_delete_fuelgrid():
    """
    Test deleting a fuelgrid.
    """
    # Create a fuelgrid
    fuelgrid = create_fuelgrid(dataset_id=DATASET.id,
                               treelist_id=TREELIST.id,
                               name="fuelgrid_delete_test",
                               description="test fuelgrid",
                               horizontal_resolution=1,
                               vertical_resolution=1,
                               border_pad=0,
                               distribution_method="uniform")

    # Wait for the fuelgrid to finish
    while fuelgrid.status != "Finished":
        fuelgrid = get_fuelgrid(fuelgrid.id)
        sleep(2)

    # Assert that the fuelgrid is in the database
    assert get_fuelgrid(fuelgrid.id)
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id in [fg_id for fg_id in treelist.fuelgrids]

    # Delete the fuelgrid
    delete_fuelgrid(fuelgrid.id)

    # Assert that the fuelgrid is no longer in the database
    with pytest.raises(HTTPError):
        get_fuelgrid(fuelgrid.id)
    dataset = get_dataset(DATASET.id)
    assert fuelgrid.id not in [fg_id for fg_id in dataset.fuelgrids]
    treelist = get_treelist(TREELIST.id)
    assert fuelgrid.id not in [fg_id for fg_id in treelist.fuelgrids]


def test_delete_all_fuelgrids():
    """
    Test deleting all fuelgrids.
    """
    # Delete all fuelgrids
    delete_all_fuelgrids()

    # List the fuelgrids
    fuelgrids = list_fuelgrids()

    # Check that there are no fuelgrids
    assert len(fuelgrids) == 0

    # Check that the dataset has no fuelgrids
    dataset = get_dataset(DATASET.id)
    assert len(dataset.fuelgrids) == 0

    # Check that the treelist has no fuelgrids
    treelist = get_treelist(TREELIST.id)
    assert len(treelist.fuelgrids) == 0
