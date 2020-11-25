$( document ).ready(function() {


    $('i').on('click',null, null, function (){
        // handle_like_dislike_click(this);
        handle_dislike_add_to_plan_click(this);
    });

    function handle_dislike_button_clicked(ele) {
        var new_value = -1;
        var recipe_name = ele.attr('name');
        if( ele.hasClass('de_select') ){
            new_value = 1;  // add to dislike list
        }else{
            new_value = 0;  // remove from dislike list
        }
        $.ajax({
           type: 'POST',
           url: 'submit_dislike',
           data: {
                'value' : new_value,
                'recipe_name' : recipe_name
           },
           success: function (data){
               if(data['status'] == 1){
                   if(new_value == 1){
                       ele.notify("Recipe added to dislike list", "error");
                   }else{
                       ele.notify("Recipe removed from dislike list", "success");
                   }
               }
           }
        });
    }

    function handle_add_to_meal_button_clicked(ele) {
        var recipe_name = ele.attr('name');
        var new_value = -1;
        if( ele.hasClass('de_select') ){
            new_value = 1;  // add
        }else{
            new_value = 0;  // remove
        }
        $.ajax({
           type: 'POST',
           url: 'submit_add_to_meal',
           data: {
                'value' : new_value,
                'recipe_name' : recipe_name
           },
           success: function (data){
               if(data['status'] == 1){
                   if(new_value == 1){
                       ele.notify("Recipe added to meal plan list", "success");
                   }else{
                       ele.notify("Recipe removed from meal plan list", "error");
                   }
                   $('#meal_plan_progress').css({ width: data['meal_plan_progress'] + '%' });
               }
           }
        });
    }

    function handle_dislike_add_to_plan_click(ele){
        var is_like = $('#' + ele.id).attr('like')

        if(is_like == 0){
            handle_dislike_button_clicked( $('#' + ele.id) );
        }else{
            handle_add_to_meal_button_clicked( $('#' + ele.id) )
        }

        // update CSS should not be here
        update_css_for_add_to_meal_plan(ele)

    }

    function update_css_for_add_to_meal_plan(ele){
        var is_like = $('#' + ele.id).attr('like');
        if( $('#' + ele.id).hasClass('de_select') ){
            $('#' + ele.id).removeClass('de_select');
            if(is_like == 0){
                $('#' + ele.id).addClass('dis_like_color_select');
            }else{
                $('#' + ele.id).addClass('like_color_select');
            }
        }else if( $('#' + ele.id).hasClass('like_color_select') || $('#' + ele.id).hasClass('dis_like_color_select') ){
            $('#' + ele.id).removeClass('like_color_select');
            $('#' + ele.id).removeClass('dis_like_color_select');
            $('#' + ele.id).addClass('de_select');
        }
    }

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

    // response to exlore more button
    function handle_load_more(ele, recipe_name){
        direction = $('input:checked').attr('direction');
        critique_name = $('input:checked').attr('column');

        $.ajax({
           type: 'POST',
           url: 'submit_load_more',
           data: {
                'direction' : direction,
                'critique_name' : critique_name,
                'recipe_name' : recipe_name
           },
           success: function (data){
               if(data['status'] == 1){
                    $('#recipe_list').fadeOut(500, function(){
                        $(this).html(data['list-content']);
                        $('#recipe_list').fadeIn(1000);
                        handle_explore_more();
                        // binding the on click event to the cart
                        $('i').bind('click', function (){
                            handle_dislike_add_to_plan_click(this);
                        });
                    });

                    $('#direction_section').fadeOut(500, function(){
                        console.log(data['direction-content'])
                        $(this).html(data['direction-content']);
                        $('#direction_section').fadeIn(1000);
                        $('#show_meal_plan').bind('click', function(){
                            handle_show_meal_plan(this);
                        });
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
    }

    function handle_explore_more(ele){
        $('div[id^="expl_more_"]').on('click', function (){
            var recipe_name = $(this).attr('name')
            $.ajax({
                type: 'POST',
                url: 'load_critique',
                data: {
                    'recipe_name' : recipe_name
                },
                success: function(data){
                    if (data['status'] == 1){
                        var ele_id = 'critique_panel_' + recipe_name;
                        $('#' + ele_id).fadeOut(500, function(){
                                $(this).html(data['critique-content']);
                                $('#' + ele_id).fadeIn(100);
                                $('input[group=' + recipe_name + ']').bind('click', function (){
                                    handle_critique_clicked(this);
                                });
                                var expl_id = 'btn-load-' + recipe_name;
                                $('#' + expl_id).bind('click', function () {
                                    handle_load_more(this,recipe_name);
                                });
                        });
                    }
                }
            });
        });
    }

    function handle_show_meal_plan(ele){
        $.ajax({
                type: 'POST',
                url: 'show_meal_plan',
                data: {
                },
                success: function(data){
                    $("#modal_holder" ).html(data['model_template']);
                    $("#meal_plan_modal" ).modal('toggle');

                    $('a[id^="model_delete_"]').click(function (){
                        handle_remove_recipe_from_model(this);
                    });
                }
            });
    }

    function handle_remove_recipe_from_model(ele){
        recipe_id =  $('#' + ele.id).attr('item_id')
        $.ajax({
           type: 'POST',
           url: 'submit_add_to_meal',
           data: {
                'value' : 0,
                'recipe_name' : recipe_id
           },
           success: function (data){
               if(data['status'] == 1){
                   $('#model-recipe-' + recipe_id).fadeOut(1000, function(){
                    });

                    $('#add-to-plan-' + recipe_id).removeClass('like_color_select');
                    $('#add-to-plan-' + recipe_id).removeClass('dis_like_color_select');
                    $('#add-to-plan-' + recipe_id).addClass('de_select');

                    $('#meal_plan_progress').css({ width: data['meal_plan_progress'] + '%' });
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

    // for button: 'Proceed, I am done reviewing recipes
    $('#dislike_add_meal_done_button').click(function (){
        $('.feedback-section').each(function(index){
            // $(this).html( ("<i class=\"fas fa-shopping-cart fa-2x\"></i>") );
        });

        $.ajax({
         type: 'POST',
         url: 'submit_dislike_add_to_plan',
         data: {
         },
         success: function(data){
            if (data['status'] == 1){
                $('#recipe_list').fadeOut(500, function(){
                    $(this).html(data['list-content']);
                    $('#recipe_list').fadeIn(1000);
                    handle_explore_more();
                    // binding the on click event to the cart
                    $('i').bind('click', function (){
                        handle_dislike_add_to_plan_click(this);
                    });
                });

                $('#direction_section').fadeOut(500, function(){
                    $(this).html(data['direction-content']);
                    $('#direction_section').fadeIn(1000);
                    $('#show_meal_plan').bind('click', function(){
                        handle_show_meal_plan(this);
                    });
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

    $('#show_meal_plan').click(function (){
        handle_show_meal_plan(this)
    });


});