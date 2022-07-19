import pathlib

import imageio
import pytest

from microscopy_automation.tests import mocks


@pytest.fixture
def artifacts_dirpath():
    return pathlib.Path(__file__).parent / 'artifacts'


@pytest.fixture
def raw_image(artifacts_dirpath):
    '''
    An example of a real raw image acquired by the microscope with proper exposure settings
    '''
    return imageio.imread(artifacts_dirpath / 'raw-image-properly-exposed.tif')


@pytest.fixture
def get_microscope_interface(raw_image):
    '''
    Factory fixture that returns a mocked microscope interface
    instantiated with the raw_image (as a numpy array)
    '''

    def _get_microscope_interface(*args, **kwargs):
        return mocks.MockedMicroscopeInterface(raw_image, *args, **kwargs)

    return _get_microscope_interface


@pytest.fixture
def autoexposure_settings():
    '''
    Mock the autoexposure_settings object
    '''

    class AutoexposureSettings:

        # minimum and maximum possible exposure times
        min_exposure_time = 1
        max_exposure_time = 500
        initial_exposure_time = 100

        # proportion by which to decrement exposure time for over-exposed images
        relative_exposure_step = 0.8

        # intensity threshold that defines under-exposure
        min_intensity = 150

        # intensity threshold that defines over-exposure
        max_intensity = 200

    return AutoexposureSettings()
