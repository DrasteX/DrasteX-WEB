
function testfn(ele){
    console.log(ele)
}
function update_cart(id, quantity) {
    fetch('/update_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "id": id,
            "quantity": quantity
        })
    });
}

function delete_button_onclickfn(btn, id) {
    btn.parentElement.parentElement.parentElement.parentElement.remove();
    update_cart(id, quantity = 0);
}

function remove_item(button, id) {
    const input = button.nextElementSibling;
    if (input.value > 1) {
        input.value -= 1;
    }
    update_cart(id, input.value);
}

function add_item(button, id) {
    const input = button.previousElementSibling;
    input.value = parseInt(input.value) + 1;
    update_cart(id, input.value);
}
document.addEventListener('DOMContentLoaded', () => {
    const email = document.getElementById('session-email').value;
    document.getElementById('session-email').remove();

    let products_data;
    

    

    Promise.all([
        fetch('/static/JSON/products.json').then(response => response.json()),
        fetch('/static/JSON/user_products_info.json').then(response => response.json())
    ]).then(([productsData, userProductsInfo]) => {
        products_data = productsData;
        if (userProductsInfo && Object.keys(userProductsInfo).length > 0) {
            const cartdata = userProductsInfo[email]['cart'];
            const summary_cont = document.querySelector('.order_items_in_cart');
            let totalcost = 0;

            for (const item in cartdata) {
                const cart_item = document.createElement('div');
                cart_item.classList.add('cart_item');
                const cartdata_item = cartdata[item];
                const products_data_item = products_data[item.replace("_"+cartdata_item['size'], '')];
                cart_item.innerHTML = `
                    <img class="item_image_cart" src="${'/static/' + products_data_item['mockup1']}">
                    <div class="cart_item_main_cont">
                        <span id="title_cart_item">${products_data_item['product_name']}</span>
                        <div class="cart_item_colour_size_share_delete_container">
                            <div class="sizeandcolor_cart"><span>${cartdata_item['color'].toUpperCase()}</span> <span>${cartdata_item['size'].toUpperCase()}</span></div>
                            <div class="shareanddelete_cart">
                                <div class="add_remove_items"><span onclick="remove_item(this,'${item}')" id="remove_item">-</span> <input id="number_of_items" min="1" value="${Number(cartdata_item['quantity'])}" type="number"> <span onclick="add_item(this, '${item}')" id="add_item">+</span></div>
                                <img class='delete_item' src="/static/Assets/Components/delete_btn.png" onclick="delete_button_onclickfn(this, '${item}')">
                            </div>
                        </div>
                        <span class="price_text_cart">INR ${Number(products_data_item['price']) * Number(cartdata_item['quantity'])}</span>
                    </div>`;
                document.querySelector('.cart_main_container').appendChild(cart_item);

                let rquantity;
                if (String(cartdata_item['quantity']).length == 1) {
                    rquantity = "0" + String(cartdata_item['quantity']);
                } else {
                    rquantity = cartdata_item['quantity'];
                }
                const buy_btn = document.querySelector('.place_order_btn')
                buy_btn.onclick = ()=>{
                    window.location.href="/checkout?product_id="+item.replace("_"+cartdata_item['size'], '')+"&order_type=1"
                }

                const summary_item = document.createElement('div');
                summary_item.classList.add('order_item');
                summary_item.innerHTML = `
                    <span class="order_item_quantity">${rquantity}</span>
                    <span class="order_item_name">${products_data_item['product_name']}</span>
                    <span class="order_item_price">INR ${Number(products_data_item['price']) * Number(cartdata_item['quantity'])}</span>`;
                totalcost += Number(products_data_item['price']);
                summary_cont.appendChild(summary_item);
            }

            document.querySelector('.total_num').textContent = `INR ${totalcost}`;
        }
    }).catch(error => {
        console.error('Error fetching data:', error);
    });
});
