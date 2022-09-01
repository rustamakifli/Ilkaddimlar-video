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
                    total_price += parseFloat(data[i]['course']['discounted_price'])
                    html += `
            <tr>
            <td class="td-img" style="text-align: center; vertical-align: middle;">
            <a href="#"><img style="height: 5rem;" src="${data[i]['course']['image']}" alt="Add Product" /></a>
            <div class="items-dsc">
            <h5><a href="#">${data[i]['course']['title']}</a></h5>
            </div>
            </td>
            <td class="td">$${parseFloat(data[i]['course']['discounted_price']).toFixed(2)}</td>
          
            <td class="td">
            <strong>$${parseFloat(data[i]['course']['discounted_price']).toFixed(2)}</strong>
            </td>
            <td class="td"><i data="${data[i]['course']['id']}" class="mdi mdi-close remove_from_cart" onmouseover="removeFromCart()" title="Remove this product"></i></td>
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

