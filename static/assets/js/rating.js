
$(document).ready(function(){
    $('#commentform input[type=radio]').click(function(){
        document.getElementById("star_value").value = this.value;
    });
});


// commentform.onsubmit = (e) => {
//     e.preventDefault();
//     const formData = new FormData(commentform);
//     var ratingvalue = formData.get("rating");
//     document.getElementById("star_value").value = ratingvalue
// };


// (function() {
//     let form = document.getElementById("commentform");
//     form.addEventListener('submit', async (event) => {
//         event.preventDefault();
//         let postData = {
//             "user": form.user.value,
//             "rating": form.star_value.value,
//             "course": form.course_id.value,
//             "comment": form.comment.value,
//         }
//         let response = await fetch('http://127.0.0.1:8000/api/comments/', {
//              headers: {
//                  'Content-Type': 'application/json',
//                  },
//              method: "POST",
//              body: JSON.stringify(postData)
//         }); 
 
//     });
 
//  })();