from typing import List, Optional, Dict, Any, Set
from django import template
from django.http import HttpRequest

from menu.models import MenuItem


register = template.Library()


def get_all_menu_items(menu_title: str) -> List[MenuItem]:
    """Получить все пункты меню с указанным именем."""
    return list(
        MenuItem.objects
        .select_related('parent')
        .filter(menu__title=menu_title)
        .order_by('order')
    )


def normalize_path(path: str) -> str:
    """Привести путь к единому виду"""
    if not path.endswith('/'):
        path += '/'
    return path.split('?')[0]


def find_active_item(menu_items: List[MenuItem], request_path: str) -> Optional[MenuItem]:
    """Определить активный пункт меню по совпадению request.path с URL пункта."""
    request_path = normalize_path(request_path)
    for item in menu_items:
        url = item.get_url()
        if url and url != '#':
            if normalize_path(url) == request_path:
                return item
    return None


def get_expanded_ids(active_item: Optional[MenuItem]) -> Set[int]:
    """Возвратить множество id всех пунктов, лежащих на пути к активному пункту (включая его самого)."""
    expanded = set()
    parent = active_item
    while parent:
        expanded.add(parent.id)
        parent = parent.parent
    return expanded


def build_children_map(items: List[MenuItem]) -> Dict[Optional[int], List[MenuItem]] :
    """Возвращает словарь соответствия parent_id -> [MenuItem, ...] для дерева."""
    children_map = {}
    for item in items:
        children_map.setdefault(item.parent_id, []).append(item)
    return children_map

def build_nodes(
        parent_id: Optional[int],
        children_map: Dict[Optional[int], List[MenuItem]],
        active_item: Optional[MenuItem],
        expanded_ids: Set[int],
        parent_is_active: bool = False
) -> List[Dict[str, Any]]:
    """Рекурсивно построить дерево пунктов меню."""
    nodes = []
    for item in children_map.get(parent_id, []):
        is_active = active_item and item.id == active_item.id
        is_expanded = item.id in expanded_ids
        if is_expanded or is_active or parent_is_active:
            child_items = build_nodes(
                item.id, children_map, active_item, expanded_ids, parent_is_active=is_active
            )
        else:
            child_items = []
        node = {
            'item': item,
            'is_active': is_active,
            'is_expanded': is_expanded,
            'child_items': child_items,
        }
        nodes.append(node)
    return nodes


# def build_nodes(
#         parent_id: Optional[int],
#         children_map: Dict[Optional[int], List[MenuItem]],
#         active_item: Optional[MenuItem],
#         expanded_ids: Set[int],
#         parent_is_active: bool = False
# ) -> List[Dict[str, Any]]:
#     nodes = []
#     for item in children_map.get(parent_id, []):
#         is_active = active_item is not None and item.id == active_item.id
#         is_expanded = (
#                 item.id in expanded_ids
#                 or (active_item is not None and item.parent_id == active_item.id)
#         )
#
#         # Всегда строим все дочерние элементы
#         child_items = build_nodes(
#             item.id, children_map, active_item, expanded_ids, parent_is_active=is_active
#         )
#
#         node = {
#             'item': item,
#             'is_active': is_active,
#             'is_expanded': is_expanded,
#             'child_items': child_items,
#         }
#         nodes.append(node)
#     return nodes





@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context: Dict[str, Any], menu_title: str) -> Dict[str, Any]:
    """Django inclusion tag для построения древовидного меню."""
    request = context.get('request')
    if not request:
        return {
            'menu_title': menu_title,
            'tree': [],
            'request': None,
        }
    all_items = get_all_menu_items(menu_title)
    active_item = find_active_item(all_items, request.path)
    expanded_ids = get_expanded_ids(active_item) if active_item else set()
    children_map = build_children_map(all_items)
    tree = build_nodes(None, children_map, active_item, expanded_ids, parent_is_active=False)

    return {
        'menu_title': menu_title,
        'tree': tree,
        'request': request,
    }
