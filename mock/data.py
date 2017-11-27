CATEGORIES = [
    {
        'name': 'electronics',
        'id': 0
    },
    {
        'name': 'clothing',
        'id': 1
    },
    {
        'name': 'computers',
        'id': 2
    },
    {
        'name': 'tools',
        'id': 3
    }
]

ITEMS = [
    {
        'id': 0,
        'name': 'Carhartt Duck Jacket',
        'description': 'Warm winter jacket.',
        'price': 89.99,
        'category': '1',
        'category_name': 'clothing',
        'image': 'jacket.jpg'
    },
    {
        'id': 1,
        'name': 'Nvidia GTX 1080Ti',
        'description': 'The most powerful graphics card on the market.',
        'price': 689.99,
        'category': '2',
        'category_name': 'computers',
        'image': 'gtx.png'
    },
    {
        'id': 2,
        'name': 'Raspberry Pi Zero W',
        'description': 'Hobby electronics control board.',
        'price': 4.99,
        'category': '0',
        'category_name': 'electronics',
        'image': 'pi.jpg'
    },
    {
        'id': 3,
        'name': 'Klein Diagonal Cutters',
        'description': 'High leverage cutting pliers for electricians.',
        'price': 34.99,
        'category': '3',
        'category_name': 'tools',
        'image': 'klein.jpg'
    },
    {
        'id': 4,
        'name': 'Redwing Irish Setter Boots',
        'description': 'High quality boots for demanding work.',
        'price': 194.99,
        'category': '1',
        'category_name': 'clothing',
        'image': 'redwing.jpg'
    }
]

def items_in_category(category_name):

    '''Returns a list of items belonging to specified category.'''

    result = []
    for item in ITEMS:
        if item['category_name'] == category_name:
            result.append(item)
    return result
