import logging

import numpy as np

lgger = logging.getLogger()


def rescale_image(raw_image, scale):
    '''
    Simulate an under- or over-exposed image by multiplicatively rescaling its intensities
    and then clamping the rescaled intensities to the range of uint8

    raw_image : a numpy array representing a raw image (of any dimensions and any dtype)
    scale : an arbitrary scale factor greater than zero
        if less than one, the rescaled image will appear under-exposed
        if greater than one, the rescaled image will appear over-exposed
    '''
    normalized_image = raw_image.copy().astype(float)
    min_intensity = normalized_image.min()
    max_intensity = normalized_image.max()

    # normalize the raw intensities to [0, 1]
    if max_intensity > min_intensity:
        normalized_image -= min_intensity
        normalized_image[normalized_image < 0] = 0
        normalized_image /= max_intensity - min_intensity
        normalized_image[normalized_image > 1] = 1
    else:
        normalized_image *= 0

    # rescale the normalized image
    rescaled_image = normalized_image * scale

    # clamp the max intensity to 1
    # (this will result in the saturated pixels that characterize an over-exposed image,
    # as long as the `scale` was sufficiently large)
    rescaled_image[rescaled_image > 1] = 1

    # coerce to uint8
    rescaled_image = (255 * rescaled_image).astype('uint8')
    return rescaled_image


class MockedMicroscopeInterface:
    def __init__(self, raw_image, sample_brightness=1, num_hot_pixels=0):

        self._raw_image = raw_image
        self._sample_brightness = sample_brightness
        self._num_hot_pixels = num_hot_pixels
        self._exposure_time = None

    def acquire_image(self):
        '''
        Acquires an image using current exposure settings and returns the image data
        as a numpy array
        '''
        if self._exposure_time is None:
            raise ValueError('Exposure time is not set')

        total_brightness = self._exposure_time * self._sample_brightness
        mocked_image = rescale_image(self._raw_image, scale=total_brightness)

        # add the hot pixels, if any
        for _ in range(self._num_hot_pixels):
            mocked_image[tuple(np.random.randint(mocked_image.shape[0], size=2))] = 255

        return mocked_image

    def set_exposure_time(self, exposure_time):
        '''
        Updates the exposure time used to 'acquire' images
        '''
        if exposure_time == 0:
            raise ValueError('Exposure time cannot be zero')

        self._exposure_time = exposure_time
