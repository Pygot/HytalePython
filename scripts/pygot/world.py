# type: ignore

from com.hypixel.hytale.server.core.universe import Universe


def get_world_by_name(name):
    return Universe.get().getWorld(name)
