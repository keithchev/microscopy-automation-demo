from microscopy_automation.autoexposure import autoexposure


def test_autoexposure_overrexposed_image(get_microscope_interface, autoexposure_settings):
    '''
    Check that the exposure time is decreased when the image is initally over-exposed
    '''
    microscope_interface = get_microscope_interface(sample_brightness=10)
    exposure_time = autoexposure(microscope_interface, autoexposure_settings)

    # since the image was over-exposed, the calculated exposure time should be shorter
    assert exposure_time < autoexposure_settings.initial_exposure_time


def test_autoexposure_underexposed_image(get_microscope_interface, autoexposure_settings):
    '''
    Check that the exposure time is increased when an image is initially under-exposed
    '''
    microscope_interface = get_microscope_interface(sample_brightness=0.001)
    exposure_time = autoexposure(microscope_interface, autoexposure_settings)

    # since the image was under-exposed, the calculated exposure time should be longer
    assert exposure_time > autoexposure_settings.initial_exposure_time


def test_autoexposure_underexposed_image_with_hot_pixels(
    get_microscope_interface, autoexposure_settings
):
    '''
    Check that the autoexposure function is insensitive to a few hot pixels
    in an otherwise under-exposed image
    '''
    microscope_interface = get_microscope_interface(sample_brightness=0.001, num_hot_pixels=10)
    exposure_time = autoexposure(microscope_interface, autoexposure_settings)
    assert exposure_time > autoexposure_settings.initial_exposure_time


def test_autoexposure_underexposed_image_with_too_many_hot_pixels(
    get_microscope_interface, autoexposure_settings
):
    '''
    Check that the autoexposure function *is* sensitive to hot pixels if there are enough of them
    in an otherwise under-exposed image
    '''
    microscope_interface = get_microscope_interface(sample_brightness=0.001, num_hot_pixels=1000)
    exposure_time = autoexposure(microscope_interface, autoexposure_settings)
    assert exposure_time < autoexposure_settings.initial_exposure_time
