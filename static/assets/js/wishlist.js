function wishlistManager() {
    fetch(`http://127.0.0.1:8000/api/wishlist/`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(response => response.json())
        .then(data => {
            wishlist_tbody = document.getElementById('wishlist_tbody');
            if (wishlist_tbody) {
                wishlist_tbody.innerHTML = '';
            }
            id_arr = []
            for (let i = 0; i < data['course'].length; i++) {
                id_arr.push(data['course'][i]['id'])
                console.log(data['course'][i]['id'])

                if (wishlist_tbody) {

                    wishlist_tbody.innerHTML += `
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
					`;
                }
            }
            

        });
}

window.addEventListener('DOMContentLoaded', (event) => {
    wishlistManager()
});

// function addtoCartFromWishlist() {
//     const addToBasket = document.querySelectorAll('.add_to_cart');
//     addToBasket.forEach(item => {
//         item.onclick = function () {
//             if (item.classList.contains('disabled') == false) {
//                 if (item.tagName == 'A') {
//                     item.style.backgroundColor = "green";
//                     item.style.color = "white";
//                     item.innerText = "Added to cart"
//                     item.classList.add('disabled')
//                     setTimeout(() => {
//                         item.style.background = "";
//                         item.style.color = "";
//                         item.innerText = "Add to cart"
//                         item.classList.remove('disabled')
//                     }, 1000);
//                 } else {
//                     item.parentElement.style.backgroundColor = "green";
//                     item.style.color = "white";
//                     item.classList.add('disabled')
//                     setTimeout(() => {
//                         item.parentElement.style.background = "";
//                         item.style.color = "";
//                         item.classList.remove('disabled')
//                     }, 1000);
//                 }
//                 const productId = this.getAttribute('data');
//                 template = "product_list.html"
//                 try {
//                     quantity = document.getElementById('quantity').value;
//                 } catch {
//                     quantity = 1
//                 }
//                 BasketLogic.productManager(productId, quantity, template);


//             }
//         }
//     })
// }

function removeFromWishlist() {
    var removeFromWishlist = document.querySelectorAll('.removeFromWishlist');
    for (let i = 0; i < removeFromWishlist.length; i++) {
        removeFromWishlist[i].onclick = function () {
            const courseId = this.getAttribute('data');
            WishlistLogic.wishlistPostManager(courseId);
        }
    }
}