# coding=utf-8
from wraptor.decorators import throttle
from config import config
from items import get_item, get_item_kind_from_item, refresh_item

from plex_activity import Activity
from plex_activity.sources.s_logging.main import Logging as Activity_Logging


class PlexActivityManager(object):
    def start(self):
        activity_sources_enabled = None

        if config.universal_plex_token:
            from plex import Plex
            Plex.configuration.defaults.authentication(config.universal_plex_token)
            activity_sources_enabled = ["websocket"]
            Activity.on('websocket.playing', self.on_playing)

        elif config.server_log_path:
            Activity_Logging.add_hint(config.server_log_path, None)
            activity_sources_enabled = ["logging"]
            Activity.on('logging.playing', self.on_playing)

        if activity_sources_enabled:
            Activity.start(activity_sources_enabled)

    @throttle(5, instance_method=True)
    def on_playing(self, info):
        if not config.use_activities:
            return

        # ignore non-playing states and anything too far in
        if info["state"] != "playing" or info["viewOffset"] > 60000:
            return

        # don't trigger on the first hit ever
        if "last_played_items" not in Dict:
            Dict["last_played_items"] = []
            Dict.Save()
            return

        rating_key = info["ratingKey"]
        if rating_key not in Dict["last_played_items"]:
            # new playing; store last 10 recently played items
            Dict["last_played_items"].insert(0, rating_key)
            Dict["last_played_items"] = Dict["last_played_items"][:10]

            Dict.Save()

            debug_msg = "Started playing %s. Refreshing it." % rating_key

            key_to_refresh = None
            if config.activity_mode in ["refresh", "next_episode", "hybrid"]:
                # next episode or next episode and current movie
                if config.activity_mode in ["next_episode", "hybrid"]:
                    plex_item = get_item(rating_key)
                    if not plex_item:
                        Log.Warn("Can't determine media type of %s, skipping" % rating_key)
                        return

                    if get_item_kind_from_item(plex_item) == "episode":
                        next_ep = self.get_next_episode(rating_key)
                        if next_ep:
                            key_to_refresh = next_ep.rating_key
                            debug_msg = "Started playing %s. Refreshing next episode (%s, S%02iE%02i)." % \
                                        (rating_key, next_ep.rating_key, int(next_ep.season.index), int(next_ep.index))

                    else:
                        if config.activity_mode == "hybrid":
                            key_to_refresh = rating_key
                elif config.activity_mode == "refresh":
                    key_to_refresh = rating_key

                if key_to_refresh:
                    Log.Debug(debug_msg)
                    refresh_item(key_to_refresh)

    def get_next_episode(self, rating_key):
        plex_item = get_item(rating_key)
        if not plex_item:
            return

        if get_item_kind_from_item(plex_item) == "episode":
            # get season
            season = get_item(plex_item.season.rating_key)
            if not season:
                return

            # determine next episode
            # next episode is in the same season
            if plex_item.index < season.episode_count:
                # get next ep
                for ep in season.children():
                    if ep.index == plex_item.index + 1:
                        return ep

            # it's not, try getting the first episode of the next season
            else:
                # get show
                show = get_item(plex_item.show.rating_key)
                # is there a next season?
                if season.index < show.season_count:
                    for other_season in show.children():
                        if other_season.index == season.index + 1:
                            next_season = other_season
                            for ep in next_season.children():
                                if ep.index == 1:
                                    return ep

activity = PlexActivityManager()
