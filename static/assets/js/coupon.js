var CouponLogic = {
    couponManager(code) {
        fetch('http://127.0.0.1:8000/api/coupon/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                'code': code,
            })
        })
            .then(response => response.json())
            .then(data => {
                cartManager()
                cartItemManager()
            });
    }
}

coupon_button = document.getElementById('coupon_button')
coupon_button.onclick = function () {
    coupon_code = document.getElementById('coupon_code').value
    CouponLogic.couponManager(coupon_code)
    console.log('coupon works')
}