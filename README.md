# Django

For English please scroll down



Данный проект – интернет-магазин. На главной странице отображаются товары. Их можно отсортировать с помощью меню в левой части. На странице товары отображаются по три товара (сделано с помощью пагинатора)
Для дополнения категорий и товаров на сайт после миграций можно выполнить скрипт:
python manage.py fill_db

![catalog](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/shop_catalog.png)
В интернет-магазине можно зарегистрироваться с помощью формы регистрации.

Так же можно пройти авторизауию с помощью аккаунта ВК. Данные от аккаунта будут подтянуты в личный профиль.

![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/profile.png)

В профиле отображается корзина. Для обновления итоговой стоимости перезагрузка не требуется (реализовано с jquery)

При оформлении заказа переходит на страницу заказов, там можно изменить заказ, формить его.
Для обновления итоговой стоимости перезагрузка так же не требуется (реализовано с jquery)
![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/orders.png)

Реализована кастомная панель администратора. В ней можно редактировать, создавать, удалять пользователей, категории и товары.

![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/custom_admin_users.png)

Ветвь lesson2-8 подготовлена для запуске на сервере (postgresql, nginx, gunicorn)

*******************************************************************************************************************************************



This project is an online-shop. There is a catalog with goods on a main page . Goods can be filtered by categories. total quantity of goods is 3 (proceeed with a paginator)
Сategories and goods can be added after migrations with a command:
python manage.py fill_db

![catalog](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/shop_catalog.png)
You can register on a site with a standard form.


You can authorise with VK account. Required profiles details will be taken from VK.

![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/profile.png)

Bastket can be obtained in a profile. Page refresh is not required to calculate final price in case of quantity change (proceed with  jquery)

You go to order pagge after order submission. You can change goods, quantity before order finalisation.
Page refresh is not required to calculate final price in case of quantity change (proceed with  jquery)
![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/orders.png)

Site has custom admin console. You can change, create , delete users, categories and goods.

![profile](https://github.com/AleksandrVladimirovichNaumov/Django/raw/master/screenshots/custom_admin_users.png)

Branch lesson2-8 is prepared for installation on a server (postgresql, nginx, gunicorn)