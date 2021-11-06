window.addEventListener("load", function (evt){

    let _quantity, _price, orderitem_num, delta_quantity, order_item_quantity, delta_cost

    let quantity_arr = []
    let price_arr = []

    let total_forms = parseInt($('input[name=order_item-TOTAL_FORMS]').val())


    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;

    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;


    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=order_item-' + i + '-quantity]').val());
        _price = parseInt($('.order_items-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }

    }


    $('.order_form').on('click', 'input[type=number]', function () {

        let target = event.target
        orderitem_num = parseInt(target.name.replace('order_item-', '').replace('-quantity', ''));

        if (price_arr[orderitem_num]) {
            order_item_quantity = parseInt(target.value);

            delta_quantity = order_item_quantity - quantity_arr[orderitem_num];

            quantity_arr[orderitem_num] = order_item_quantity
            console.info('PRICE', price_arr)
            console.info('QUANTITY', quantity_arr)

            orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        }



    })

    $('.order_form').on('click', 'input[type=checkbox]', function () {

        let target = event.target
        orderitem_num = parseInt(target.name.replace('order_item-', '').replace('-DELETE', ''));

        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num]
        } else {
            delta_quantity = quantity_arr[orderitem_num]

        }

        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)

    })


    function orderSummerUpdate(order_item_price, delta_quantity) {
        delta_cost = order_item_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toString() + ',00');

    }

    $(document).on('change', 'select[type=drop_list]', function () {
        let target = event.target
        console.log(target.name);
        orderitem_num = parseInt(target.name.replace('order_item-', '').replace('-quantity', ''));
        console.log(orderitem_num);
        product_item = target.value;
        console.log(product_item);

        $.ajax({
            url: '/products/price/' + product_item,
            success: function (data){

                    console.log(data.price);
                    price_arr[orderitem_num]=parseFloat(data.price);
                    console.log('<span class="order_items-' + orderitem_num + '-price">' + data.price.toString() + ' руб </span>');
                    let price_html = '<span class="order_items-' + orderitem_num + '-price">' + data.price.toString().replace('.', ',') + ' руб</span>';

                    let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                    console.log(current_tr.find('tr:eq(2)'));
                    current_tr.find('td:eq(2)').html(price_html);
            }

        });


    })

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'order_item',
        removed: deleteOrderItem,

    })

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        console.log(target_name)
        orderitem_num = parseInt(target_name.replace('order_item-', '').replace('-quantity', ''));
        console.log(orderitem_num)
        delta_quantity = -quantity_arr[orderitem_num];
        console.log(delta_quantity)

        orderSummerUpdate(price_arr[orderitem_num], delta_quantity);

    }

})