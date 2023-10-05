
document.addEventListener("DOMContentLoaded", function() {
    const logout_button = document.getElementById('logout_button');
    const profile_image_img = document.getElementById('profile_image_in_base');

    const b_node = document.getElementById('login_name');
    const url_value=b_node.getAttribute('check_url');
    const csrftoken=getCookie('csrftoken');
    

    $.ajax({ //
        type: 'POST',
        url: url_value,
        headers: {"X-CSRFToken":csrftoken},
        data: {
            'aa': 'aa'  
        },
        processData: false,
        contentType: false,                
        success: function (response) {
            b_node.textContent=response.message+" 님 환영합니다.";
            logout_button.classList.add('visible');
            console.log("profile url : "+ response.profile_url);
            profile_image_img.src=response.profile_url;
            profile_image_img.classList.add('visible');

        }
    });

});

