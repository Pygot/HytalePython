# type: ignore

from com.hypixel.hytale.server.core.modules.entity.component import TransformComponent


def get_position(ref, store):
    transform_component = store.getComponent(ref, TransformComponent.getComponentType())

    if transform_component:
        return transform_component.getPosition()
    return None


def get_rotation(ref, store):
    transform_component = store.getComponent(ref, TransformComponent.getComponentType())

    if transform_component:
        return transform_component.getRotation()
    return None
