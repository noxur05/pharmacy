$(document).ready(function(){
    $('.submitButton').click(function(event){
        event.preventDefault()
        let form = $('#parent-form')[0];
        let modelName = $('#selected_model_name').val();

        let formData = new FormData(form);
        formData.append('selected_model_name', modelName);
        let formControl = $('.form-control');
        let formIsValid = true;
        formControl.each(function(){
            if ($(this).val() == ''){
                formIsValid = false;
                $(this).addClass('is-invalid')
            } else {
                $(this).removeClass('is-invalid')
            }
        });
        if (formIsValid){
            $.ajax({
                url:'/admin/add/',
                type:'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response){
                    console.log('Success:');
                    formControl.each(function(){
                        $(this).val('')
                    });
                },
                error: function(response){
                    console.log('Error:', response);
                }
            });
        }
    });
    // $('.editBtn').click(function(){
    //     let button = $(this).val();
    //     let nameModel = $('#nameModel').val()
    //     console.log(button, nameModel);
    //     $.ajax({
    //         url:'/admin/edit/',
    //         type:'POST',
    //         data: {
    //             'id': button,
    //             'model': nameModel,
    //             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    //         },
    //         success: function(response){
    //             console.log('Success:');
    //         },
    //         error: function(response){
    //             console.log('Error:', response);
    //         }
    //     });
    // });
});
