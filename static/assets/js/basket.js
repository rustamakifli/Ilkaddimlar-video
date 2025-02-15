const BasketLogic = {
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
					// cartItemManager()
				} else {
					alert(data.message);
				}
			});
	}
    
}


const addToBasket = document.querySelectorAll('.add_to_cart');
addToBasket.forEach(item => {
	item.onclick = function () {
		if (item.classList.contains('disabled') == false) {
			if (item.tagName == 'A') {
				item.style.backgroundColor = "green";
				item.style.color = "white";
				item.innerText = "Added to cart"
				item.classList.add('disabled')
				setTimeout(() => {
					item.style.background = "";
					item.style.color = "";
					item.innerText = "Add to cart"
					item.classList.remove('disabled')
				}, 1000);
			} else {
				item.parentElement.style.backgroundColor = "green";
				item.style.color = "white";
				item.classList.add('disabled')
				setTimeout(() => {
					item.parentElement.style.background = "";
					item.style.color = "";
					item.classList.remove('disabled')
				}, 1000);
			}
			const courseId = this.getAttribute('data');
			template = "course-list.html"
			
			BasketLogic.productManager(courseId, template);


		}
	}
})

mdi_close = document.getElementsByClassName('mdi-close')
product_count = document.getElementById("product_count")
basketItem = document.getElementById("cartdrop")
total = document.getElementById("total")

function cartManager() {
	fetch('http://127.0.0.1:8000/api/cart-item/', {
		method: 'GET',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${localStorage.getItem('token')}`
		}
	})
		.then(response => response.json())
		.then(data => {
			html = ''
			total_price = 0
			let count = 0
			
			if (data.length > 0 && data[0]['is_ordered'] == false) {
				for (let i = 0; i < data.length; i++) {
					total_price += parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100)
					count += 1
						html += `
					<div class="dropdown-cart">
					<div class="media-left remove-cart">
					<a data="${data[i]['course']['id']}" class="remove_from_cart" onmouseover="removeFromCart()"> <i class="fa fa-close"></i> </a>
					</div>
					<div class="media-left">

					  <a href="#">
						<img class="media-object" src="${data[i]['course']['image']}" alt="img" width="130">
					  </a>
					</div>
					<div class="media-body">
					  <h4 class="media-heading"><a href="#">${data[i]['course']['title']}</a></h4>                      
					  <span class="popular-course-price">$${parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100).toFixed(2)}</span>
					</div>

				  	</div>
					<hr>
					
					`
					
				}
			}
			basketItem.innerHTML = html
			basketItem.innerHTML += `<div class="total">
			<span>Total: <strong> $${total_price.toFixed(2)}</strong></span>
			</div>
			`
			total.innerText = `$${total_price.toFixed(2)}`
			product_count.innerText = count
			try {
				cartItemManager()
			} catch {
			}
			try {
				checkoutManager()
			} catch {
			}
		});
}

window.addEventListener('DOMContentLoaded', (event) => {
	cartManager()
});

function removeFromCart() {
	var remove_from_cart = document.getElementsByClassName("remove_from_cart")
	for (let i = 0; i < remove_from_cart.length; i++) {  
		remove_from_cart[i].onclick = function () {
			courseId = this.getAttribute('data')
			template = "remove_from_cart"

			BasketLogic.productManager(courseId, template);
		}
	}
}


wishlistUrl = location.origin + '/api/wishlist/'
const WishlistLogic = {
 	wishlistPostManager(courseId) {
 		fetch(wishlistUrl, {
 			method: 'POST',
 			credentials: 'include',
 			headers: {
 				'Content-Type': 'application/json',
 				'Authorization': `Bearer ${localStorage.getItem('token')}`
 			},
 			body: JSON.stringify({
 				'course': courseId,
 			})
 		})
 			.then(response => response.json())
 			.then(data => {
 				try {
 					wishlistManager()
 				}catch{
 				}
 			});
 	}
}



var add_to_wishlist = document.getElementsByClassName('add_to_wishlist');
for (let i = 0; i < add_to_wishlist.length; i++) {
 	add_to_wishlist[i].onclick = function () {
 		const courseId = this.getAttribute('data');
 		WishlistLogic.wishlistPostManager(courseId);
 	}
}


