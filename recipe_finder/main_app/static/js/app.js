$( document ).ready(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $('#btn-user-next').click(function(event) {
        data_dict = {
            'username' : $('#userID').val()
        }


        $.get('submit_user_form/',data_dict, function(data){
            window.location.href = data['redirect-url']
        });

     });


});