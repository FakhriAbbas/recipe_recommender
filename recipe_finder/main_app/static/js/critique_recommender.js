$( document ).ready(function() {

    // $('i[id^=tup-\\*]').click(function() {
    //     alert('hi')
    // });

    $('i').on('click',null, null, function (){
        handle_like_dislike_click(this);
    });

    function handle_like_dislike_click(ele){
        var is_like = $('#' + ele.id).attr('like')
        if(is_like == 1){
            other_icon = $('#' + ele.id).siblings()[0];
        }else{
            other_icon = $('#' + ele.id).siblings()[0];
        }
        if(is_like == 1){
            if( $('#' + ele.id).hasClass('de_select') ){
                $('#' + ele.id).removeClass('de_select');
                $('#' + ele.id).addClass('like_color_select');
                $(other_icon).removeClass('dis_like_color_select')
                $(other_icon).addClass('de_select')
            } else if( $('#' + ele.id).hasClass('like_color_select') ){
                $('#' + ele.id).removeClass('like_color_select');
                $('#' + ele.id).addClass('de_select');
            }
        }
        if(is_like == 0){
            if( $('#' + ele.id).hasClass('de_select') ){
                $('#' + ele.id).removeClass('de_select');
                $('#' + ele.id).addClass('dis_like_color_select');
                $(other_icon).removeClass('like_color_select')
                $(other_icon).addClass('de_select')
            } else if( $('#' + ele.id).hasClass('dis_like_color_select') ){
                $('#' + ele.id).removeClass('dis_like_color_select');
                $('#' + ele.id).addClass('de_select');
            }
        }
    }

    function handle_shopping_cart_click(ele){
        if( $('#' + ele.id).hasClass('de_select') ){
            $('#' + ele.id).removeClass('de_select');
            $('#' + ele.id).addClass('like_color_select');
        }else{
            $('#' + ele.id).removeClass('like_color_select');
            $('#' + ele.id).addClass('de_select');
        }
    }

    function handle_critique_clicked(ele){
        var group_val = $(ele).attr('group');
        $('button[id^="btn-load-"]').prop('disabled', true);
        $('#btn-load-' + group_val).prop('disabled', false);
    }

    function handle_filling_shopping_done(btn){
        $('.feedback-section').each(function(index){
            // $(this).html( ("<i class=\"fas fa-shopping-cart fa-2x\"></i>") );
        });

        $.ajax({
         type: 'POST',
         url: 'submit_shopping',
         data: {
         },
         success: function(data){
            if (data['status'] == 1){
                $('#recipe_list').fadeOut(500, function(){
                    $(this).html(data['list-content']);
                    $('#recipe_list').fadeIn(1000);
                });

                $('#direction_section').fadeOut(500, function(){
                    $(this).html(data['direction-content']);
                    $('#direction_section').fadeIn(1000);
                    $('input[type="radio"]').bind('click', function (){
                        handle_critique_clicked(this);
                    });

                });



            }
         }
        });
    }

    $('#like_done_button').click(function (){
        $('.feedback-section').each(function(index){
            // $(this).html( ("<i class=\"fas fa-shopping-cart fa-2x\"></i>") );
        });

        $.ajax({
         type: 'POST',
         url: 'submit_like_dislike',
         data: {
         },
         success: function(data){
            if (data['status'] == 1){
                $('#recipe_list').fadeOut(500, function(){
                    $(this).html(data['list-content']);
                    $('#recipe_list').fadeIn(1000);
                    // binding the on click event to the cart
                    $('i').bind('click', function (){
                        handle_shopping_cart_click(this);
                    });
                });

                $('#direction_section').fadeOut(500, function(){
                    $(this).html(data['direction-content']);
                    $('#direction_section').fadeIn(1000);
                });

                $('#button_section').fadeOut(500, function(){
                    $(this).html(data['button-content']);
                    $('#button_section').fadeIn(1000);
                    $('#shopping_done_button').bind('click', function (){
                        handle_filling_shopping_done(this);
                    });
                });

            }
         }
        });
    });


});