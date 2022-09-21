var CartLogic = {
    productManager(courseId, template) {
        fetch('http://127.0.0.1:8000/api/cart/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                'course': courseId,
                'template': template,
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    cartManager()
                    cartItemManager()
                } else {
                    alert(data.message);
                }
            });
    }
}


let cart_body = document.getElementById("cart_body")

url = location.origin + '/api/cart-item/';
function cartItemManager() {
    fetch(url, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            let html = ''
            total_price = 0
            total_products = document.getElementById("total_products")
            for (let i = 0; i < data.length; i++) {
                if (data[i]['is_ordered'] == false) {
                    total_price += parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100)
                    html += `
            <tr>
            <td class="course-remove"><i data="${data[i]['course']['id']}" class="fa fa-close remove_from_cart" onmouseover="removeFromCart()" title="Remove this product"></i></td>

            <td class="course-image" style="text-align: center; vertical-align: middle;">
            <a href="#"><img width="150"  src="${data[i]['course']['image']}" alt="Add Product" /></a>
            </td>
            <td class="course-name">
            <a href="#">${data[i]['course']['title']}</a>
            </td>
            <td class="course-price">
            <del>$${parseFloat(data[i]['course']['price']).toFixed(2)} </del>
            <span>$${parseFloat(data[i]['course']['discounted_price']).toFixed(2)* (100 - data[i]['coupon_discount']) / 100}</span>
            </td>
          
            <td class="course-fullprice">
            <span>$${parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100).toFixed(2)}</span>
            </td>
            </tr>
			`
                }
            }
            cart_body.innerHTML = html
            
            if (data.length == 0) {
                total_products.style.display = 'none'
            } 

        });
}

window.addEventListener('DOMContentLoaded', (event) => {
    cartItemManager()
});

