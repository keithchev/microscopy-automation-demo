import numpy as np


def observe_max_intensity(microscope_interface):
    '''
    Observe the maximum image intensity given the current exposure settings,
    using a percentile to calculate the 'maximum' intensity
    as a defense against hot pixels, anomalous bright spots/dust, etc
    '''
    image = microscope_interface.acquire_image()

    # the 99.99th percentile here corresponds to ~100 pixels in a 1024x1024 image
    max_intensity = np.percentile(image, 99.99)
    return max_intensity


def autoexposure(microscope_interface, autoexposure_settings):

    overexposure_did_occur = False
    calculated_exposure_time = autoexposure_settings.initial_exposure_time

    # set the exposure time on the microscope
    microscope_interface.set_exposure_time(calculated_exposure_time)
    observed_max_intensity = observe_max_intensity(microscope_interface)
    image_was_overexposed = observed_max_intensity > autoexposure_settings.max_intensity

    while image_was_overexposed:

        overexposure_did_occur = True

        # lower the exposure time
        calculated_exposure_time = (
            calculated_exposure_time * autoexposure_settings.relative_exposure_step
        )

        # break out of the while loop if the exposure time has been lowered
        # as far as it can be and the image is still over-exposed
        if calculated_exposure_time < autoexposure_settings.min_exposure_time:
            break

        # update the exposure time on the microscope
        microscope_interface.set_exposure_time(calculated_exposure_time)

        # check the exposure again
        observed_max_intensity = observe_max_intensity(microscope_interface)
        image_was_overexposed = observed_max_intensity > autoexposure_settings.max_intensity

    # if the image was never over-exposed, we need to check for under-exposure
    if not overexposure_did_occur:
        intensity_ratio = autoexposure_settings.min_intensity / observed_max_intensity

        # if the image was under-exposed, increase the exposure time
        if intensity_ratio > 1:
            calculated_exposure_time *= intensity_ratio
            if calculated_exposure_time > autoexposure_settings.max_exposure_time:
                calculated_exposure_time = autoexposure_settings.max_exposure_time

    return calculated_exposure_time
