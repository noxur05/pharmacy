$(document).ready(function(){
    $('.submitButton').click(function(event){
        event.preventDefault()
        console.log('submit button works');
        let form = $('#parent-form')[0];
        let modelName = $('#selected_model_name').val();

        let formData = new FormData(form);
        formData.append('selected_model_name', modelName);
        console.log(formData);
        $.ajax({
            url:'/admin/add/',
            type:'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()  // CSRF token
            },
            success: function(response){
                console.log('Success:');
            },
            error: function(response){
                console.log('Error:', response);
            }
        });
    });
});
