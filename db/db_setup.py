from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_models import Base, Category, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def create(s, obj):
    s.add(obj)
    s.commit()

user1 = User(
    name='John Archuletta',
    picture='https://lh6.googleusercontent.com/-QxaoomDZoiI/AAAAAAAAAAI/AAAAAAAAA8E/x5_SlNb51fE/photo.jpg',
    email='john@johnarchuletta.com',
    google_id='111512916056360063040'
)

create(session, user1)

category1 = Category(name='electronics')
category2 = Category(name='computers')
category3 = Category(name='clothing')
category4 = Category(name='tools')

create(session, category1)
create(session, category2)
create(session, category3)
create(session, category4)

item1 = Item(
    name='Carhartt Jacket',
    description='Warm jacket for the extremely cold weather.',
    price='89.99',
    image='https://content.backcountry.com/images/items/900/CHT/CHT0055/MOSACC.jpg',
    category=category3
)

item2 = Item(
    name='Nvidia GTX1080Ti',
    description='The most powerful graphics card on the market.',
    price='689.99',
    image='https://images.nvidia.com/pascal/img/gtx1080ti/GeForce_GTX_1080Ti_3qtr_Front_Left.png',
    category=category2
)

item3 = Item(
    name='Raspberry Pi Zero W',
    description='Hobby electronics control board.',
    price='5.99',
    image='https://www.raspberrypi.org/app/uploads/2017/05/Raspberry-Pi-Zero-1-1755x1080.jpg',
    category=category1
)

item4 = Item(
    name='Klein Diagonal Cutters',
    description='High leverage cutting pliers for electricians.',
    price='34.99',
    image='https://d35gqh05wwjv5k.cloudfront.net/media/catalog/product/k/l/klein-tools--diagonal-cutting-pliers-ee037-lg.jpg',
    category=category4
)

item5 = Item(
    name='Redwing Irish Setter Boots',
    description='High quality long-lasting boots for demanding work.',
    price='174.99',
    image='http://www.bobstores.com/on/demandware.static/-/Sites-vestis-master-catalog/default/dwf88b627d/product/images/1365/412/1365412/1365412_201_main.jpg',
    category=category3
)

item6 = Item(
    name='Hakko FX-951-66 Soldering Station',
    description='High quality soldering station for hobby electronics.',
    price='145.99',
    image='https://images-na.ssl-images-amazon.com/images/I/412CMFoYpOL._SX342_.jpg',
    category=category1
)

item7 = Item(
    name='Dell 27" 4K IPS Monitor',
    description='High resolution monitor for creative professionals.',
    price='699.99',
    image='http://snpi.dell.com/snp/images/products/large/en-us~210-AHSQ_V2/210-AHSQ_V2.jpg',
    category=category2
)

item8 = Item(
    name='Estwing Leather Wrapped Hammer',
    description='Perfectly balance hammer that can take a beating.',
    price='29.99',
    image='https://images-na.ssl-images-amazon.com/images/I/81rn8AV7FjL._SY355_.jpg',
    category=category4
)

create(session, item1)
create(session, item2)
create(session, item3)
create(session, item4)
create(session, item5)
create(session, item6)
create(session, item7)
create(session, item8)
