let success_body = document.getElementById("success_body")
console.log('saam')
function SuccessManager() {
    fetch('http://127.0.0.1:8000/api/success/', {
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
            for (let i = 0; i < data.length; i++) {
                console.log(data)
                if (data[i]['is_paid'] == true) {
                    total_price += parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100)
                    html += `
            <tr>
            <td class="course-remove"></td>

            <td class="course-image" style="text-align: center; vertical-align: middle;">
            <a href="#"><img width="150"  src="${data[i]['course']['image']}" alt="Add Product" /></a>
            </td>
            <td class="course-name">
            <a href="#">${data[i]['course']['title']}</a>
            </td>
            <td class="course-price">
            <span>$${parseFloat(data[i]['course']['discounted_price']).toFixed(2)* (100 - data[i]['coupon_discount']) / 100}</span>
            </td>
          
            <td class="course-fullprice">
            <span>$${parseFloat(data[i]['course']['discounted_price']* (100 - data[i]['coupon_discount']) / 100).toFixed(2)}</span>
            </td>
            </tr>
			`
                }
            }
            success_body.innerHTML = html
            
            if (data.length == 0) {
                total_products.style.display = 'none'
            } 

        });
}

window.addEventListener('DOMContentLoaded', (event) => {
    SuccessManager()
});
