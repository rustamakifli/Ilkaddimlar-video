$(document).ready(function(){
    $('#commentform input[type=radio]').click(function(){
        document.getElementById("star_value").value = this.value;
    });
});