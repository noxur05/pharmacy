$(document).ready(function() {
    const translations = {
        'en': {
            'removed_from_cart': 'Removed from Cart',
            'added_to_cart': 'Added to Cart',
            'gosh': 'Add',
            'ayyr': 'Remove'
        },
        'tm': {
            'removed_from_cart': 'Sarpdan aýryldy',
            'added_to_cart': 'Sarpana goşuldy',
            'gosh': 'Goş',
            'ayyr': 'Aýyr'
        },
        'ru': {
            'removed_from_cart': 'Удалено из корзины',
            'added_to_cart': 'Добавлено в корзину',
            'gosh': 'Добавить',
            'ayyr': 'Удалить'
        }
    };

    $('.addBtn').click(function(event){
        event.preventDefault();
        let button = $(this);
        let inCart = button.data('in-cart') === 'True';
        
        let form = button.closest('.add-form');
        let productId = form.find('input[name="product_id"]').val();
        button.prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: '/product/add/', 
            contentType: 'application/json',
            dataType: 'json', 
            data: JSON.stringify({ 
                'data': productId  
            }),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
            },
            success: function(response){
                console.log('Success:');
                button.data('in-cart', inCart ? 'False' : 'True');
                $('.totalQuantity').text(response.total_quantity)
                let currentLanguage = response.lang;
                console.log(currentLanguage)
                
                function getTranslation(key) {
                    return translations[currentLanguage][key] || key;
                }
                if (response.status == 'deleted') {
                    console.log('Removed from Cart');
                    button.find('span').text(getTranslation('gosh'));
                } 
                else {
                    button.find('span').text(getTranslation('ayyr'));
                    console.log('Added to Cart');
                }
                button.prop('disabled', false);
            },
            error: function(response){
                console.log('Error:', response);
                button.prop('disabled', false);
            }
        });
    });

    $('.likeBtn').click(function(el){
        el.preventDefault();
        let button = $(this);
        console.log('clicked');
        let form = button.closest('.like-form');
        let productId = form.find('input[name="product_id"]').val();
        let inLike = button.data('in-like') === 'True';

        if (inLike){
            // Change classList of i in button
            button.find('i').removeClass('bi-heart-fill').addClass('bi-heart');
        }
        else{
            button.find('i').removeClass('bi-heart').addClass('bi-heart-fill');
        }
        button.prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: '/like/liked/',  // Replace with your view's URL
            data: {
                'data': productId,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response){
                console.log('Success: Liked');
                button.data('in-like', inLike ? 'False' : 'True');
                button.prop('disabled', false);


            },
            error: function(response){
                console.log('Error:', response);
                button.prop('disabled', false);

                // Handle the error (e.g., display a message)
            }
        });
        // setTimeout(() =>{
        //     button.prop('disabled', false)
        // }, 200);
    });
});



