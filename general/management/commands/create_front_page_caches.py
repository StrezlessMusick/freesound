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

import json
import logging
import time
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.cache import cache

from donations.models import Donation
from sounds.models import Download, Pack, Sound
from sounds.views import get_n_weeks_back_datetime
from utils.management_commands import LoggingBaseCommand

commands_logger = logging.getLogger("commands")


class Command(LoggingBaseCommand):
    help = "Create caches needed for front page"

    def handle(self, **options):
        self.log_start()

        cache_time = 24 * 60 * 60  # 1 day cache time
        # NOTE: The specific cache time is not important as long as it is bigger than the frequency with which we run
        # create_front_page_caches management command

        # Generate cache for the blog news from blog's RSS feed
        # Create one for Freeesound Nightingale frontend and one for BeastWhoosh
        rss_cache = render_to_string('rss_cache.html', {'rss_url': settings.FREESOUND_RSS})
        cache.set("rss_cache", rss_cache, cache_time)
        rss_cache_bw = render_to_string('molecules/news_cache.html', {'rss_url': settings.FREESOUND_RSS})
        cache.set("rss_cache_bw", rss_cache_bw, cache_time)

        # TODO: we still don't know how to handle multiple news entries in BW, currently only the latest will be shown

        # Generate popular searches cache
        popular_searches = ['wind', 'music', 'footsteps', 'woosh', 'explosion', 'scream', 'click', 'whoosh', 'piano',
                            'swoosh', 'rain', 'fire']
        cache.set("popular_searches", popular_searches,  cache_time)

        # TODO: we have to decide how do we determine "trending searches" and how often these are updated. Depending on
        # this we'll have to change the frequency with which we run create_front_page_caches management command

        # Generate trending sounds cache
        trending_sound_ids = list(Download.objects.order_by('-created').values_list('sound_id', flat=True)[0:9])
        cache.set("trending_sound_ids", trending_sound_ids,  cache_time)

        # TODO: decide how to compute trending sounds. Current implementation simply takes the 3 most recent downloads.
        # Depending on the calculation of trending sounds we might need to change periodicity with which we run
        # create_front_page_caches

        # Generate trending packs cache
        trending_pack_ids = list(Pack.objects.select_related('user').filter(num_sounds__gte=3)
                                 .order_by('-last_updated').values_list('id', flat=True)[:9])
        cache.set("trending_pack_ids", trending_pack_ids, cache_time)

        # TODO: decide what we consider to be a trending pack, for now we just take the last 9 that were updated

        # Add total number of sounds in Freesound to the cache
        total_num_sounds = Sound.public.all().count()
        cache.set("total_num_sounds", total_num_sounds, cache_time)

        # Calculate top donor
        last_week = get_n_weeks_back_datetime(n_weeks=1)
        top_donor_data = defaultdict(int)
        for username, amount in \
                Donation.objects.filter(created__gt=last_week) \
                        .exclude(user=None, is_anonymous=True) \
                        .values_list('user__username', 'amount'):
            top_donor_data[username] += amount
        if top_donor_data:
            top_donor_username = sorted(top_donor_data.items(), key=lambda x: x[1], reverse=True)[0][0]
            top_donor = User.objects.get(username=top_donor_username)
            cache.set("top_donor_user_id", top_donor.id, cache_time)
        else:
            cache.set("top_donor_user_id", None, cache_time)

        self.log_end()
