$( document ).ready(function() {

    $('#q2_o3').change(function (event) {
        var value = !$('#q2_o3').is(":checked")
        $("#q2-text").prop('disabled', value);
    });

    $('#q4_o3').change(function (event) {
        var value = !$('#q4_o3').is(":checked")
        $("#q4-text").prop('disabled', value);
    });

    $('#q2_o1').change(function (event) {
        var value = !$('#q2_o1').is(":checked")
        $("#q5-text").prop('disabled', value);
    });

    $('#q4_o1').change(function (event) {
        var value = !$('#q4_o1').is(":checked")
        $("#q6-text").prop('disabled', value);
    });

    $('#pre-survey-btn').click(function (event) {
        var q1 = $("input:radio[name ='q1']:checked").val();
        var q2_values = read_checkbox_values('q2');
        var q2_text = $("#q2-text").val();
        var q3 = $("input:radio[name ='q3']:checked").val();
        var q4_values = read_checkbox_values('q4');
        var q4_text = $("#q4-text").val();
        var q5 = $('#q5-text').val();
        var q6 = $('#q6-text').val();

        console.log(q2_values);
        if(VALIDATION){
            // TODO
        }
        $.ajax({
         type: 'POST',
         url: 'pre_survey',
         data: {
             'q1' : q1,
             'q2[]' : q2_values,
             'q2_text' : q2_text,
             'q3' : q3,
             'q4[]' : q4_values,
             'q4_text' : q4_text,
             'q5' : q5,
             'q6' : q6
         },
         success: function(data){
             if (data['status'] == 1){
                 window.location.href = data['redirect-url']
             }else{
                 alert(data['error-msg'] + ':' + 'pre_survey');
             }
         }
        });
    });

});