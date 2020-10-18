$( document ).ready(function() {


    $('#preference-btn').click(function (event) {
        var q1_values = read_checkbox_values('q1');
        var q3_values = read_checkbox_values('q3');

        console.log(q1_values)
        console.log(q3_values)

        if(VALIDATION){
            // TODO
        }

        $.ajax({
         type: 'POST',
         url: 'preference',
         data: {
             'q1[]' : q1_values,
             'q3[]' : q3_values
         },
         success: function(data){
             if (data['status'] == 1){
                 window.location.href = data['redirect-url']
             }else{
                 alert(data['error-msg'] + ':' + 'preference');
             }
         }
        });


    });

});