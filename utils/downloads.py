
#
# Freesound is (c) MUSIC TECHNOLOGY GROUP, UNIVERSITAT POMPEU FABRA
#
# Freesound is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Freesound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     See AUTHORS file.
#

import zlib

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from sounds.models import License


def download_sounds(licenses_url, pack):
    """
    From a list of sounds generates the HttpResponse with the information of
    the wav files of the sonds and a text file with the license. This response
    is handled by mod_zipfile of nginx to generate a zip file with the content.
    """
    attribution = pack.get_attribution()
    license_crc = zlib.crc32(attribution.encode('UTF-8')) & 0xffffffff
    filelist = "%02x %i %s %s\r\n" % (license_crc,
                                    len(attribution.encode('UTF-8')),
                                    licenses_url, "_readme_and_license.txt")

    sounds_list = pack.sound_set.filter(processing_state="OK",
            moderation_state="OK").select_related('user', 'license')

    for sound in sounds_list:
        url = sound.locations("sendfile_url")
        name = sound.friendly_filename()
        if sound.crc == '':
            continue
        filelist += "%s %i %s %s\r\n" % (sound.crc, sound.filesize, url, name)


    response = HttpResponse(filelist, content_type="text/plain")
    response['X-Archive-Files'] = 'zip'
    return response